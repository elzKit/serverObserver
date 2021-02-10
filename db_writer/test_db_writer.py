from unittest import TestCase
import time
import os
import psycopg2

import db_writer


class Test(TestCase):

    def setUp(self):
        # for simplicity, we assume the test db is already running
        self.url = "postgres://avnadmin:oajw7gopckewmims@pg-276e6f6c-elisa-50a0.aivencloud.com:13046/defaultdb?sslmode=require"
        self.table_name = "server_metrics_test"
        self.db_conn = psycopg2.connect(self.url)
        self.cursor = self.db_conn.cursor()
        #normally we would have a new DB each time. We fake it here
        try:
            q = f"DROP TABLE {self.table_name};"
            self.cursor.execute(q)
            self.db_conn.commit()
        except:
            self.db_conn.rollback()
            # cover this failure with silence, since it is normal

    def tearDown(self):
        try:
            q = f"DROP TABLE {self.table_name};"
            self.cursor.execute(q)
            self.db_conn.commit()
        except psycopg2.errors.UndefinedTable as e:
            self.db_conn.rollback()
        self.cursor.close()
        self.db_conn.close()

    def helper_get_records_count(self):
        try:
            q = f"""SELECT * from {self.table_name}"""
            self.cursor.execute(q)
            records = self.cursor.fetchall()
            self.db_conn.commit()
            return len(records)
        except:
            self.db_conn.rollback()
            return -1

    def test_initial_state(self):
        n = self.helper_get_records_count()
        self.assertEqual(n, -1)

    def test_create_db(self):
        db_writer.create_table_if(self.url, table_name=self.table_name)
        n = self.helper_get_records_count()
        self.assertEqual(n,0)

    def test_create_db_2(self):
        # test that we do not create a table, if one is already there
        n = self.helper_get_records_count()
        self.assertEqual(-1, n, 'initial state - table does not exist')
        db_writer.create_table_if(self.url, table_name=self.table_name)
        n = self.helper_get_records_count()
        self.assertEqual(0, n, 'empty table is there')
        message = {
            'timestamp': time.time(),
            'url': 'http://toto.com',
            'response_time': 2.0,
            'status_code': '200',
            'matched': True}
        db_writer.write(self.url, message, table_name=self.table_name)
        n = self.helper_get_records_count()
        self.assertEqual(1, n, 'we write 1 element')
        db_writer.create_table_if(self.url, table_name=self.table_name)
        n = self.helper_get_records_count()
        self.assertEqual(1, n, "the element is still there, even if we attempt to create a table")

    def test_write_ok_record_with_match(self):
        db_writer.create_table_if(self.url, table_name=self.table_name)
        message = {
            'timestamp': time.time(),
            'url': 'http://toto.com',
            'response_time': 2.0,
            'status_code': '200',
            'matched': True}
        db_writer.write(self.url, message, table_name=self.table_name)
        n = self.helper_get_records_count()
        self.assertEqual(1, n, "write msg without match")

    def test_write_ok_record_without_match(self):
        db_writer.create_table_if(self.url, table_name=self.table_name)
        message = {
            'timestamp': time.time(),
            'url': 'http://toto.com',
            'response_time': 2.0,
            'status_code': '200',
            }
        db_writer.write(self.url, message, table_name=self.table_name)
        n = self.helper_get_records_count()
        self.assertEqual(1, n, "write msg without match")

    def test_write_err_record(self):
        db_writer.create_table_if(self.url, table_name=self.table_name)
        message = {
            'timestamp': time.time(),
            'url': 'http://toto.com',
            'error_msg': 'bla'
        }
        db_writer.write(self.url, message, table_name=self.table_name)
        n = self.helper_get_records_count()
        self.assertEqual(1, n, "write msg without match")



