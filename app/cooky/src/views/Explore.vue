<template>
  <div class="explore">
    
<v-card>
    <v-tabs
      v-model="tab"
      background-color="transparent"
      grow
    >
    <v-tab key="Tab1">
        Pantry
      </v-tab>

    <v-tab key="Tab2">
        All
      </v-tab>

    </v-tabs>

<!-- Tab Contents -->
    <v-tabs-items v-model="tab">
    <!-- Tab One Content -->
      <v-tab-item key="Tab1">


      
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

    <!-- Tab Two Content -->
      <v-tab-item key="Tab2">
        
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
              :src="cards[0].src"
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


                  <v-spacer></v-spacer>

                  <v-btn color="white" icon>
                    <v-icon>mdi-dots-vertical</v-icon>
                  </v-btn>
                  
              </v-app-bar>

              <v-card-title>
                <h1>{{detail.title}}</h1>
              </v-card-title>
          </v-img>


        <v-list three-line>
          
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Description</v-list-item-title>
              <v-list-item-subtitle>{{detail.description}}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Recipe</v-list-item-title>
              <v-list-item-subtitle>{{detail.recipe}}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        
        </v-list>

      </v-card>

    </v-dialog>



</div>
</template>

<script>
import axios from 'axios'

async function getExploreData() {
	try {
		const response = await axios.get("http://localhost:5000/explore?reco=pantry");
		console.log(response);
    return response;
	}
	catch (error) {
		console.log(error);
	}
}

  export default {
    name: 'Explore',
    
    components: {},

    data() {
      return {
        tab: null,
        dialog: false,
        cards: [
          { id: 1, title: 'Pre-fab homes', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 6 },//card image can be generated from bing in backend
          { id: 2, title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 6 },
          { id: 3, title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 7 },
          { id: 4, title: 'Train', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 5 },
          { id: 5, title: 'Pre-fab homes', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 6 },
          { id: 6, title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 6 },
          { id: 7, title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 7 },
          { id: 8, title: 'Train', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 5 }
        ],//dynamically create cards by loading from API
        response_cooky: {"n_recipe_id":{},"s_recipe_title":{},"array_ingredients":{},"s_directions":{},"s_link":{},"s_source":{},"array_NER":{}},//response json -> has all information needed for detail page as well

        detail: {
          title: 'Dish Title', src: 'https://cdn.vuetifyjs.com/images/cards/train.jpg', description: 'Description for this dish', recipe: 'Recipe for this dish', rating: 5}
      }
    },

    methods: {
      itemClick(id) {
        this.dialog = true
        this.detail.title = this.cards.filter(dish => dish.id === id)[0].title //sample of changing titles
        this.detail.src = this.cards.filter(dish => dish.id === id)[0].src //sample of changing titles
        this.detail.description = this.cards.filter(dish => dish.id === id)[0].directions //sample of changing titles
        this.detail.recipe = this.cards.filter(dish => dish.id === id)[0].recipe //sample of changing titles
        //fetch description and recipe from db to present
        // update detail object
        //this.detail = {fetched object}
      }
    }
  }

cooky_response = getExploreData()
this.cards = cooky_response
</script>
