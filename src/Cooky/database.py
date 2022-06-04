from dataclasses import dataclass
import time
import sqlalchemy
import psycopg2
import psycopg2.extras
import pandas as pd
import re
import logging

from food_extractor.food_model import FoodModel

@dataclass
class DataBase:
    pwd = 1234
    port = 5432
    hostname = "localhost"

    alchemy_connection = None
    psycopg2_connection = None

    # dataset_file_path = "C:/Projects/Cooky/data/full_dataset.csv"
    dataset_file_path = "C:/Projects/Cooky/data/part_dataset.csv"

    def __init__(self, db_init=True):
        self.connect()
        if db_init is True:
            self.del_schema()
            df = self.read_csv()
            df_recipes = self.dump_recipes(df)
            df_ingredients = self.dump_ingredients(df_recipes)
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
            self.connect()
            logging.error("Transaction Failed - Review given inputs! Reestablished connection to database backend")
            return False, None

    def read_csv(self):
        logging.info("Read CSV File")
        df = pd.read_csv(self.dataset_file_path, sep=",", )
        logging.info("Read Finished")
        return df

    def dump_recipes(self, df):

        df.columns = ["n_recipe_id", "s_recipe_title", "array_ingredients", "s_directions", "s_link",
                      "s_source", "array_NER"]
        df_recipes = df.set_index("n_recipe_id")
        self.write_df2table(df_recipes, table_name="recipes")

        logging.info(df_recipes.head())
        return df_recipes

    def dump_ingredients(self, df_recipes):

        # make ingredients a list
        df_recipes.array_ingredients = df_recipes.array_ingredients.apply(eval)

        # extract all raw ingredients into separate df
        df_ingredients = df_recipes.explode("array_ingredients")[["array_ingredients"]]
        df_ingredients = df_ingredients.reset_index()

        ingredient_inputs = df_ingredients.array_ingredients.to_list()
        model = FoodModel("chambliss/distilbert-for-food-extraction")

        output = model.extract_foods(ingredient_inputs)

        ingredients_raw_output = [x["Ingredient"] for x in output]
        ingredients_cleaned = list()
        for x in ingredients_raw_output:
            if x:   # is not empty
                text = ""
                for x_part in x:
                    text += x_part["text"] + " "
                ingredients_cleaned.append(text)
            else:
                ingredients_cleaned.append(None)

        if df_ingredients.shape[0] != len(ingredients_cleaned):
            raise

        df_ingredients["s_ingredient"] = ingredients_cleaned

        df_items = df_ingredients["s_ingredient"].drop_duplicates()
        df_items = df_items.rename("s_item_name")
        df_items.index.names = ["n_item_id"]

        self.write_df2table(df_items, table_name="items")

        df_ingredients.index.names = ["n_ingredient_id"]
        self.write_df2table(df_ingredients, table_name="ingredients")

        return df_ingredients


if __name__ == "__main__":
    db = DataBase()
