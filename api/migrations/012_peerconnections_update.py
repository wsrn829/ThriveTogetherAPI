steps = [
    [
        """
        ALTER TABLE peer_connections
        ALTER COLUMN sender_name drop not null,
        ALTER COLUMN recipient_name drop not null;
        """,
        """
        DROP TABLE peer_connections;
        """,
    ],
]
