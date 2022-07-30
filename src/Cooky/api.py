from crypt import methods
import string
from flask import Flask, jsonify, request
from sqlalchemy import all_
from torch import randint
from cooky import Cooky
from recommender import Recommender
from flask_cors import CORS, cross_origin


print(
'''
   _____            _          
  / ____|          | |         
 | |     ___   ___ | | ___   _ 
 | |    / _ \ / _ \| |/ / | | |
 | |___| (_) | (_) |   <| |_| |
  \_____\___/ \___/|_|\_\\__, |
                          __/ |
                         |___/ 

(c) 2022 - Seems-Inc.de
'''

)


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

cooky = Cooky(init_db=False)

# Explore Page Functions
"""
- Load all recommended stuff: List of Dicts

Functions:
- get_all_recipe_ids()
- meal_reco_without_pantry: db excerpt
- meal_reco_by_pantr: ranked recipes

"""


# @app.route("/reco", methods=["GET"])
# def loadReco():
#   cooky.reco = Recommender(cooky.db, True)
#   return "success", 200

@app.route("/explore", methods=["GET"])
def explore():
  session = request.args.get('session', None)
  pantry = int(request.args.get('pantry', 0))
  # sync session
  cooky.n_user_id = session
  # meals = cooky.meal_reco_without_pantry().to_dict()


  # Without Pantry Recommendation
  all_rec = cooky.meal_reco_without_pantry()
  # print(all_rec.n_recipe_id.to_list())
  all_recipes = cooky.get_recipes(all_rec.n_recipe_id.to_list())

  #  Intuition: only the recipes that are already being recommended should be considered for recommendation by pantry
  # For this, there is no need to go through all meals to get the candidates
  # instead, we pass a list of possible recipes and check only for those, this should reduce the load on the database and improve performance as well
  potential_candidates = all_recipes.n_recipe_id.to_list()

  # With Pantry Recommendation
  pantry_rec = cooky.meal_reco_by_pantry(potential_candidates)
  # print(pantry_rec.n_recipe_id.to_list())
  pantry_recipes = cooky.get_recipes(pantry_rec.n_recipe_id.to_list())
  
  return jsonify({"all":all_recipes.to_dict(),"pantry":pantry_recipes.to_dict()}), 200

@app.route("/explore/ingredients", methods=["GET"])
def fetchIngredients():
  session = request.args.get('session', None)
  recipe_id = request.args.get('recipe_id', None)
  ingredients = cooky.select_ingredients(recipe_id)
  return ingredients.to_json(), 200

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

@app.route("/pantry", methods=["GET"])
def loadPantry():
  # [
  #         {
  #           id: 1,
  #           title: "item1",
  #           qty: 111
  #         },
  #         {
  #           id: 3,
  #           title: "item3",
  #           qty: 3
  #         }
  #       ]


  session = request.args.get('session', None)

  # sync session
  cooky.n_user_id = session  

  # fetch items
  pantry_items = cooky.get_current_stock().to_dict()
  all_items = cooky.get_all_items().to_dict()
  
  # return items
  return {'all':all_items, 'pantry':pantry_items}, 200

@app.route("/pantry/delete", methods=["DELETE"])
def deleteItem():
  session = request.args.get('session', None)
  item_id = request.args.get('item_id', None)
  item_qty = request.args.get('item_qty', None)

  # sync session
  cooky.n_user_id = session

  # Delete
  cooky.reduce_stock(item_id, item_qty)

  return 'success', 202

@app.route("/pantry/add", methods=["GET"])
def addItem():
  session = request.args.get('session', None)
  item_id = request.args.get('item_id', None)
  item_qty = request.args.get('item_qty', None)

  # sync session
  cooky.n_user_id = session

  # add item
  cooky.add_item2stock(item_id, item_qty)

  return 'success', 202

@app.route("/pantry/cook", methods=["GET"])
def cookDish():
  session = request.args.get('session', None)
  n_recipe_id = request.args.get('recipe_id', None)

  # sync session
  cooky.n_user_id = session

  # add item
  cooky.cook_meal(n_recipe_id)

  return 'success', 202


@app.route("/explore/rating", methods=["GET"])
def getRating():
  session = request.args.get('session', None)
  n_recipe_id = request.args.get('recipe_id', None)

  # sync session
  cooky.n_user_id = session

  # get rating
  rating = cooky.get_avg_rating(n_recipe_id).avg[0]
  if rating == False:
    rating = float(0)
  return jsonify({"rating":rating}), 200

if __name__ == "__main__":
    app.run(debug=True)
