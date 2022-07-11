import pandas as pd
import matplotlib.pyplot as plt
import pyspark
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import functions as F
import os


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
        # self.spark = pyspark.sql.SparkSession.builder.appName("Cooky").getOrCreate()
        os.environ["HADOOP_HOME"] = "C:/tmp"

        # .master("spark://localhost:7077") \

        self.spark = pyspark.sql.SparkSession \
            .builder \
            .appName("Cooky") \
            .getOrCreate()
        sc = self.spark.sparkContext

        return self.spark

    def train_als(self):
        self.create_spark_session()

        df = self.db.get_data_from_table("ratings", b_full_table=True)

        # convert to pyspark
        pdf_ratings = self.spark.createDataFrame(df)

        (train, test) = pdf_ratings.randomSplit([0.7, 0.3], seed=123)

        als = ALS(
            rank=10,
            maxIter=5,
            regParam=0.01,
            alpha=1,
            userCol="n_user_id",
            itemCol="n_recipe_id",
            ratingCol="n_rating",
            coldStartStrategy="drop",
            nonnegative=True,
            implicitPrefs=False,
            seed=123
        )

        model = als.fit(train)

        pred = model.transform(test)
        eval = RegressionEvaluator(metricName="RMSE", labelCol="n_rating", predictionCol="prediction")
        rmse = eval.evaluate(pred)

        print(rmse)

        model.write().overwrite().save("../data/model/als_v1")
        return model

    def reco_als(self, model: ALSModel, user_dataset, n_recos=3):
        user_recos = model.recommendForUserSubset(user_dataset, n_recos)
        return user_recos


if __name__ == "__main__":
    from database import DataBase

    obj = Recommender(DataBase(False))
    # obj.generate_synthetic_user_data()
    obj.train_als()
