steps = [
    [
        """
        ALTER TABLE peer_connections
        ALTER COLUMN has_messaged TYPE VARCHAR(255);
        """,
        """
        DROP TABLE peer_connections;
        """,
    ],
]
