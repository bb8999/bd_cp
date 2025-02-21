import pg8000
from queue import Queue
from contextlib import contextmanager
from settings import DB_CONFIG, POOL_MIN_CONN, POOL_MAX_CONN
import atexit

class Pg8000ConnectionPool:
    def __init__(self, min_conn, max_conn, db_config):
        self.db_config = db_config
        self.pool = Queue(maxsize=max_conn)
        self.min_conn = min_conn
        self.max_conn = max_conn

        for _ in range(min_conn):
            self.pool.put(self._create_connection())

    def _create_connection(self):
        return pg8000.connect(**self.db_config)

    def get_connection(self):
        if self.pool.empty() and self.pool.qsize() < self.max_conn:
            return self._create_connection()
        return self.pool.get()

    def put_connection(self, connection):
        try:
            self.pool.put(connection, block=False)
        except Exception:
            connection.close()

    def close_all_connections(self):
        while not self.pool.empty():
            conn = self.pool.get()
            conn.close()

print("Initializing connection pool...")
connection_pool = Pg8000ConnectionPool(POOL_MIN_CONN, POOL_MAX_CONN, DB_CONFIG)

@contextmanager
def get_connection():
    connection = connection_pool.get_connection()
    try:
        yield connection
    finally:
        connection_pool.put_connection(connection)

def close_connection_pool():
    if connection_pool:
        connection_pool.close_all_connections()
        print("Connection pool closed.")

def on_exit():
    print("Приложение завершено! Закрываем ресурсы...")
    close_connection_pool()

atexit.register(on_exit)
