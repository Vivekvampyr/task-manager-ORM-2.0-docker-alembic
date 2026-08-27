from sqlalchemy import create_engine, text
from app.db.database import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as connection:
    result = connection.execute(
        text("SELECT current_user, current_database()")
    )
    print(result.fetchone())