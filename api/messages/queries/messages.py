import os
from psycopg_pool import ConnectionPool

pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])


class MessageQueries:
    def get_user_info(self, user_id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT u.username, u.profile_image, u.profile_link
                    FROM users u
                    WHERE u.id = %s
                    """,
                    [user_id],
                )
                row = cur.fetchone()
                user_info = {
                    "username": row[0],
                    "profile_image": row[1],
                    "profile_link": row[2],
                }
        return user_info

    def dict_to_list(self, dict1):
        conversations = []
        messages = []
        for key, value in dict1.items():
            for item in value:
                item["user_id"] = key
                messages.append(item)
            conversations.append(messages)
            messages = []
        return conversations

    def get_messages(self, user_id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT u.id AS user_id, m.id, m.recipient,
                        m.sender, m.date, m.content, m.is_read
                    FROM users u
                    JOIN messages m ON(u.id = m.recipient OR u.id = m.sender)
                    WHERE u.id = %s
                    ORDER BY m.date DESC
                    """,
                    [user_id],
                )
                messages = {}
                for row in cur.fetchall():
                    message = {
                        "id": row[1],
                        "recipient": row[2],
                        "sender": row[3],
                        "date": row[4],
                        "content": row[5],
                        "is_read": row[6],
                    }
                    if message["recipient"] == user_id:
                        user_info = self.get_user_info(message["sender"])
                        message.update(user_info)
                    elif message["sender"] == user_id:
                        user_info = self.get_user_info(message["recipient"])
                        message.update(user_info)
                    # check if other user is recipient or sender
                    if message["recipient"] == user_id:
                        key = message["sender"]
                        if key in messages:
                            messages[key].append(message)
                        else:
                            messages[key] = [message]
                    elif message["sender"] == user_id:
                        key = message["recipient"]
                        if key in messages:
                            messages[key].append(message)
                        else:
                            messages[key] = [message]
                conversations = self.dict_to_list(messages)
        return conversations

    def get_messages_from_one_user(self, user_id, user2_id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT u.id AS user_id, m.id, m.recipient,
                        m.sender, m.date, m.content, m.is_read
                    FROM users u
                    JOIN messages m ON (
                        (u.id = m.recipient AND m.sender = %s)
                        OR (u.id = m.sender AND m.recipient = %s)
                    )
                    WHERE u.id IN (%s, %s)
                    ORDER BY m.date DESC
                    """,
                    [user_id, user_id, user2_id, user2_id],
                )
                messages = []
                for row in cur.fetchall():
                    message = {
                        "id": row[1],
                        "recipient": row[2],
                        "sender": row[3],
                        "date": row[4],
                        "content": row[5],
                        "is_read": row[6],
                    }
                    user2_info = self.get_user_info(user2_id)
                    user_id = {"user_id": user2_id}
                    message.update(user2_info)
                    message.update(user_id)
                    messages.append(message)
        return messages

    def create_message(self, data):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                params = [
                    data.sender,
                    data.recipient,
                    data.content,
                ]
                cur.execute(
                    """
                    INSERT INTO messages (sender, recipient, content)
                    VALUES (%s, %s, %s)
                    RETURNING id, sender, recipient, content, date, is_read
                    """,
                    params
                )
                record = None
                row = cur.fetchone()
                if row is not None:
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]
                    user_info = self.get_user_info(record["recipient"])
                    user_id = {"user_id": record["recipient"]}
                    record.update(user_info)
                    record.update(user_id)
                return record
