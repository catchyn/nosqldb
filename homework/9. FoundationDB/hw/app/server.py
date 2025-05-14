import fdb
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from contextlib import contextmanager

# Инициализация FoundationDB
fdb.api_version(620)
db = fdb.open()

# Определяем пространства ключей
PRODUCTS_SUBSPACE = fdb.Subspace(('products',))
PRICE_INDEX_SUBSPACE = fdb.Subspace(('index', 'price'))
SIZE_INDEX_SUBSPACE = fdb.Subspace(('index', 'size'))

app = FastAPI()


class Product(BaseModel):
    product_id: int
    title: str
    price: float
    size: int


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    size: Optional[int] = None


class ProductIdsResponse(BaseModel):
    product_ids: List[int]


@contextmanager
def transaction_scope():
    """Контекстный менеджер для явных транзакций"""
    tr = db.create_transaction()
    try:
        yield tr
        tr.commit().wait()
    except fdb.FDBError as e:
        tr.on_error(e.code).wait()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@app.post("/products/", response_model=dict)
def create_product(product: Product):
    @fdb.transactional
    def create_tx(tr):
        if tr[PRODUCTS_SUBSPACE[product.product_id]].present():
            raise HTTPException(status_code=400, detail="Product already exists")

        tr[PRODUCTS_SUBSPACE[product.product_id]] = json.dumps(product.dict()).encode()
        price_key = PRICE_INDEX_SUBSPACE.pack((float(product.price), int(product.product_id)))
        size_key = SIZE_INDEX_SUBSPACE.pack((int(product.size), int(product.product_id)))
        tr[price_key] = b''
        tr[size_key] = b''

    create_tx(db)
    return {"message": "Product created"}


@app.put("/products/{product_id}", response_model=dict)
def update_product(product_id: int, update: ProductUpdate):
    @fdb.transactional
    def update_tx(tr):
        product_key = PRODUCTS_SUBSPACE[product_id]
        product_data = tr[product_key]

        if not product_data.present():
            raise HTTPException(status_code=404, detail="Product not found")

        product_dict = json.loads(product_data.decode())
        old_price = float(product_dict['price'])
        old_size = int(product_dict['size'])
        new_price = float(update.price) if update.price is not None else old_price
        new_size = int(update.size) if update.size is not None else old_size

        if update.title is not None:
            product_dict['title'] = update.title
        if update.price is not None:
            product_dict['price'] = new_price
        if update.size is not None:
            product_dict['size'] = new_size

        tr[product_key] = json.dumps(product_dict).encode()

        if update.price is not None and new_price != old_price:
            old_price_key = PRICE_INDEX_SUBSPACE.pack((old_price, product_id))
            new_price_key = PRICE_INDEX_SUBSPACE.pack((new_price, product_id))
            tr.clear(old_price_key)
            tr[new_price_key] = b''

        if update.size is not None and new_size != old_size:
            old_size_key = SIZE_INDEX_SUBSPACE.pack((old_size, product_id))
            new_size_key = SIZE_INDEX_SUBSPACE.pack((new_size, product_id))
            tr.clear(old_size_key)
            tr[new_size_key] = b''

    update_tx(db)
    return {"message": "Product updated"}


@app.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int):
    @fdb.transactional
    def delete_tx(tr):
        product_key = PRODUCTS_SUBSPACE[product_id]
        product_data = tr[product_key]

        if not product_data.present():
            raise HTTPException(status_code=404, detail="Product not found")

        product_dict = json.loads(product_data.decode())

        tr.clear(product_key)

        price_key = PRICE_INDEX_SUBSPACE.pack((float(product_dict['price']), product_id))
        size_key = SIZE_INDEX_SUBSPACE.pack((int(product_dict['size']), product_id))
        tr.clear(price_key)
        tr.clear(size_key)

    delete_tx(db)
    return {"message": "Product deleted"}


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    @fdb.transactional
    def get_tx(tr):
        product_key = PRODUCTS_SUBSPACE[product_id]
        product_data = tr[product_key]

        if not product_data.present():
            raise HTTPException(status_code=404, detail="Product not found")

        try:
            return json.loads(product_data.decode())
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail="Invalid product data format") from e

    try:
        return get_tx(db)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/by_price/", response_model=ProductIdsResponse)
def get_products_by_price_range(min_price: float, max_price: float):
    try:
        @fdb.transactional
        def query_tx(tr):
            product_ids = []
            for kv in tr.get_range(PRICE_INDEX_SUBSPACE.pack((min_price,)), PRICE_INDEX_SUBSPACE.pack((max_price,))):
                price, product_id = PRICE_INDEX_SUBSPACE.unpack(kv.key)
                product_ids.append(product_id)
            return {"product_ids": sorted(product_ids)}

        return query_tx(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving products: {str(e)}")


@app.get("/products/by_size/", response_model=ProductIdsResponse)
def get_products_by_size_range(min_size: int, max_size: int):
    try:
        @fdb.transactional
        def query_tx(tr):
            product_ids = []
            for kv in tr.get_range(SIZE_INDEX_SUBSPACE.pack((min_size,)), SIZE_INDEX_SUBSPACE.pack((max_size,))):
                size, product_id = SIZE_INDEX_SUBSPACE.unpack(kv.key)
                product_ids.append(product_id)
            return {"product_ids": sorted(product_ids)}

        return query_tx(db)

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid product data format")
