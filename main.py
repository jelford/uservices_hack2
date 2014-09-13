import pika
from psycopg2 import connect
from json import dumps
parameters = pika.URLParameters('amqp://54.76.117.95:5672')
channel = None
ALL_TOPICS_SQL = 'SELECT DISTINCT topic FROM facts;'

def on_open(connection):
  # Invoked when the connection is open
  print "Connected!", connection
  connection.channel(on_channel_open)

def on_channel_open(new_channel):
  global channel
  channel = new_channel
  # channel.exchange_declare(on_exchange_declareok, 'combo', 'topic')
  topics = all_topics()
  message = { "authors": [ "@jelford", "@sleepyfox" ] }
  message.update({ "topics": topics })
  channel.basic_publish('combo', 'test_topic', dumps(message))

# Create our connection object, passing in the on_open method
connection = pika.SelectConnection(parameters, on_open)

def all_topics():
  """Return a list of all topics."""
  conn = connect(host='microservices-chris-10sep2014.cc9uedlzx2lk.eu-west-1.rds.amazonaws.com', database='micro',
                 user='microservices', password='microservices')
  cursor = conn.cursor()
  try:
      cursor.execute(ALL_TOPICS_SQL)
      topics = [row[0] for row in cursor.fetchall()]
      # self.send_response(200)
      # self.send_header("Content-Type", "application/json")
      # self.end_headers()
      print "All topics: ", topics
      return topics 
  # except Exception as e:
  #     print 'Exception: %s' % e.message
  #     # print_exc()
  finally:
      cursor.close()
      conn.close()

try:
    # Loop so we can communicate with RabbitMQ
    connection.ioloop.start()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed, will stop on its own
    connection.ioloop.start()
