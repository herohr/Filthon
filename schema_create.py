import pymysql
from database_connect_consts import *


def create_tables():
    config = {
        'host': HOSTNAME,
        'port': PORT,
        'user': USERNAME,
        'password': PASSWORD,
        'db': DATABASE
    }
    schema = """
        CREATE TABLE students(
        id VARCHAR(20) NOT NULL,
        longitude DOUBLE DEFAULT 0,
        latitude DOUBLE DEFAULT 0,
        ask BOOLEAN DEFAULT false,
        PRIMARY KEY(`id`)
        );
        CREATE TABLE cars(
        id int unsigned auto_increment,
        longitude double default 0,
        latitude double default 0,
        ask BOOLEAN DEFAULT false,
        primary key(`id`)
        )

    """  # MYSQL

    db = pymysql.connect(**config)
    db.cursor().execute(schema)

    db.commit()
    db.close()

if __name__ == "__main__":
    create_tables()
