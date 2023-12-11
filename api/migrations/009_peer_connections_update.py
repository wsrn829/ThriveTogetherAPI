steps = [
    [
        """
        ALTER TABLE peer_connections
        ADD COLUMN sender_name VARCHAR(50) NOT NULL,
        ADD COLUMN recipient_name VARCHAR(50) NOT NULL;
        """,
        """
        DROP TABLE peer_connections;
        """,
    ],
]
