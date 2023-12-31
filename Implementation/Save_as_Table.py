# import all the required packages
from sqlalchemy.engine import create_engine
import base64
from pymongo import MongoClient
import mysql.connector


# Creating a table/document based on the database type in the specified schema.
def save_as_table(db_type, df, filename):
    if db_type:
        database_type = db_type["type"].lower()
        username = db_type.get("username")
        password = db_type.get("password")
        password = (base64.b64decode(password)).decode('ascii')
        host = db_type.get("host")
        database = db_type.get("database")
        schema_name = db_type.get("schema")
        port = db_type.get("port")

        # create connections to the database based on the user input
        if database_type == "mongodb":
            client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}/{database}?ssl=true')
            db = client[database]
            collection = db[filename]
            documents = df.to_dict(orient='records')
            collection.insert_many(documents)
            client.close()

        elif database_type == "oracle":
            oracle_engine = create_engine(f'oracle+oracledb://{username}:{password}@{host}:{port}/{database}')
            df.to_sql(filename, con=oracle_engine, schema=schema_name, if_exists="replace", index=False)
            oracle_engine.dispose()

        elif database_type == "mysql":
            mysql_db = mysql.connector.connect(host=host, user=username, password=password, database=database)
            df.to_sql(filename, con=mysql_db, schema=schema_name, if_exists="replace", index=False)
            mysql_db.close()

        else:
            postgres_engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
            df.to_sql(filename, con=postgres_engine, schema=schema_name, if_exists="replace", index=False)
            postgres_engine.dispose()

    else:
        pass
