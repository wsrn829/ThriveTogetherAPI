steps = [
    [
        """
        ALTER TABLE peer
        add column id SERIAL PRIMARY KEY NOT NULL;
        """,
        """
        DROP TABLE peer;
        """,
    ],
]
