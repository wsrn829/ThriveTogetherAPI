steps = [
    [
        """
        CREATE TABLE peer (
            user_id INT NOT NULL REFERENCES users(id),
            peer_id INT NOT NULL REFERENCES users(id),
            peer_name VARCHAR(50) NOT NULL,
            profile_link VARCHAR(1000),
            tags_id INT REFERENCES tags(id),
            profile_image VARCHAR(1000),
            status INT NOT NULL DEFAULT 0
        );
        """,
        """
        DROP TABLE peer;
        """,
    ],
]
