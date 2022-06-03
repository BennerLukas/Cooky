from dataclasses import dataclass
from database_init import DataBase
from recomender import Recommender
@dataclass
class Cooky:

    def __init__(self):
        self.db = DataBase()
        self.n_user_id = "Peter"
        self.n_pantry_id = 1
        self.n_recipe_id = 1

    def _get_data(self, table_name):
        pass

    def _write_data(self, df, table_name, mode="append"):
        pass

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