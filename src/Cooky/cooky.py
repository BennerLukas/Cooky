from dataclasses import dataclass
import pandas as pd

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

    def add_item2stock(self, n_item_id, s_unit_type, n_amount_in_stock):
        s_sql = f" INSERT INTO pantry(n_user_id, n_item_id, s_unit_type, f_amount_in_stock) VALUES ('{self.n_user_id}', '{n_item_id}', '{s_unit_type}', '{n_amount_in_stock}') RETURNING n_pantry_id;"
        success, result = self.db.write_sql2table(s_sql)
        if success is not True:
            raise
        self.n_user_id = result[0][0]
        return self.n_user_id

    def get_current_stock(self):
        pass

    def cook_meal(self):
        pass

    def possible_recipes(self, s_user_input):
        candidates = list()

        return candidates

    def meal_reco(self, s_user_input=None):
        # Current User Input

        # Check available recipes
        candiates = self.possible_recipes(s_user_input)

        # Rank recipes
        reco = Recommender()
        ranked_recipes = reco.ranking(candiates)
        return ranked_recipes


if __name__ == "__main__":
    cooky = Cooky()
    cooky.add_user("Hans")
    cooky.add_item2stock(1, "kg", 1)
