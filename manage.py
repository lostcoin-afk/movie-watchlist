from flask.cli import FlaskGroup
from app import app, db

cli = FlaskGroup(app)

@cli.command("create-db")
def create_db():
    """Creates all database tables."""
    db.create_all()
    print("✅ Database created.")

@cli.command("drop-db")
def drop_db():
    """Drops all database tables."""
    db.drop_all()
    print("🚫 Database tables dropped.")

@cli.command("reset-db")
def reset_db():
    """Drops and recreates all tables."""
    db.drop_all()
    db.create_all()
    print("🔁 Database reset.")

if __name__ == '__main__':
    cli()