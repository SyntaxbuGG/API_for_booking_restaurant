import os

from dotenv import load_dotenv

load_dotenv()



SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL")
