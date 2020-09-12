#!/usr/bin/env python
#
# Example producer of queue message
#
# pip3 install -r requirements.txt
#
import argparse
import sys
import os
import pika


example_usage = '''====EXAMPLE USAGE=====

Connect to remote rabbitmq host
--user=guest --password=guest --host=192.168.1.200

Specify exchange, automatically sets routing-key to blank
--exchange=myexchange
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

# create queue if it does not exist
channel.queue_declare(queue=args.queue)
print("using queue: {}".format(args.queue))

# create exchange if requested
if len(args.exchange):
  args.routing_key=''
  channel.exchange_declare(exchange=args.exchange,exchange_type='fanout')
  print("declared exchange '{}'".format(args.exchange))
  channel.queue_bind(exchange=args.exchange,queue=args.queue)
  print("bound queue {} to exchange {}".format(args.queue,args.exchange))
else:
  print("using default rabbitMQ exchange")



# publish message
channel.basic_publish(exchange=args.exchange, routing_key=args.routing_key, body=args.body)

# close connection
connection.close()
sys.exit(0)
