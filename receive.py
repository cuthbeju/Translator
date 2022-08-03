import pika, sys, os
import json

# adapted from: https://www.rabbitmq.com/tutorials/tutorial-one-python.html
# date of retrieval: 08/02/22
def main():
    """
    Listens for responses from Random Sentence Generator microservice and writes the response to a JSON file.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='rand_sentence')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        random_sentence = body.decode('utf-8')
        
        # adapted from: https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
        # date of retrieval: 08/02/22
        with open("sentence.json", "w") as outfile:
            json.dump(random_sentence, outfile)

    channel.basic_consume(queue='rand_sentence', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)