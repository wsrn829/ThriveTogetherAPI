import os
from psycopg_pool import ConnectionPool

pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])


class PeerConnectionQueries:
    def create_connection(self, data):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                params = [
                    data.sender,
                    data.recipient,
                    data.status,
                    data.has_messaged,
                    data.sender_name,
                    data.recipient_name,
                ]
                cur.execute(
                    """
                    INSERT INTO peer_connections (sender, recipient, status, \
                        has_messaged, sender_name, recipient_name)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id, sender, recipient, status, has_messaged, \
                        sender_name, recipient_name
                    """,
                    params,
                )

                record = None
                row = cur.fetchone()
                if row is not None:
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]
                return record

    def get_peer_connection(self, user_id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT sender, recipient, has_messaged,sender_name, \
                        recipient_name, status
                    FROM peer_connections as p
                    WHERE (p.recipient = %s)
                    """,
                    [user_id],
                )
                peer_connections = []
                rows = cur.fetchall()
                for row in rows:
                    peer_connection = {
                        "sender": row[0],
                        "recipient": row[1],
                        "has_messaged": row[2],
                        "sender_name": row[3],
                        "recipient_name": row[4],
                        "status": row[5],
                    }
                    peer_connections.append(peer_connection)
                return peer_connections


class PeerQueries:
    def get_peers(self, user_id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT user_id, peer_id, peer_name, profile_link, tags_id,\
                        profile_image, status
                    FROM peer as p
                    WHERE (p.user_id= %s)
                    """,
                    [user_id],
                )

                peers = []
                for row in cur.fetchall():
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]
                    peers.append(record)
                return peers

    # check the request still pending or not
    def get_peer_request(self, user_id, sendRequest_id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT sender, recipient, has_messaged,sender_name,\
                        recipient_name, status
                    FROM peer_connections as p
                    WHERE (p.sender = %s and p.recipient= %s)
                    """,
                    [sendRequest_id, user_id],
                )
                rows = cur.fetchall()
                for row in rows:
                    peer_request = {
                        "sender": row[0],
                        "recipient": row[1],
                        "has_messaged": row[2],
                        "sender_name": row[3],
                        "recipient_name": row[4],
                        "status": row[5],
                    }
                return peer_request

    def update_peer_connections(self, status, user_id, sendRequest_id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    update peer_connections
                    set status = %s
                    WHERE (sender = %s and recipient= %s)
                    RETURNING sender, recipient, status, has_messaged, \
                        sender_name, recipient_name
                    """,
                    [status, sendRequest_id, user_id],
                )
                rows = cur.fetchall()
                for row in rows:
                    peer_connection = {
                        "sender": row[0],
                        "recipient": row[1],
                        "has_messaged": row[2],
                        "sender_name": row[3],
                        "recipient_name": row[4],
                        "status": row[5],
                    }
                return peer_connection

    def insert_peer(self, data):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                params = [
                    data.user_id,
                    data.peer_id,
                    data.peer_name,
                    data.profile_link,
                    data.tags_id,
                    data.profile_image,
                    data.status,
                ]
                cur.execute(
                    """
                    INSERT INTO peer (user_id, peer_id, peer_name, \
                        profile_link, tags_id, profile_image, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING user_id, peer_id, peer_name, profile_link, \
                        tags_id, profile_image, status
                    """,
                    params,
                )
                record = {}
                row = cur.fetchone()
                if row is not None:
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]
                return record
