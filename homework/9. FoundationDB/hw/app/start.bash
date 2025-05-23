#! /bin/bash

# start.bash
#
# This source file is part of the FoundationDB open source project
#
# Copyright 2013-2024 Apple Inc. and the FoundationDB project authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

set -xe;

echo "START START STARTs"

if [[ -z "${FDB_CLUSTER_FILE:-}" || ! -s "${FDB_CLUSTER_FILE}" ]]; then
    /app/create_cluster_file.bash
    FDB_CLUSTER_FILE="${FDB_CLUSTER_FILE:-/etc/foundationdb/fdb.cluster}"

    # Attempt to connect. Configure the database if necessary.
    if ! /usr/bin/fdbcli -C "${FDB_CLUSTER_FILE}" --exec status --timeout 3 ; then
        echo "creating the database"
        if ! fdbcli -C "${FDB_CLUSTER_FILE}" --exec "configure new single memory ; status" --timeout 10 ; then
            echo "Unable to configure new FDB cluster."
            exit 1
        fi
    fi
fi

# Новая проверка файла кластера
if [[ -f "${FDB_CLUSTER_FILE}" ]]; then
    echo "Cluster file created at ${FDB_CLUSTER_FILE}"
    echo "File contents:"
    cat "${FDB_CLUSTER_FILE}"
else
    echo "ERROR: Cluster file not found at ${FDB_CLUSTER_FILE}" >&2
    exit 1
fi

# Запускаем приложение
echo "=== STARTING APPLICATION ==="
exec uvicorn server:app --host 0.0.0.0 --port 5000