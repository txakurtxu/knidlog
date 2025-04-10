import psycopg2
from psycopg2 import sql
from psycopg2.extras import LoggingConnection, execute_values
import os
import logging
import datetime

logger = logging.getLogger(__name__)

def connect_db():
    dsn = os.environ['SUPAB_URL']
    conn = psycopg2.connect(dsn, connection_factory = LoggingConnection, sslmode = "prefer",)
    conn.initialize(logger)
    return conn

def close_db(conn):
    conn.close()

def query_db(msg):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute(msg, )
    rows = curs.fetchall()
    close_db(conn)
    return rows

def query_usage(days):
    rest_user_ids = ['kp_386dc15554fc4aff8fc1ef0fd1fe9a9e', 'kp_405ca7ce9b914d88b72a21a744f951cf', 'kp_887bc1ba30c04ec3b8d132e9f4938784', 'kp_653232fc04174a7c9dd37e5c25eefc68', 'kp_1c0745d726614813af23e36a9b65a21e']
    query = """
            SELECT DISTINCT
            P.last_name, CC.user_id, CCS.created_at, CC.id, left(CCS.clinical_history, 10), left(CCS.differential_diagnosis #>> '{}', 10), left(CCS.transcript #>> '{}', 10)
            FROM
            clinical_cases_snapshots CCS 
            JOIN
            clinical_cases CC ON CC.id = CCS.clinical_case_id
            FULL JOIN
            profiles P on P.id = CC.user_id
            WHERE
            CC.user_id::text not in ('')
    """
    query += f"""
            AND CC.user_id::text not in ({str(rest_user_ids)[1: -1]})
            AND CCS.created_at > current_date - interval '{days - 1} day' 
            ORDER BY CCS.created_at DESC
    """
    r_val = query_db(query)
    return r_val
