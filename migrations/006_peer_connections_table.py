steps = [
    [
        """
        CREATE TABLE peer_connections (
            id SERIAL PRIMARY KEY NOT NULL,
            sender INT NOT NULL REFERENCES users(id),
            recipient INT NOT NULL REFERENCES users(id),
            status VARCHAR(50) NOT NULL,
            has_messaged BOOL DEFAULT FALSE
        );
        """,
        """
        DROP TABLE peer_connections;
        """,
    ],
]
