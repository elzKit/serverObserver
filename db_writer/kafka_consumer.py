from kafka import KafkaConsumer
import db_writer


def consume_events(cert_folder,
                   host,
                   port,
                   db_uri,
                   topic='server_metrics',
                   table_name='server_metrics'):
    """
    Reads a kafka topic and writes the messages read to DB writer.
    """
    consumer = KafkaConsumer(
        topic,
        client_id="server-metrics-client",
        group_id="server-metrics-group",
        bootstrap_servers=host + ":" + port,
        security_protocol="SSL",
        ssl_cafile=cert_folder + "/ca.pem",
        ssl_certfile=cert_folder + "/service.cert",
        ssl_keyfile=cert_folder + "/service.key",
    )
    print('kafka consumer ready to receive...')

    for msg in consumer:
        json_msg = json.loads(msg.value)
        print("Received: {}".format(json_msg))
        db_writer.write(db_uri, json_msg, table_name)


if __name__ == "__main__":
    import json
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--cert-folder', help="Path to folder containing required Kafka certificates", required=True)
    parser.add_argument('--host', help="Kafka Host (obtained from Aiven console)", required=True)
    parser.add_argument('--port', help="Kafka Port (obtained from Aiven console)", required=True)
    parser.add_argument('--db-uri', help="postreSQL uir", required=True)
    parser.add_argument('--topic-name', help="Topic Name", default='server_metrics')
    parser.add_argument('--table-name', help="Table Name", default='server_metrics')
    args = parser.parse_args()

    consume_events(cert_folder=args.cert_folder,
                   host=args.host,
                   port=args.port,
                   db_uri=args.db_uri,
                   topic=args.topic_name,
                   )
