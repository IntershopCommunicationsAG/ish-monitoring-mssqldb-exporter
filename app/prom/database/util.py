import logging
import socket
from pyodbc import connect, DatabaseError, InterfaceError, OperationalError

from flask import current_app as app

LOGGER = logging.getLogger(__name__)


def is_port_open():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((app.config["SERVER"], int(app.config["PORT"])))
        s.shutdown(2)
        return True
    except:
        return False

def get_connection():
    driver = app.config["DRIVER"]
    server = app.config["SERVER"]
    port = app.config["PORT"]
    user = app.config["USERNAME"]
    password = app.config["PASSWORD"]
    try:
        conn = connect('DRIVER={};SERVER={};PORT={};UID={};PWD={}'.format(driver, server, port, user, password))
    except OperationalError:
        raise InterfaceError
    return conn


def get_query_result(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        column_name = [column[0] for column in cursor.description]
        for row in result:
            yield dict(zip(column_name, row))
    except DatabaseError as e:
        LOGGER.error("Query: %s has error: %s", query, str(e))
