<template>
  <div class="explore">
    
<v-card>
    <v-tabs
      v-model="tab"
      background-color="transparent"
      grow
    >
    <v-tab key="Tab1"
    @click="process_all_reco(0)">
        All
      </v-tab>

    <v-tab key="Tab2"
    @click="process_all_reco(1)">
        Pantry
      </v-tab>

    </v-tabs>

<!-- Tab Contents -->
    <v-tabs-items v-model="tab">

    <!-- Tab One Content -->
      <v-tab-item key="Tab1">
        
      <!-- Boxed View of Dishes -->
      <v-container 
        fluid>
        <p class="text-h5 text--primary"> Based on your preference</p>
        <v-row 
          dense>
          <v-col
            v-for="card in cards"
            :key="card.id"
            :cols="card.flex"
          >
            <v-card
              @click="itemClick(card.id)">
              <v-img
                :src="card.src"
                class="white--text align-end"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                height="200px"
                lazy-src
              >
                <v-card-title v-text="card.title"></v-card-title>
              </v-img>

            </v-card>
          </v-col>
        </v-row>
      </v-container>

      </v-tab-item>

<!-- Tab Two Content -->
      <v-tab-item key="Tab2">


      
      <!-- Boxed View of Dishes -->
      <v-container 
        fluid>
        <p class="text-h5 text--primary"> Based on your pantry </p>
        <v-row 
          dense>
          <v-col
            v-for="card in cards"
            :key="card.id"
            :cols="card.flex"
          >
            <v-card
              @click="itemClick(card.id)">
              <v-img
                :src="card.src"
                class="white--text align-end"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                height="200px"
                lazy-src
              >
                <v-card-title v-text="card.title"></v-card-title>
              </v-img>

            </v-card>
          </v-col>
        </v-row>
      </v-container>

      </v-tab-item>

    </v-tabs-items>
    
  </v-card>


    <!-- Popup for detailed view -->
    <v-dialog
      v-model="dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >

      <v-card>
          


        <v-img
              :src="detail.src"
              class="white--text"
              gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
              lazy-src
            >

              

              <v-app-bar
                  flat
                  color="rgba(0, 0, 0, 0)"
                >
                  <!-- close detailed view -->
                  <v-btn icon dark @click="dialog = false" >
                    <v-icon>mdi-arrow-left</v-icon>
                  </v-btn>





                  
              </v-app-bar>

              <v-card-title>
                <h1>{{detail.title}}</h1>
              </v-card-title>

              <v-btn
                  class="ma-2"
                  outlined
                  color="white"
                  @click="cookDish(detail.id)"
                  v-if="tab"
                  >Cook This Dish</v-btn>

              
              <v-rating
                hover
                background-color="grey"
                color="white"
                empty-icon="mdi-star-outline"
                full-icon="mdi-star"
                half-icon="mdi-star-half-full"
                length="5"
                size="30"
                :value=detail.rating
              ></v-rating>

              </v-img>

        <v-list three-line>
          

          
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Ingredients</v-list-item-title>
              <v-list-item-subtitle
              v-for="ingredient in detail.ingredients.replace('[','').replace(']','').replace(/&quot;/g, '').split(',')">
              {{ingredient}}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Directions</v-list-item-title>
              <v-list-item-subtitle
              v-for="direction in detail.directions.replace('[','').replace(']','').replace(/&quot;/g, '').split(',')">
              {{direction}}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

        </v-list>

      </v-card>

    </v-dialog>

    <!-- Snackbar on Success -->
    <v-snackbar
      v-model="on_success.snackbar"
      :timeout="on_success.timeout"
    >
      {{ on_success.text }}


        <v-btn
          color="blue"
          text
          @click="on_success.snackbar = false"
        >
          Close
        </v-btn>

    </v-snackbar>

</div>
</template>

