# A besic message publisher
import pika
from json import dumps

parameters = pika.URLParameters('amqp://54.76.117.95:5672')

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='combo')
# properties = pika.BasicProperties(content_type="text/plain", delivery_mode=2)
message = { "authors": [ "@jelford", "@sleepyfox" ] }
channel.basic_publish('combo', 'test_topic', dumps(message))
