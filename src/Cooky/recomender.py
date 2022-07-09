import pandas as pd
import matplotlib.pyplot as plt
import pyspark


class Recommender:

    def __init__(self, db):
        self.db = db
        self.spark = None

    def ranking(self, candidate_recipes):
        sorted_candidates = candidate_recipes
        # TODO
        return sorted_candidates

    def generate_synthetic_user_data(self):
        df_recipes = self.db.get_data_from_table("recipes", b_full_table=True)
        max_recipe_id = df_recipes.n_recipe_id.max()

        df = pd.read_csv("../data/BX-Book-Ratings.csv", sep=";", encoding='CP1252', escapechar='\\')
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

        self.db.write_df2table(df_final, "ratings")

        # write users to db
        df_users = pd.DataFrame(df["User-ID"].unique(), columns=["n_user_id"])
        df_users["s_username"] = "synth-user"
        df_users = df_users.set_index("n_user_id")
        self.db.write_df2table(df_users, "users")

        return True

    def create_spark_session(self):
        self.spark = pyspark.sql.SparkSession.builder.appName("Cooky").getOrCreate()
        return self.spark

    def calc_als(self):
        df = self.db.get_data_from_table("ratings", b_full_table=True)

        s_sql = "SELECT DISTINCT n_recipe_id FROM recipes"
        recipes = self.db.get_data_from_table("recipes", b_full_table=False, s_query=s_sql)  # aka items

        s_sql = "SELECT DISTINCT n_user_id FROM users"
        users = self.db.get_data_from_table("users", b_full_table=False, s_query=s_sql)

        # convert to pyspark
        pdf_ratings = self.spark.createDataFrame(df)
        pdf_recipes = self.spark.createDataFrame(recipes)
        pdf_users = self.spark.createDataFrame(users)

        pass


if __name__ == "__main__":
    from database import DataBase

    obj = Recommender(DataBase())
    # obj.generate_synthetic_user_data()
    obj.calc_recos()
