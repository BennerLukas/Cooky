from dataclasses import dataclass
import time
import sqlalchemy
import psycopg2
import psycopg2.extras
import pandas as pd
import re
import logging


@dataclass
class DataBase:
    pwd = 1234
    port = 5432
    hostname = "localhost"

    alchemy_connection = None
    psycopg2_connection = None

    dataset_file_path = "C:/Projects/Cooky/data/full_dataset.csv"

    # dataset_file_path = "C:/Projects/Cooky/data/part_dataset.csv"

    def __init__(self):
        self.connect()
        self.del_schema()
        df = self.read_csv()
        self.clean_and_dump(df)
        self.init_schema()

    def connect(self):
        b_connected = False

        while b_connected is False:
            # tests if the database is already accessible
            try:
                # set the needed connections and engines
                alchemy_engine = sqlalchemy.create_engine(
                    f'postgresql+psycopg2://postgres:{self.pwd}@{self.hostname}:{self.port}/postgres')
                self.alchemy_connection = alchemy_engine.connect()

                self.psycopg2_connection = psycopg2.connect(database="postgres", user="postgres", port=self.port,
                                                            password=self.pwd, host=self.hostname)

                # if all connections were successful the connection status is set to true
                b_connected = True
                logging.info("Database Connected")

            except Exception as an_exception:
                logging.warning("No Connection possible - try again in 5s")
                time.sleep(5)
        return True

    def del_schema(self):
        s_sql_statement = open("../db/del.sql", "r").read()

        # cleaning file from comments and escape functions
        s_sql_statement = re.sub(r"--.*|\n|\t", " ", s_sql_statement)
        res = self.alchemy_connection.execute(s_sql_statement)
        logging.debug(res)

    def init_schema(self):
        s_sql_statement = open("../db/init.sql", "r").read()

        # cleaning file from comments and escape functions
        s_sql_statement = re.sub(r"--.*|\n|\t", " ", s_sql_statement)
        res = self.alchemy_connection.execute(s_sql_statement)
        logging.debug(res)

    def get_data_from_table(self, table_name, b_full_table=True, s_query=None):
        if b_full_table is True:
            df = pd.read_sql_table(table_name, self.alchemy_connection)
        elif b_full_table is False and s_query is not None:
            df = self._get_select(s_query)
        else:
            logging.error("Error occurred. Maybe table does not exist")
            raise
        return df

    def _get_select(self, sql_query: str):
        try:
            df = pd.read_sql_query(sql_query, self.alchemy_connection)
        except Exception as an_exception:
            logging.error(an_exception)
            logging.error("Query couldn't be executed.")
            return False
        return df

    def write_df2table(self, df, table_name, mode="append"):
        try:
            logging.info("Dump to Database")
            res = df.to_sql(table_name, self.alchemy_connection, if_exists=mode)
            logging.info("Dump to completed")
            logging.info(f"Response Value{res} ")
        except:
            logging.error("Error occurred. Maybe df has wrong shape or data inside")
            raise

    def write_sql2table(self, sql):
        try:
            db_cursor = self.psycopg2_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            db_cursor.execute(sql)
            # tries to get content of cursor (result of query) - if empty fails with ProgrammingError
            try:
                result = db_cursor.fetchall()
            except psycopg2.errors.ProgrammingError:
                result = None

            # finishes transaction and closes session
            self.psycopg2_connection.commit()
            db_cursor.close()
            logging.info("Executed SQL query successfully")
            return True, result
            # if SQL statement was invalid it'll be caught and database connection reestablished
        except psycopg2.errors.InFailedSqlTransaction:
            self.b_connected = False
            self._connect()
            logging.error("Transaction Failed - Review given inputs! Reestablished connection to database backend")
            return False, None

    def read_csv(self):
        logging.info("Read CSV File")
        df = pd.read_csv(self.dataset_file_path, sep=",", )
        logging.info("Read Finished")
        return df

    def clean_and_dump(self, df_recipes):

        df_recipes.columns = ["n_recipe_id", "s_recipe_title", "array_ingredients", "s_directions", "s_link",
                              "s_source",
                              "array_NER"]
        df_recipes = df_recipes.set_index("n_recipe_id")
        logging.info(df_recipes.head())

        # make ingredients a list
        df_recipes.array_ingredients = df_recipes.array_ingredients.apply(eval)

        # extract all distinct raw ingredients into separate df
        df_ingredients = df_recipes.explode("array_ingredients")[["array_ingredients"]]

        # extract measurements & amount  --> forget amounts if some is there its there...?

        # map ingredient to base items

        # new feature meta-tag (style, culture, veggie)

        # length of direction text => complexity

        # Definition of Done 1
        # Add, Del Items to pantry
        # Cook recipe - remove items
        # get_data_from_table
        # write_to_table

        # Check if cook-able

        # Definition of Done 2
        # User Input ->  possible prefiltering with tags -> check for valid recipes -> rank for specific user -> output recipe

        # Definition of Done 3 (Ayman)
        # Pretty GUI

        logging.info("Dump to Database")
        res = df_recipes.to_sql("recipes", self.alchemy_connection, if_exists="append")
        logging.info("Dump to completed")
        logging.info(f"Response Value{res} ")


if __name__ == "__main__":
    db = DataBase()
