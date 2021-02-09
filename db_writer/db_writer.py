import psycopg2


def write(db_uri, json_msg, table_name = "server_metrics"):
    try:
        db_conn = psycopg2.connect(db_uri)
        cursor = db_conn.cursor()
        # trying to be as generic as possible here, perhaps better ways exist?
        columns = str(tuple([k for k in json_msg.keys()])).replace("'", "") # columns must be without '
        values = str(tuple([str(v).replace("'","") for v in json_msg.values()])) # values must be with ', hence as str

        q = f"""INSERT INTO {table_name} {columns} VALUES {values}"""
        cursor.execute(q)
        db_conn.commit()
        print('written db record for', json_msg)
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if (db_conn):
            cursor.close()
            db_conn.close()

