import logging

from pyodbc import connect, DatabaseError

from flask import current_app as app

LOGGER = logging.getLogger(__name__)


def get_connection():
    host = app.config["HOST"]
    port = app.config["PORT"]
    user = app.config["USERNAME"]
    password = app.config["PASSWORD"]

    conn = connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s,%s;UID=%s;PWD=%s' % (host, port, user, password))
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
