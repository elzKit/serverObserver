# server observer
A tiny system which monitors a list of URLs
and stores the collected metrics to a PostgreSQL db.
Designed as 2 separate components, connected via kafka. 

## website_checker
  * monitors a list of websites in json fromat. For each website,
    a regexp can be speficied. See websites.json for example of the format expected
  * collects the response time, status code and, optionally, presence of regexp on the page
  * in case of connection error, it collects the error message
  * writes messages to a kafka topic (by default, "server_metrics")

## db_writer
* reads messages from a kafka topic, and stores them in a PostgreSQL table.

# Installation

## Service setup
* create Kafka service and PostgreSQL service. They can be created easily with aiven, 
as described in [here](https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka)
and [here](https://help.aiven.io/en/articles/489573-getting-started-with-aiven-postgresql)

* Store the credentials (ca.pem, service.cert and service.key) in "cert-folder" 
* Create a kafka topic. The default topic assumed by the system is "server_metrics".
* Create a PostgreSQL table. The default table assumed by the system is "server_metrics"

## Installing the website_checker
```bash
cd website_checker
virtualenv --python=python3.7 .venv
source .venv/bin/activate
pip install requests kafka-python
```

### Usage
```bash
python kafka_producer.py --cert-folder=<your cert-folder> --host=<your kafka service url> 
--port=<the port of your kafka service>
```

By default, it checks the websites specified in the websites.json config file provided.

## Installing the db_writer

```bash
cd db_writer
virtualenv --python=python3.7 .venv
source .venv/bin/activate
pip install psycopg2-binary kafka-python
```
### Usage
```bash
python kafka_consumer.py --cert-folder=<credentials folder> --host=<your kafka service url> 
--port=<the port of your kafka service> --db-uri=<postgreSQL db uri>
```
