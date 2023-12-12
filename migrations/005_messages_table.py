steps = [
    [
        """
        CREATE TABLE messages (
            id SERIAL PRIMARY KEY NOT NULL,
            recipient INT NOT NULL REFERENCES users(id),
            sender INT NOT NULL REFERENCES users(id),
            date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            content VARCHAR(5000),
            is_read BOOL
        );
        """,
        """
        DROP TABLE messages;
        """,
    ],
]
