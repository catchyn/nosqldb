const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'nodejs-app',
  brokers: [process.env.KAFKA_BROKERS || 'localhost:9092'],
  retry: {
    initialRetryTime: 1000,
    retries: 5
  }
});

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

const producer = kafka.producer();
const consumer = kafka.consumer({ groupId: 'test-group' })
const admin = kafka.admin();

const send = async () => {
  await producer.connect();
  await producer.send({
    topic: 'any-message-topic',
    messages: [{ value: 'Test message from nodejs app' }, { value: 'Another test message from nodejs app'}],
  });
  console.log('Message sent successfully');
  await producer.disconnect();
};

const receive = async () => {
    await consumer.connect()
    await consumer.subscribe({ topic: 'any-message-topic', fromBeginning: true })
    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        console.log(`new message from consumer--topic:${topic}--partition:${partition}--value:${message.value.toString()}--fullMessage:${JSON.stringify(message)}`)
      },
    })
    console.log('Message receive function run successfully');
}

const getTopicList = async () => {
    await setupKafka();

    const topics = await admin.listTopics();
    console.log('topics:', topics);
}

const setupKafka = async () => {
  await admin.connect();

  await admin.createTopics({
    topics: [{
      topic: 'any-message-topic',
      numPartitions: 1,
      replicationFactor: 1,
    }],
    waitForLeaders: true
  });

  await admin.disconnect();
}

const errorWrapper = async (f, title) => {
    try {
        await f();
    } catch(error) {
        console.error(title || f.name, error);
        throw error;
    }
}

const processing = async () => {
    await errorWrapper(setupKafka);
    await delay(2000)
//    await errorWrapper(getTopicList);
    await errorWrapper(send);
    await delay(1000)
    await errorWrapper(receive);
}

processing().catch(console.error);
