from dataclasses import dataclass

import pandas as pd

from database import DataBase
from recomender import Recommender


@dataclass
class Cooky:

    def __init__(self):
        self.db = DataBase()
        self.n_user_id = None
        self.n_pantry_id = 1
        self.n_recipe_id = 1

    def add_user(self, s_username):
        s_sql = f" INSERT INTO users(s_username) VALUES ('{s_username}');"
        success, result = self.db.write_sql2table(s_sql)
        if success is not True:
            raise


    def add_item2stock(self):
        pass

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
