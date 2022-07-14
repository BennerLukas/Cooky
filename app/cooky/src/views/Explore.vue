<template>
  <div class="explore pa-6">
    <h1>Explore</h1>
    


    <v-container 
      fluid>
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

    <!-- Popup for detailed view -->
    <v-dialog
      v-model="dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >

      <v-card>
          
        <v-toolbar dark color="primary">

          <!-- close detailed view -->
          <v-btn icon dark @click="dialog = false">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>


          <v-toolbar-title>{{detail.title}}</v-toolbar-title>

        
        </v-toolbar>
        <v-list three-line subheader>
          <v-subheader>User Controls</v-subheader>
          
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Description</v-list-item-title>
              <v-list-item-subtitle>{{detail.description}}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

                  <v-btn @click.stop="test()">
          Open Dialog
        </v-btn>
          
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
    name: 'Explore',
    
    components: {},

    data() {
      return {
        dialog: false,
        cards: [
          { id: 1, title: 'Pre-fab homes', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 6 },//card image can be generated from bing in backend
          { id: 2, title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 6 },
          { id: 3, title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 7 },
          { id: 4, title: 'Train', src: 'https://cdn.vuetifyjs.com/images/cards/train.jpg', flex: 5 },
          { id: 5, title: 'Pre-fab homes', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 6 },
          { id: 6, title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 6 },
          { id: 7, title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 7 },
          { id: 8, title: 'Train', src: 'https://cdn.vuetifyjs.com/images/cards/train.jpg', flex: 5 }
        ],//dynamically create cards by loading from API
        detail: {
          title: 'Dish Title', src: 'https://cdn.vuetifyjs.com/images/cards/train.jpg', description: 'Description for this dish', recipe: 'Recipe for this dish', rating: 5}
      }
    },

    methods: {
      itemClick(id) {
        console.log(id)
        this.dialog = true
        //fetch description and recipe from db to present
        // update detail object
        //this.detail = {fetched object}
      }
    }
  }
</script>