<script>
import axios from 'axios'
import VueCookies from 'vue-cookies'

  export default {
    name: 'Explore',
    
    components: {},

    data() {
      return {
        tab: null,
        dialog: false,
        all_reco: {},
        pantry_reco: {},
        cards: [],//dynamically create cards by loading from API
        response_cooky: {"n_recipe_id":{},"s_recipe_title":{},"array_ingredients":{},"s_directions":{},"s_link":{},"s_source":{},"array_NER":{}},//response json -> has all information needed for detail page as well

        detail: {
        id: 0, title: 'Dish Title', src: 'https://cdn.vuetifyjs.com/images/cards/train.jpg', directions: 'Description for this dish', ingredients: 'Recipe for this dish', rating: 5},
        on_success: {
          snackbar: false,
          text: "",
          timeout: 2000,
        } 
      }
    },

    methods: {
      onload() {
        //TODO: Check if session ID, else redirect
          var session = VueCookies.isKey("session")
          if (session) {
            // fetch session
            let session_id = VueCookies.get("session")

            // load recommendations
            this.loadRecommedations(session_id)

          } else {
            this.$router.push('settings') 
          }

      },
      loadRecommedations(session_id) {
        axios.get('http://localhost:5000/explore?session='+session_id)
            .then(response => {
              if (response.status == 200) {
                this.all_reco = response.data["all"]
                this.pantry_reco = response.data["pantry"]

                this.process_all_reco(0)
              }
            })
            .catch(error => console.log(error))
      },
      process_all_reco(reco_type) {
          if (reco_type == 0) {
            var recommendation = this.all_reco
          } else {
            var recommendation = this.pantry_reco
          }
          this.cards = []
          let flex_val = [6,6,5,7]


          // images are hard coded as to not expose any API keys. We recommend using the Bing Image Search Api with the recipe title as an input. Take any of the returned URLs as a showcase image.
          var session = VueCookies.isKey("session")
          if (session == 99) {
          var images = [
            "https://cdn.pixabay.com/photo/2022/07/01/13/31/salad-dressing-7295630_960_720.jpg",
            "https://cdn.pixabay.com/photo/2016/07/12/08/12/oatmeal-raisin-cookies-1511599_960_720.jpg",
            "https://cdn.pixabay.com/photo/2015/12/08/19/08/steak-1083567_960_720.jpg",
            "https://cdn.pixabay.com/photo/2015/07/26/21/39/deviled-eggs-861773_960_720.jpg",
            "https://cdn.pixabay.com/photo/2020/01/17/10/18/meat-loaf-4772659_960_720.jpg",
            "https://cdn.pixabay.com/photo/2011/03/30/10/28/apple-pie-6007_960_720.jpg",
            "https://cdn.pixabay.com/photo/2019/11/07/13/05/waffle-4608843_960_720.jpg",
            "https://cdn.pixabay.com/photo/2014/04/14/20/45/scalloped-324243_960_720.jpg",
            "https://cdn.pixabay.com/photo/2016/10/25/13/43/stollen-1768907_960_720.jpg",
            "https://cdn.pixabay.com/photo/2020/03/09/17/11/macaroni-4916444_960_720.jpg",
            "https://cdn.pixabay.com/photo/2016/02/05/15/34/pasta-1181189_960_720.jpg"
          ]  
          } else {
          var images = [
            "https://cdn.pixabay.com/photo/2016/01/26/00/53/potatoe-1161819_960_720.jpg",
            "https://cdn.pixabay.com/photo/2016/04/23/23/19/beef-1348517_960_720.jpg",
            "https://cdn.pixabay.com/photo/2021/04/01/11/50/asparagus-6141991_960_720.jpg",
            "https://cdn.pixabay.com/photo/2019/08/15/10/46/deep-fried-4407741_960_720.jpg",
            "https://cdn.pixabay.com/photo/2015/04/24/20/04/corn-bread-738244_960_720.jpg",
            "https://cdn.pixabay.com/photo/2014/05/23/23/17/dessert-352475_960_720.jpg",
            "https://cdn.pixabay.com/photo/2020/09/16/06/54/cookies-5575588_960_720.jpg",
            "https://cdn.pixabay.com/photo/2010/12/13/10/13/chocolate-2554_960_720.jpg",
            "https://cdn.pixabay.com/photo/2016/11/06/23/24/broccoli-1804446_960_720.jpg",
            "https://cdn.pixabay.com/photo/2016/11/18/17/42/barbecue-1836053_960_720.jpg",
            "https://cdn.pixabay.com/photo/2016/11/18/17/42/barbecue-1836053_960_720.jpg"
          ]
          }
          
          if (Object.values(recommendation).length != 0) {
            for (let index = 0; index < Object.values(recommendation.n_recipe_id).length; index++) {
              let card = { id: recommendation.n_recipe_id[index],
              title: recommendation.s_recipe_title[index],
              src: images[index%10],
              flex: flex_val[index%4],
              ingredients:recommendation.array_NER[index],
              directions:recommendation.s_directions[index]}
              this.cards.push(card)
            } 
          }
      },
      async itemClick(id) {
        let session_id = VueCookies.get("session")
        await axios.get('http://localhost:5000/explore/rating?session='+session_id+'&recipe_id='+id)
            .then(response => {
              if (response.status == 200) {
                this.detail.rating = response.data['rating']/2
                console.log(this.detail.rating)
              }
            })

        this.dialog = true
        this.detail.id = id
        this.detail.title = this.cards.filter(dish => dish.id === id)[0].title 
        this.detail.src = this.cards.filter(dish => dish.id === id)[0].src 
        this.detail.directions = this.cards.filter(dish => dish.id === id)[0].directions 
        this.detail.ingredients = this.cards.filter(dish => dish.id === id)[0].ingredients 

        //fetch description and recipe from db to present
        // update detail object
        //this.detail = {fetched object}
      },
      cookDish(n_recipe_id) {
        console.log("cooking")

        let session_id = VueCookies.get("session")

        axios.get('http://localhost:5000/pantry/cook?session='+session_id+'&recipe_id='+n_recipe_id)
            .then(response => {
              if (response.status == 202) {
                this.on_success.text = "Items deducted from pantry. Enjoy!"
                this.on_success.snackbar = true
              }
            })
            .catch(error => console.log(error)
            )
      }
    },
    beforeMount(){
    this.onload()
    }
  }

// cooky_response = getExploreData()
// this.cards = cooky_response
</script>
