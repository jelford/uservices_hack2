from pika import BlockingConnection, ConnectionParameters

RABBIT_HOST = '54.76.117.95'
RABBIT_PORT = 5672
EXCHANGE = 'combo'
ROUTING_KEY = '#'

def on_consume(ch, method, properties, body):
  print method.routing_key, body

conn = BlockingConnection(ConnectionParameters(host=RABBIT_HOST,
                                               port=RABBIT_PORT))
channel = conn.channel()
channel.exchange_declare(exchange=EXCHANGE, type='topic')
result = channel.queue_declare(exclusive=True)
queue = result.method.queue
channel.queue_bind(exchange=EXCHANGE, queue=queue, routing_key = ROUTING_KEY)
channel.basic_consume(on_consume, queue=queue, no_ack=True)
channel.start_consuming()