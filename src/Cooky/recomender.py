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
        self.model = None

        self.train_als()
        self.reco_als()

    def ranking(self, candidate_recipes, n_user_id):
        s_sql = f"SELECT * FROM recos WHERE n_user_id = {n_user_id}"
        reco_recipes = self.db.get_data_from_table("recos", b_full_table=False, s_query=s_sql)
        if reco_recipes.count()[0] == 0:
            return False
        reco_recipes_list = reco_recipes.n_recipe_id.to_list()

        matches = list(set(candidate_recipes) & set(reco_recipes_list))
        result = reco_recipes.loc[reco_recipes["n_recipe_id"].isin(matches)].sort_values(by="rating", ascending=False)
        return result

    def create_spark_session(self):
        # self.spark = pyspark.sql.SparkSession.builder.appName("Cooky").getOrCreate()
        os.environ["HADOOP_HOME"] = r"C:\Users\lukas\spark-3.3.0-bin-hadoop3"
        os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jre1.8.0_333"
        os.environ["PYSPARK_PYTHON"] = "python"

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
            maxIter=10,
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
        eval = RegressionEvaluator(metricName="rmse", labelCol="n_rating", predictionCol="prediction")
        rmse = eval.evaluate(pred)

        print(rmse)

        # model.write().overwrite().save("../data/model")
        self.model = model
        return model

    def reco_als(self, n_recos=10):
        if self.model is None:
            raise
        # user_recos = model.recommendForUserSubset(user_dataset, n_recos)
        user_recos = self.model.recommendForAllUsers(n_recos)

        user_recos_exploded = user_recos.withColumn("reco", F.explode("recommendations")).select("n_user_id", F.col(
            "reco.n_recipe_id"), F.col("reco.rating"))
        user_recos_exploded = user_recos_exploded.where(F.col("rating") > 0)

        df_user_recos_exploded = user_recos_exploded.toPandas()
        self.db.write_df2table(df_user_recos_exploded, "recos", mode="replace")
        return df_user_recos_exploded
