from alembic.config import Config
from alembic import command, context
from sqlalchemy import create_engine


def create_migration():
    # Load the Alembic configuration

    alembic_cfg = Config("alembic.ini")
    # Replace with your actual Alembic configuration file

    # Create an initial migration
    command.revision(
        alembic_cfg, autogenerate=True, message="Initial migration")


def apply_migrations():
    # Access the database URL from the context object
    db_url = context.config.get_main_option("sqlalchemy.url")

    # Create an engine using the db_url
    engine = create_engine(db_url)

    # Load the Alembic configuration
    alembic_cfg = Config("alembic.ini")
    # Replace with your actual Alembic configuration file

    # Apply all available migrations using the engine
    with engine.connect() as connection:
        alembic_cfg.attributes['connection'] = connection
        command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    create_migration()  # Create the initial migration
    apply_migrations()  # Apply all available migrations
