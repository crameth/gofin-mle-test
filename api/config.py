import os

db_config = {
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "host": os.environ["MYSQL_HOST"],
    "database": os.environ["MYSQL_DATABASE"],
    "raise_on_warnings": True
}