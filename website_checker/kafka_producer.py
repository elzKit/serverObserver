import time

from kafka import KafkaProducer, errors
from kafka.admin import KafkaAdminClient, NewTopic

import website_checker


def create_topic(cert_folder,
                 host,
                 port,
                 topic):
    admin_client = KafkaAdminClient(
        bootstrap_servers=host + ":" + port,
        security_protocol="SSL",
        ssl_cafile=cert_folder + "/ca.pem",
        ssl_certfile=cert_folder + "/service.cert",
        ssl_keyfile=cert_folder + "/service.key",
        client_id='kafka_producer',
    )

    try:
        topic_list = [NewTopic(name=topic, num_partitions=1, replication_factor=1)]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except errors.TopicAlreadyExistsError as e:
        if "already exsits" not in str(e):
            print(e)


def produce_events(cert_folder,
                   host,
                   port,
                   topic,
                   waiting_time_in_sec,
                   url_list):
    """
    The website metrics producer is a kafka producer which periodically checks a list of websites using website_checker
    and writes the collected metrics to the kafka topic
    """

    producer = KafkaProducer(
        bootstrap_servers=host + ":" + port,
        security_protocol="SSL",
        ssl_cafile=cert_folder + "/ca.pem",
        ssl_certfile=cert_folder + "/service.cert",
        ssl_keyfile=cert_folder + "/service.key",
    )
    print('kafka producer ready to send')

    while True:
        for el in url_list:
            if isinstance(el, list):
                url = el[0]
                regexp = el[1] if len(el) > 1 else None
            else:
                url = el
                regexp = None
            message = website_checker.check(url, regexp)
            try:
                producer.send(topic, json.dumps(message).encode("utf-8"))
                print(f"sent message: {message}")
            except Exception as e:
                print('send failed', e)
            producer.flush()
        # wait between the round of checks
        time.sleep(waiting_time_in_sec)


if __name__ == "__main__":
    import json
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--cert-folder', help="Path to folder containing required Kafka certificates", required=True)
    parser.add_argument('--host', help="Kafka Host (obtained from Aiven console)", required=True)
    parser.add_argument('--port', help="Kafka Port (obtained from Aiven console)", required=True)
    parser.add_argument('--topic-name', help="Topic Name", default='server_metrics')
    parser.add_argument('--waiting-time', help="waiting time between url checks", default="1")
    parser.add_argument('--website-file', help="json file with a list of websites (and regex patterns) to check",
                        default="website_list.json")
    args = parser.parse_args()

    with open(args.website_file) as f:
        website_list = json.load(f)
    print("Monitoring websites:", website_list)

    create_topic(cert_folder=args.cert_folder,
                 host=args.host,
                 port=args.port,
                 topic=args.topic_name)

    produce_events(cert_folder=args.cert_folder,
                   host=args.host,
                   port=args.port,
                   topic=args.topic_name,
                   waiting_time_in_sec=int(args.waiting_time),
                   url_list=website_list)
