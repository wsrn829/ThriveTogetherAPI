steps = [
    [
        """
        ALTER TABLE messages
        ALTER COLUMN is_read SET DEFAULT FALSE;
        """,
        """
        DROP TABLE messages;
        """,
    ],
]
