from kafka import KafkaConsumer
import db_writer


def consume_events(cert_folder,
                   host,
                   port,
                   db_uri,
                   topic_name,
                   table_name):
    """
    Reads a kafka topic and writes the messages read to DB writer.
    """
    consumer = KafkaConsumer(
        topic_name,
        client_id="server-metrics-client",
        group_id="server-metrics-group",
        bootstrap_servers=host + ":" + port,
        security_protocol="SSL",
        ssl_cafile=cert_folder + "/ca.pem",
        ssl_certfile=cert_folder + "/service.cert",
        ssl_keyfile=cert_folder + "/service.key",
    )

    db_writer.create_table_if(db_uri, table_name)

    print(f'kafka consumer ready to receive from {topic_name} and write to {table_name}')

    for msg in consumer:
        json_msg = json.loads(msg.value)
        print(f"Received {json_msg}")
        db_writer.write(db_uri, json_msg, table_name)


if __name__ == "__main__":
    import json
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--cert-folder', help="Path to folder containing required Kafka certificates", required=True)
    parser.add_argument('--host', help="Kafka Host (obtained from Aiven console)", required=True)
    parser.add_argument('--port', help="Kafka Port (obtained from Aiven console)", required=True)
    parser.add_argument('--db-uri', help="postreSQL uir", required=True)
    parser.add_argument('--topic', help="Topic Name", default='server_metrics')
    parser.add_argument('--table', help="Table Name", default='server_metrics')
    args = parser.parse_args()

    consume_events(cert_folder=args.cert_folder,
                   host=args.host,
                   port=args.port,
                   db_uri=args.db_uri,
                   topic_name=args.topic,
                   table_name=args.table,
                   )
