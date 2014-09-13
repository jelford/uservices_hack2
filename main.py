import pika

parameters = pika.URLParameters('amqp://54.76.117.95:5672')
channel = None

def on_open(connection):
  # Invoked when the connection is open
  print "Connected!", connection
  connection.channel(on_channel_open)

def on_channel_open(new_channel):
  global channel
  channel = new_channel
  # channel.exchange_declare(on_exchange_declareok, 'combo', 'topic')
  channel.basic_publish('combo', 'test_topic', '{ "authors": [ "@jelford", "@sleepyfox" ] }')

# Create our connection object, passing in the on_open method
connection = pika.SelectConnection(parameters, on_open)

try:
    # Loop so we can communicate with RabbitMQ
    connection.ioloop.start()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed, will stop on its own
    connection.ioloop.start()