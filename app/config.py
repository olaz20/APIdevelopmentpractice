from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
class Settings(BaseSettings):   #this is to perform validation 
   database_hostname: str
   database_port: str
   database_password: str
   database_name: str
   database_username: str
   secret_key: str
   algorithm: str
   access_token_expire_minutes: int
   
   class Config:
       env_file = ".env"
       env_file_encoding = 'utf-8'
settings = Settings()


