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

    def read_csv(self):
        logging.info("Read CSV File")
        # df = pd.read_csv("C:/Projects/Cooky/data/full_dataset.csv", sep=",", )
        df = pd.read_csv("C:/Projects/Cooky/data/part_dataset.csv", sep=",", )
        logging.info("Read Finished")
        return df

    def clean_and_dump(self, df_recipes):
        
        df_recipes.columns = ["n_recipe_id", "s_recipe_title", "array_ingredients", "s_directions", "s_link", "s_source",
                      "array_NER"]
        df_recipes = df_recipes.set_index("n_recipe_id")
        logging.info(df_recipes.head())

        # TODO cleaning + enhancing

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
