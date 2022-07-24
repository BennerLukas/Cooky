from dataclasses import dataclass
import logging
import pandas as pd

from gevent import idle

logging.basicConfig(level=logging.INFO)

from database import DataBase
from recommender import Recommender


@dataclass
class Cooky:

    def __init__(self, init_db=True):
        self.db = DataBase(init_db)
        self.n_user_id = None
        self.reco = Recommender(self.db, init_db)

        if init_db:
            self.db.write_sql2table(f"ALTER TABLE ratings ADD PRIMARY KEY (n_user_id, n_recipe_id);")

    # TODO: fetch rating from db to pass to client
    def get_rating(self):
        pass

    def add_rating(self, n_rating_value, n_recipe_id):
        s_sql = f" INSERT INTO ratings(n_user_id, n_rating, n_recipe_id) VALUES ('{self.n_user_id}', '{n_recipe_id}', '{n_rating_value}');"
        self.db.write_sql2table(s_sql)
        return True

    def select_ingredients(self, n_recipe_id):
        # Checks if a given user-id exists in the DB
        s_sql = f" SELECT * FROM ingredients WHERE n_recipe_id = {n_recipe_id};"
        df = self.db.get_data_from_table("ingredients", b_full_table=False, s_query=s_sql)
        return df

    def check_user(self, user_id):
        # Checks if a given user-id exists in the DB
        s_sql = f" SELECT * FROM users WHERE n_user_id = {user_id};"
        df = self.db.get_data_from_table("users", b_full_table=False, s_query=s_sql)

        if df.empty:
            return False
        else:
            return True

    def add_user(self, s_username):

        # add user
        s_sql = f" INSERT INTO users(s_username) VALUES ('{s_username}') RETURNING n_user_id;"
        success, result = self.db.write_sql2table(s_sql)
        if success is not True:
            raise
        self.n_user_id = result[0][0]
        return self.n_user_id

    def add_item2stock(self, n_item_id, n_amount_in_stock):

        s_sql = f"SELECT s_unit_type FROM ingredients WHERE n_ingredient_id = {n_item_id}"
        df = self.db.get_data_from_table("ingredients", b_full_table=False, s_query=s_sql)

        s_unit_type = df.s_unit_type[0]

        s_sql = f" INSERT INTO pantry(n_user_id, n_item_id, s_unit_type, f_amount_in_stock) VALUES ('{self.n_user_id}','{n_item_id}', '{s_unit_type}', '{n_amount_in_stock}') RETURNING n_pantry_id;"
        success, result = self.db.write_sql2table(s_sql)
        if success is not True:
            raise
        return result[0][0]

    def get_all_items(self):
        df = self.db.get_data_from_table("items", b_full_table=True)
        return df

    def get_current_stock(self):
        s_sql = f"SELECT * FROM pantry WHERE n_user_id = {self.n_user_id};"
        df = self.db.get_data_from_table("pantry", b_full_table=False, s_query=s_sql)
        return df

    def get_all_recipe_ids(self):
        s_sql = f"SELECT DISTINCT n_recipe_id FROM recipes;"
        df = self.db.get_data_from_table("recipes", b_full_table=False, s_query=s_sql)
        return df

    def get_recipes(self, id_list):
        if len(id_list) != 0:
            s_sql = f"SELECT * FROM recipes where n_recipe_id in {tuple(id_list)};"
            df = self.db.get_data_from_table("recipes", b_full_table=False, s_query=s_sql)
            return df
        else:
            return pd.DataFrame()

    def reduce_stock(self, n_item_id, n_amount_to_reduce):
        s_sql = f"SELECT * FROM pantry WHERE n_item_id = {n_item_id} AND n_user_id = {self.n_user_id};"
        df = self.db.get_data_from_table("pantry", b_full_table=False, s_query=s_sql)
        print("Amount: ",df.f_amount_in_stock)
        if len(df.f_amount_in_stock) != 1:
            raise
        new_amount = df.f_amount_in_stock.to_list()[0] - float(n_amount_to_reduce)
        if new_amount <= 0:
            s_sql = f"DELETE FROM pantry WHERE n_item_id = {n_item_id} AND n_user_id = {self.n_user_id};"
            self.db.write_sql2table(s_sql)
        else:
            s_sql = f"UPDATE pantry SET f_amount_in_stock = {new_amount}  WHERE n_item_id = {n_item_id} AND n_user_id = {self.n_user_id};"
            self.db.write_sql2table(s_sql)

    def cook_meal(self, n_recipe_id):  # remove stock
        s_sql = f"SELECT * FROM ingredients WHERE n_recipe_id = {n_recipe_id};"
        df_needed_ingredients = self.db.get_data_from_table("ingredients", b_full_table=False, s_query=s_sql)

        # reduce every item in stock by amount needed in recipe,
        for ingredient, amount in zip(df_needed_ingredients.n_ingredient_id, df_needed_ingredients.f_amount_needed):
            self.reduce_stock(ingredient, amount)
        return True

    def _possible_recipes(self):
        candidates = list()
        my_stock = self.get_current_stock()
        recipe_ids = self.get_all_recipe_ids().n_recipe_id.to_list()
        for recipe_id in recipe_ids:
            s_sql = f"SELECT * FROM ingredients WHERE n_recipe_id = {recipe_id};"
            df_needed_ingredients = self.db.get_data_from_table("ingredients", b_full_table=False, s_query=s_sql)
            # check if in stock
            missing_items = list()
            found_items = list()
            for ingredient in df_needed_ingredients.n_ingredient_id.to_list():
                if ingredient in my_stock.n_item_id.to_list():
                    amount_needed = float(df_needed_ingredients.loc[df_needed_ingredients["n_ingredient_id"] == ingredient].f_amount_needed)
                    amount_available = float(my_stock.loc[my_stock["n_item_id"] == ingredient].f_amount_in_stock)
                    if amount_needed <= amount_available:
                        found_items.append(ingredient)
                    else:
                        logging.debug(f"Ingredient {ingredient} found but was not enough")
                        missing_items.append(ingredient)

                else:
                    missing_items.append(ingredient)
            if len(missing_items) > 0:
                logging.debug(f" Recipe {recipe_id} not possible to cook")
                logging.debug(f"missing {missing_items}")
                continue

            candidates.append(recipe_id)

        return candidates

    def meal_reco_without_pantry(self):
        s_sql = f"SELECT * FROM recos WHERE n_user_id = {self.n_user_id}"
        recos = self.db.get_data_from_table("recos", b_full_table=False, s_query=s_sql)
        return recos.sort_values(by="rating", ascending=False)

    def meal_reco_by_pantry(self):
        # Check available recipes
        candidates = self._possible_recipes()

        # Rank recipes
        ranked_recipes = self.reco.ranking(candidates, self.n_user_id)
        return ranked_recipes

    @staticmethod
    def usage():
        add_user = "cooky.add_user('Hans')"
        add_item = "cooky.add_item2stock(10, 1)"

        get_items = "cooky.get_all_items()"
        get_current_stock = "cooky.get_current_stock()"

        reduce_stock = "cooky.reduce_stock(1, 0.5)"
        cook_meal = "cooky.cook_meal(1)"

        meal_reco = "cooky.meal_reco_by_pantry()"
        meal_reco2 = "cooky.meal_reco_without_pantry()"

        msg = f"""

   _____            _          
  / ____|          | |         
 | |     ___   ___ | | ___   _ 
 | |    / _ \ / _ \| |/ / | | |
 | |___| (_) | (_) |   <| |_| |
  \_____\___/ \___/|_|\_\\__, |
                          __/ |
                         |___/ 

(c) 2022 - Seems-Inc.de

------ Example for callable functions ------
cooky = Cooky()

{add_user}
{add_item}

{get_items}
{get_current_stock}

{reduce_stock}
{cook_meal}
{meal_reco}
{meal_reco2}

"""
        logging.info(msg)
        return msg


if __name__ == "__main__":
    cooky = Cooky()
    cooky.usage()
    cooky.n_user_id = 8961
    for i in range(0, 150):
        try:
            cooky.add_item2stock(i, 10)
        except:
            logging.debug("Exception triggered")
            continue
    cooky.reduce_stock(1, 1)
    print(cooky.get_current_stock().head())

    # meals1 = cooky.meal_reco_by_pantry().to_dict()
    # print("meals1: ", meals1)
    # recipe_ids1 = meals1["n_recipe_id"].values()
    # recipes1 = cooky.get_recipes(recipe_ids1).to_json()
    # print("Reco by pantry:", recipes1)

    # meals2 = cooky.meal_reco_without_pantry().to_dict()
    # print("meals2: ", meals2)
    # recipe_ids2 = meals2["n_recipe_id"].values()
    # recipes2 = cooky.get_recipes(recipe_ids2).to_json()
    # print("Reco without pantry:", recipes2)

    #ERROR: cooky.cook_meal(meals.n_recipe_id.to_list()[0])
    cooky.add_rating(10, 2)
    pass
