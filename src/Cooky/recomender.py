import pandas as pd
import matplotlib.pyplot as plt


class Recommender:

    def __init__(self, db):
        self.db = db

    def ranking(self, candidate_recipes):
        sorted_candidates = candidate_recipes
        # TODO
        return sorted_candidates

    def generate_synthetic_user_data(self):
        df_recipes = self.db.get_data_from_table("recipes", b_full_table=True)
        max_recipe_id = df_recipes.n_recipe_id.max()

        df = pd.read_csv("./data/BX-Book-Ratings.csv", sep=";", encoding='CP1252', escapechar='\\')
        df = df[df["Book-Rating"] != 0]

        df_lookup = pd.DataFrame(df.ISBN.unique(), columns=["ISBN"])
        df_lookup["n_recipe_id"] = df_lookup.index
        df_lookup = df_lookup.where(df_lookup["n_recipe_id"] <= max_recipe_id)

        df_joined = df.merge(df_lookup, on="ISBN", how="inner")

        df_final = df_joined.drop(columns=["ISBN"]).rename({
            "User-ID": "user_id",
            "Book-Rating": "rating",
        })

        self.db.write_df2table(df_final, "ratings")

        # write users to db
        df_users = pd.DataFrame(df["User-ID"].unique(), columns=["n_user_id"])
        df_users["s_username"] = "synth-user"
        self.db.write_df2table(df_users[["n_user_id", "s_username"]], "users")

        return True


if __name__ == "__main__":
    from database import DataBase
    obj = Recommender(DataBase())
    obj.generate_synthetic_user_data()
