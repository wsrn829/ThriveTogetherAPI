steps = [
    [
        """
        ALTER TABLE messages
        ADD COLUMN user_id INT;
        """,
        """
        DROP TABLE messages;
        """,
    ],
]
