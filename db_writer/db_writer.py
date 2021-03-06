import psycopg2

server_metrics_schema = """
          timestamp     REAL    NOT NULL,
          url           TEXT    NOT NULL,
          response_time REAL    ,
          status_code   TEXT    ,
          matched       bool    ,
          error_msg     TEXT
"""


def create_table_if(db_uri, table_name='server_metrics'):
    db_conn = psycopg2.connect(db_uri)
    cursor = db_conn.cursor()
    try:
        q = f"SELECT * FROM {table_name};"
        cursor.execute(q)
        db_conn.commit()
    except psycopg2.errors.UndefinedTable:
        db_conn.rollback()
        q = f"CREATE TABLE {table_name} ( {server_metrics_schema} );"
        cursor.execute(q)
        db_conn.commit()
        # print('created db table', table_name)
    finally:
        cursor.close()
        db_conn.close()


def write(db_uri, json_msg, table_name="server_metrics"):
    try:
        db_conn = psycopg2.connect(db_uri)
        cursor = db_conn.cursor()
        # trying to be as generic as possible here, perhaps better ways exist?
        # cast to tuple to have str representation as (..,)
        columns = str(tuple([k for k in json_msg.keys()])).replace("'", "")  # column names (==keys) must be without '
        values = tuple([str(v) for v in json_msg.values()])

        q = f"""INSERT INTO {table_name} {columns} VALUES {values}"""
        cursor.execute(q)
        db_conn.commit()
        # print(f'written db record in {table_name} with values {json_msg}')
    except (Exception, psycopg2.Error) as error:
        print("Error while writing to PostgreSQL", error)
    finally:
        if (db_conn):
            cursor.close()
            db_conn.close()