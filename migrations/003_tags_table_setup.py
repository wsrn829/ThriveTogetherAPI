steps = [
    [
        """
        CREATE TABLE tags (
            id SERIAL PRIMARY KEY NOT NULL,
            tag VARCHAR(50) NOT NULL UNIQUE
        );
        """,
        """
        DROP TABLE tags;
        """,
    ],
]
