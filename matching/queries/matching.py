import os
from ..models import MatchesOut, TagsOut, MatchOut
from psycopg_pool import ConnectionPool

pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])


class MatchQueries:
    def get_matches(self, tag) -> MatchesOut:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT users.username, users.id, users.about_me,
                    users.profile_link, users.profile_image,
                    users.gender, users.pronouns,
                    users.about_me, tags.tag FROM users
                    JOIN user_tags ON (users.id = user_tags.user_id)
                    JOIN tags ON (user_tags.tag_id = tags.id)
                    WHERE (tags.tag = %s)
                    """,
                    [tag]
                )

                matches = []
                rows = cur.fetchall()
                for row in rows:
                    match = self.match_record_to_dict(row, cur.description)
                    user_tags = self.get_user_tags(match['username'])
                    match.update(user_tags)
                    matches.append(MatchOut(**match))
                return {"matches": matches}

    def get_user_tags(self, username) -> TagsOut:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT tags.tag FROM users
                    JOIN user_tags ON (users.id = user_tags.user_id)
                    JOIN tags ON (user_tags.tag_id = tags.id)
                    WHERE (users.username = %s)
                    """,
                    [username]
                )

                tags = []
                rows = cur.fetchall()
                for row in rows:
                    tag = str(row[0])
                    tags.append(tag)
                return {"tags": tags}

    def match_record_to_dict(self, row, description):
        match = None
        if row is not None:
            match = {}
            match_fields = [
                "username",
                "id",
                "about_me",
                "profile_link",
                "profile_image",
                "gender",
                "pronouns",
                "about_me",
            ]
            for i, column in enumerate(description):
                if column.name in match_fields:
                    match[column.name] = row[i]
        return match
