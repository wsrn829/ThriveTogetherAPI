steps = [
    [
        """
        ALTER TABLE users
        ADD COLUMN preferences VARCHAR(10)
        """,
        """
        DROP TABLE users;
        """,
    ],
]
