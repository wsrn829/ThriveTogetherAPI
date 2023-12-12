steps = [
    [
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            hashed_password VARCHAR(1000) NOT NULL,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            gender VARCHAR(50) NOT NULL,
            pronouns VARCHAR(10) NOT NULL,
            profile_link VARCHAR(75),
            profile_image VARCHAR(1000),
            banner_image VARCHAR(1000),
            email VARCHAR(150) NOT NULL,
            about_me VARCHAR(5000),
            my_story VARCHAR(5000)

        );
        """,
        """
        DROP TABLE users;
        """,
    ],

    # [
    #     """
    #     CREATE TABLE user_tags (
    #         id SERIAL PRIMARY KEY NOT NULL,
    #         user_id INT NOT NULL REFERENCES users(id),
    #         tag_id INT NOT NULL REFERENCES tags(id),
    #     );
    #     """,
    #     """
    #     DROP TABLE user_tags;
    #     """
    # ],
    # [
    #     """
    #     CREATE TABLE messages (
    #         id SERIAL PRIMARY KEY NOT NULL,
    #         recipient INT NOT NULL REFERENCES users(id),
    #         sender INT NOT NULL REFERENCES users(id),
    #         date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    #         content VARCHAR(5000),
    #         is_read BOOL
    #     );
    #     """,
    #     """
    #     DROP TABLE messages;
    #     """
    # ],
    # [
    #     """
    #     CREATE TABLE peer_connections (
    #         id SERIAL PRIMARY KEY NOT NULL,
    #         sender INT NOT NULL REFERENCES users(id),
    #         recipient INT NOT NULL REFERENCES users(id),
    #         status VARCHAR(50) NOT NULL,
    #         has_messaged BOOL DEFAULT FALSE
    #     );
    #     """,
    #     """
    #     DROP TABLE peer_connections;
    #     """

    # ]
]
