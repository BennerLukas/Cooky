<template>
  <div class="search">
    <v-text-field
          class="pa-3"
          outlined
          hide-details
          clearable
          label="Search Dish"
          append-icon="mdi-magnify"
        ></v-text-field>

  <v-card
    class="mx-auto my-12 "
    max-width="374"
  >
    <v-card-title>{{detail.title}}</v-card-title>

    <v-card-text>
      <v-row
        align="center"
        class="mx-0"
      >
        <v-rating
          :value="4.5"
          color="amber"
          dense
          half-increments
          readonly
          size="14"
        ></v-rating>

        <div class="grey--text ms-4">
          4.5 (413)
        </div>
      </v-row>

      <div class="my-4 text-subtitle-1">
        {{detail.recipe}}
      </div>

      <div>{{detail.description}}</div>
    </v-card-text>
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

  export default {
    name: 'Search',
    
    components: {},

    data() {
      return {
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
        detail: {
          title: 'Dish Title', src: 'https://cdn.vuetifyjs.com/images/cards/train.jpg', description: 'Description for this dish', recipe: 'Recipe for this dish', rating: 5}
      }
    },

    methods: {
      itemClick(id) {
        this.dialog = true
        this.detail.title = this.cards.filter(dish => dish.id === id)[0].title //sample of changing titles
        console.log(this.detail.title)
        //fetch description and recipe from db to present
        // update detail object
        //this.detail = {fetched object}
      }
    }
  }
</script>
