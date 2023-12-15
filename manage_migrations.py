from alembic.config import Config
from alembic import command


def create_migration():
    # Load the Alembic configuration
    alembic_cfg = Config("alembic.ini")
    # Replace with your actual Alembic configuration file

    # Create an initial migration
    command.revision(
        alembic_cfg, autogenerate=True, message="Initial migration")


def apply_migrations():
    # Load the Alembic configuration
    alembic_cfg = Config("alembic.ini")
    # Replace with your actual Alembic configuration file

    # Apply all available migrations
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    create_migration()  # Create the initial migration
    apply_migrations()  # Apply all available migrations
