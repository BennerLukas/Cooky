import re
from dataclasses import dataclass
import time
import sqlalchemy
import psycopg2
import psycopg2.extras
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

from food_extractor.food_model import FoodModel
from recommender import Recommender


@dataclass
class DataBase:
    pwd = 1234
    port = 5432
    hostname = "localhost"

    alchemy_connection = None
    psycopg2_connection = None

    # dataset_file_path = "./data/part_dataset.csv"
    dataset_file_path = "./src/data/big_part_dataset.csv"
    # dataset_file_path = "./src/data/part_dataset.csv"

    # dataset_file_path = "./data/part_dataset.csv"
    # dataset_file_path = "./data/big_part_dataset.csv"


    def __init__(self, db_init=True):
        self.connect()
        if db_init is True:
            self.del_schema()
            df = self.read_csv()
            df_recipes = self.dump_recipes(df)
            self.dump_ingredients(df_recipes)

            self.init_schema()
            self.generate_synthetic_user_data()

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
        s_sql_statement = open("./src/db/del.sql", "r").read()

        # cleaning file from comments and escape functions
        s_sql_statement = re.sub(r"--.*|\n|\t", " ", s_sql_statement)
        res = self.alchemy_connection.execute(s_sql_statement)
        logging.debug(res)

    def init_schema(self):
        s_sql_statement = open("./src/db/init.sql", "r").read()

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
        df = pd.read_csv(self.dataset_file_path, sep=",")
        logging.info("Read Finished")
        return df

    def dump_recipes(self, df):

        df.columns = ["n_recipe_id", "s_recipe_title", "array_ingredients", "s_directions", "s_link",
                      "s_source", "array_NER"]
        df_recipes = df.set_index("n_recipe_id")
        df_recipes = df_recipes.reset_index(drop=True)
        df_recipes.index.names = ["n_recipe_id"]
        self.write_df2table(df_recipes, table_name="recipes")

        logging.info(df_recipes.head())
        return df_recipes

    def get_quantities(self, df_recipes, df_ingredients, df_items):
        # Deprecated!!!

        # get cleaned measurements
        raw_measurements = list()
        amounts_needed = list()
        f_amounts_needed = list()
        s_unit_types = list()

        for item, raw_ingredient in zip(ingredients_cleaned, ingredient_inputs):
            if item is not None:
                for item_part in item.split(" "):
                    raw_ingredient = raw_ingredient.replace(item_part, "")

            raw_measurements.append(raw_ingredient)

            # split into amount and unit type:
            raw_ingredient = raw_ingredient.lower()
            if "c." in raw_ingredient:
                result = re.search(".+?(?=c\.)", raw_ingredient)[0].replace(" ", "")
                amounts_needed.append(result)
                s_unit_types.append("cup(s)")

            elif "tsp." in raw_ingredient:
                result = re.findall(".+?(?=tsp\.)", raw_ingredient)[0].replace(" ", "")
                amounts_needed.append(result)
                s_unit_types.append("tsp")

            elif "tbsp." in raw_ingredient:
                result = re.findall(".+?(?=tbsp\.)", raw_ingredient)[0].replace(" ", "")
                amounts_needed.append(result)
                s_unit_types.append("tsp")

            elif "lb." in raw_ingredient:
                result = re.findall(".+?(?=lb\.)", raw_ingredient)[0].replace(" ", "")
                amounts_needed.append(result)
                s_unit_types.append("lb")

            elif "pkg." in raw_ingredient:
                result = re.findall(".+?(?=pkg\.)", raw_ingredient)[0].replace(" ", "")
                amounts_needed.append(result)
                s_unit_types.append("pkg")

            # jar
            elif "jar" in raw_ingredient:
                result = re.findall(".+?(?=jar)", raw_ingredient)[0].replace(" ", "")
                amounts_needed.append(result)
                s_unit_types.append("jar")

            elif "can" in raw_ingredient and "canned" not in raw_ingredient:
                result = re.findall(".+?(?=can)", raw_ingredient)[0].replace(" ", "")
                amounts_needed.append(result)
                s_unit_types.append("can")

            elif raw_ingredient[0].isdigit():
                result = re.findall("\d.", raw_ingredient)[0].replace(" ", "")
                amounts_needed.append(result)
                s_unit_types.append("number")

            else:
                amounts_needed.append(None)
                f_amounts_needed.append(None)
                s_unit_types.append(None)
                continue

            try:
                f_amounts_needed.append(float(result))
            except ValueError:
                try:
                    f_amounts_needed.append(eval(result))
                except (SyntaxError, NameError):
                    try:
                        search_pattern = "^[^\d]*(\d+)"
                        result = re.findall(search_pattern, result)
                        f_result = float(result[0])
                        f_amounts_needed.append(f_result)

                    except:
                        f_amounts_needed.append(1)

        df_ingredients["s_raw_measurements"] = raw_measurements
        df_ingredients["s_amount_needed"] = amounts_needed
        df_ingredients["f_amount_needed"] = f_amounts_needed
        df_ingredients["s_unit_type"] = s_unit_types

        return df_recipes, df_ingredients, df_items

    def dump_ingredients(self, df_recipes):

        # make ingredients a list
        df_recipes.array_ingredients = df_recipes.array_ingredients.apply(eval)
        df_recipes["n_recipe_id"] = df_recipes.index

        # extract all raw ingredients into separate df
        items = set()
        ingredients_dict = dict()
        ingredient_name = list()
        ingredient_recpie_id = list()
        ingredients_list = df_recipes[["array_NER", "n_recipe_id"]]
        for recipe_ingredient, n_recipe_id in zip(ingredients_list.array_NER, ingredients_list.n_recipe_id):
            ingredients = recipe_ingredient.replace("[", "").replace("]", "").split(", ")
            for ingredient in ingredients:
                items.add(ingredient)
                ingredient_name.append(ingredient)
                ingredient_recpie_id.append(n_recipe_id)

        df_items = pd.DataFrame(list(items), columns=["s_item_name"])
        df_items["n_item_id"] = df_items.index

        data = list()
        data.append(ingredient_recpie_id)
        data.append(ingredient_name)
        df_ingredients = pd.DataFrame(data).transpose()
        df_ingredients.columns = ["n_recipe_id", "s_ingredient_name"]

        df_ingredients = df_ingredients.merge(df_items, how="left", left_on=["s_ingredient_name"], right_on=["s_item_name"])
        df_ingredients = df_ingredients.drop(["s_item_name"], axis=1)
        df_ingredients.index.names = ["n_ingredient_id"]
        df_ingredients["s_unit_type"] = "<not_specified>"
        df_ingredients["f_amount_needed"] = 1
        self.write_df2table(df_items, table_name="items")
        self.write_df2table(df_ingredients, table_name="ingredients")

        return df_ingredients

    def generate_synthetic_user_data(self):
        df_recipes = self.get_data_from_table("recipes", b_full_table=True)
        max_recipe_id = df_recipes.n_recipe_id.max()

        df = pd.read_csv("./src/data/BX-Book-Ratings.csv", sep=";", encoding='CP1252', escapechar='\\')
        df = df[df["Book-Rating"] != 0]

        df_lookup = pd.DataFrame(df.ISBN.unique(), columns=["ISBN"])
        df_lookup["n_recipe_id"] = df_lookup.index
        df_lookup = df_lookup.where(df_lookup["n_recipe_id"] <= max_recipe_id)

        df_joined = df.merge(df_lookup, on="ISBN", how="inner")

        df_final = df_joined.drop(columns=["ISBN"])
        df_final = df_final.rename(columns={
            "User-ID": "n_user_id",
            "Book-Rating": "n_rating",
        })

        self.write_df2table(df_final, "ratings")

        # write users to db
        df_users = pd.DataFrame(df["User-ID"].unique(), columns=["n_user_id"])
        df_users["s_username"] = "synth-user"
        df_users = df_users.set_index("n_user_id")
        self.write_df2table(df_users, "users")

        return True


if __name__ == "__main__":
    db = DataBase()
