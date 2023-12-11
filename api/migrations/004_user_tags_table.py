steps = [
    [
        """
        CREATE TABLE user_tags (
            id SERIAL PRIMARY KEY NOT NULL,
            user_id INT NOT NULL REFERENCES users(id),
            tag_id INT NOT NULL REFERENCES tags(id)
        );
        """,
        """
        DROP TABLE user_tags;
        """,
    ],
]
