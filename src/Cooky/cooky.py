from dataclasses import dataclass
import pandas as pd
import logging
logging.basicConfig(level=logging.DEBUG)

from database import DataBase
from recomender import Recommender


@dataclass
class Cooky:

    def __init__(self):
        self.db = DataBase()
        self.n_user_id = None

    def add_user(self, s_username):

        # add user
        s_sql = f" INSERT INTO users(s_username) VALUES ('{s_username}') RETURNING n_user_id;"
        success, result = self.db.write_sql2table(s_sql)
        if success is not True:
            raise
        self.n_user_id = result[0][0]
        return self.n_user_id

    def add_item2stock(self, n_item_id, n_amount_in_stock):
        # TODO get unit_type from item table
        s_sql = f"SELECT s_unit_type FROM ingredients WHERE n_ingredient_id = {n_item_id}"
        df = self.db.get_data_from_table("ingredients", b_full_table=False, s_query=s_sql)

        s_unit_type = df.s_unit_type[0]

        s_sql = f" INSERT INTO pantry(n_user_id, n_item_id, s_unit_type, f_amount_in_stock) VALUES ('{self.n_user_id}','{n_item_id}', '{s_unit_type}', '{n_amount_in_stock}') RETURNING n_pantry_id;"
        success, result = self.db.write_sql2table(s_sql)
        if success is not True:
            raise
        return result[0][0]

    def get_current_stock(self):
        s_sql = f"SELECT * FROM pantry WHERE n_user_id = {self.n_user_id};"
        df = self.db.get_data_from_table("pantry", b_full_table=False, s_query=s_sql)
        return df

    def get_all_recipe_ids(self):
        s_sql = f"SELECT DISTINCT n_recipe_id FROM recipes;"
        df = self.db.get_data_from_table("recipes", b_full_table=False, s_query=s_sql)
        return df

    def reduce_stock(self, n_item_id, n_amount_needed):
        s_sql = f"SELECT * FROM pantry WHERE n_item_id = {n_item_id} AND n_user_id = {self.n_user_id};"
        df = self.db.get_data_from_table("pantry", b_full_table=False, s_query=s_sql)
        if len(df.f_amount_in_stock) != 1:
            raise
        new_amount = df.f_amount_in_stock.to_list()[0] - n_amount_needed
        if new_amount < 0:
            new_amount = 0

        s_sql = f"UPDATE pantry SET f_amount_in_stock = {new_amount}  WHERE n_item_id = {n_item_id} AND n_user_id = {self.n_user_id};"
        self.db.write_sql2table(s_sql)

    def cook_meal(self, n_recipe_id):    # remove stock
        s_sql = f"SELECT * FROM ingredients WHERE n_recipe_id = {n_recipe_id};"
        df_needed_ingredients = self.db.get_data_from_table("ingredients", b_full_table=False, s_query=s_sql)

        # reduce every item in stock by amount needed in recipe,
        for ingredient, amount in zip(df_needed_ingredients.n_ingredient_id, df_needed_ingredients.f_amount_needed):
            self.reduce_stock(ingredient, amount)
        return True

    def _possible_recipes(self):
        candidates = list()
        my_stock = self.get_current_stock().n_item_id.to_list()
        recipe_ids = self.get_all_recipe_ids().n_recipe_id.to_list()
        for recipe_id in recipe_ids:
            s_sql = f"SELECT * FROM ingredients WHERE n_recipe_id = {recipe_id};"
            df_needed_ingredients = self.db.get_data_from_table("ingredients", b_full_table=False, s_query=s_sql)

            # check if in stock
            missing_items = list()
            found_items = list()
            for ingredient in df_needed_ingredients.n_ingredient_id.to_list():
                if ingredient in my_stock:
                    found_items.append(ingredient)
                else:
                    missing_items.append(ingredient)
            if len(missing_items) > 0:
                logging.debug(f" Recipe {recipe_id} not possible to cook")
                logging.debug(f"missing {missing_items}")
                continue

            candidates.append(recipe_id)

        return candidates

    def meal_reco(self):      # TODO MAKI, MAVI
        # Current User Input

        # Check available recipes
        candidates = self._possible_recipes()

        # Rank recipes
        reco = Recommender()
        ranked_recipes = reco.ranking(candidates)
        return ranked_recipes


if __name__ == "__main__":
    cooky = Cooky()
    cooky.add_user("Hans")
    for i in range(0, 70):
        try:
            cooky.add_item2stock(i, 1)
        except:
            continue
    cooky.reduce_stock(1, 1)
    print(cooky.get_current_stock().head())
    meals = cooky.meal_reco()

    cooky.cook_meal(meals[0])
    pass