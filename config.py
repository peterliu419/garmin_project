import os
from dotenv import load_dotenv
load_dotenv()

mysql_config = {
    "host" : os.getenv("HOST"),
    "user" : os.getenv("USER"),
    "password" : os.getenv("PASSWORD"),
    "database" : os.getenv("DATABASE")
}