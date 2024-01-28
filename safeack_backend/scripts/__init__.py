from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import SQLALCHEMY_DATABASE_URL

# Replace 'your_database_url' with the actual URL for your database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create an instance of the Session class to use as a session
db = Session()


def close_session():
    db.close()
