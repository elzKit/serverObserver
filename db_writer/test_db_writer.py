from unittest import TestCase
import time
import db_writer


class Test(TestCase):
    def test_write_ok_record_with_match(self):
        message = {
            'timestamp': time.time(),
            'url': 'http://toto.com',
            'response_time': 2.0,
            'status_code': '200',
            'matched': True}
        db_writer.write(message)
        # TODO actuall test something

    def test_write_ok_record_without_match(self):
        message = {
            'timestamp': time.time(),
            'url': 'http://toto.com',
            'response_time': 2.0,
            'status_code': '200',
        }
        db_writer.write(message)
        # TODO actuall test something

    def test_write_err_record(self):
        message = {
            'timestamp': time.time(),
            'url': 'http://toto.com',
            'error_msg': 'bla'
        }
        db_writer.write(message)
