from crypt import methods
import string
from flask import Flask, jsonify, request
from torch import randint
from cooky import Cooky

app = Flask(__name__)

cooky = Cooky(init_db=False)

# Explore Page Functions
"""
- Load all recommended stuff: List of Dicts

Functions:
- get_all_recipe_ids()
- meal_reco_without_pantry: db excerpt
- meal_reco_by_pantr: ranked recipes
"""

@app.route("/explore/", methods=["GET"])
def explore():

    if request.args.get('reco') == "pantry":
        meals = cooky.meal_reco_by_pantry().to_dict()
        recipe_ids = meals["n_recipe_id"].values()
        recipes = cooky.get_recipes(recipe_ids).to_json()
        

        cards = []
        for i in recipes["n_recipe_id"]:
          cards.append(
            {
              "id":i,
              "title":recipes["n_recipe_id"][i],
              "ingredients":recipes["array_ingredients"][i],
              "directions":recipes["s_directions"][i],
              "entities":recipes["array_NER"][i],
              "flex":7,
              "src": "https://cdn.vuetifyjs.com/images/cards/house.jpg"
            }
          )


        return cards, 200


    elif request.args.get('reco') == "all":
        meals = cooky.meal_reco_without_pantry().to_dict()
        recipe_ids = meals["n_recipe_id"].values()
        recipes = cooky.get_recipes(recipe_ids).to_json()


        cards = []
        for i in recipes["n_recipe_id"]:
          cards.append(
            {
              "id":i,
              "title":recipes["n_recipe_id"][i],
              "ingredients":recipes["array_ingredients"][i],
              "directions":recipes["s_directions"][i],
              "entities":recipes["array_NER"][i],
              "flex":7,
              "src": "https://cdn.vuetifyjs.com/images/cards/house.jpg"
            }
          )


        return cards, 200

    else:
        return "error", 500

# Detail Page Functions
"""
- On Click, load Details
- Bing API Call for Image

Functions:
- add_rating(user_id, recipe_id, rating_value): True
- cook_meal(recipe_id): True #reduces stock according to meal

"""

# Search Page
"""
- Query DB for Dish Name and return details as well

Functions:

- get_all_recipe_ids(): IDs of recipes
- _possible_recipes(): list of recipes #probably support function, do not use directly
"""

# Settings Page Functions
"""
- Change User View

Functions:
- add_user(username): user_id #Note: this creates a new user, to choose a user, use variable self.n_user_id
"""


@app.route("/login", methods=["POST"]) # Sensitive data, hence POST
def login():
    if request.method == 'POST':
        # Read Request
        # {
        #     "username": 1,
        #     "password": 1
        # }
        data = request.json
        user_id = data["username"]
        password = data["password"]

        # Check validity
        if cooky.check_user(user_id):
          cooky.n_user_id = user_id
          return jsonify({"session":user_id}), 200
        else:
          return "not found", 404


# Pantry Page Functions
"""
- CRUD Pantry items
- U equals D/C

Functions:
- add_item2stock(item id, amount)
- get_all_items() #shows all available items
- get_current_stock()
- reduce_stock(item_id,amount_to_reduce)
"""

if __name__ == "__main__":
    app.run(debug=True)
