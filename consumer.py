#!/usr/bin/env python
#
# Example consumer of queue messages
#
# pip3 install -r requirements.txt
#
import argparse
import sys
import os
import pika
import signal

def queue_callback(channel, method, properties, body):
  if len(method.exchange):
    print("from exchange '{}': {}".format(method.exchange,body.decode('UTF-8')))
  else:
    print("from queue {}: {}".format(method.routing_key,body.decode('UTF-8')))

def signal_handler(signal,frame):
  print("\nCTRL-C handler, cleaning up rabbitmq connection and quitting")
  connection.close()
  sys.exit(0)

example_usage = '''====EXAMPLE USAGE=====

Connect to remote rabbitmq host
--user=guest --password=guest --host=192.168.1.200

Specify exchange and queue name
--exchange=myexchange --queue=myqueue
'''

ap = argparse.ArgumentParser(description="RabbitMQ producer",
                             epilog=example_usage,
                             formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--user',default="guest",help="username e.g. 'guest'")
ap.add_argument('--password',default="guest",help="password e.g. 'pass'")
ap.add_argument('--host',default="localhost",help="rabbitMQ host, defaults to localhost")
ap.add_argument('--port',type=int,default=5672,help="rabbitMQ port, defaults to 5672")
ap.add_argument('--exchange',default="",help="name of exchange to use, empty means default")
ap.add_argument('--queue',default="testqueue",help="name of default queue, defaults to 'testqueue'")
ap.add_argument('--routing-key',default="testqueue",help="routing key, defaults to 'testqueue'")
ap.add_argument('--body',default="my test!",help="body of message, defaults to 'mytest!'")
args = ap.parse_args()


# connect to RabbitMQ
credentials = pika.PlainCredentials(args.user, args.password )
connection = pika.BlockingConnection(pika.ConnectionParameters(args.host, args.port, '/', credentials ))
channel = connection.channel()

channel.basic_consume(queue=args.queue, on_message_callback=queue_callback, auto_ack=True)

# capture CTRL-C
signal.signal(signal.SIGINT, signal_handler)

print("Waiting for messages, CTRL-C to quit...")
print("")
channel.start_consuming()

