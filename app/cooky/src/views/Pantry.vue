<template>
  <div class="pantry pa-6">
    <v-list
      two-line
      flat
    >
      <h1>Pantry</h1>


      <v-row>
        <v-col
          cols="8"
        >
        <!-- Dropdown item -->
        <v-select
          v-model="selectedItem"
          :items="Object.values(all_items.s_ingredient)"
          label="Outlined style"
          outlined
        ></v-select>
        </v-col>

        <v-col
          cols="4"
        >
        <!-- Dropdown QTY -->
        <v-text-field
        v-model.number="qty"
        @click:append="addItem"
        @keyup.enter="addItem"
          outlined
          hide-details
          label="QTY"
          append-icon="mdi-plus"
          type="number"
        ></v-text-field>
        </v-col>
      </v-row>

<!-- <v-text-field
        v-model="newItemName"
        @click:append="addItem"
        @keyup.enter="addItem"
          class="pa-3"
          outlined
          hide-details
          clearable
          label="Add Item"
          append-icon="mdi-plus"
        ></v-text-field> -->



      <div
       v-for="item in items"
        :key="item.id">
        <v-list-item>
          <template v-slot:default="{ active }">
          <!-- remove checkbox later -->
            <!-- <v-list-item-action>
              <v-checkbox
                :input-value="active"
                color="primary"
              ></v-checkbox>
            </v-list-item-action> -->

            <v-list-item-content>
              <v-list-item-title>{{item.title}}</v-list-item-title>
              <!--add item quantity from database below-->
              <v-list-item-subtitle>QTY:{{item.qty}}</v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-action>
          <v-btn 
          @click.stop="itemDelete(item.id)"
          icon>
            <v-icon color="grey lighten-1">mdi-delete</v-icon>
          </v-btn>
        </v-list-item-action>
          </template>
        </v-list-item>
        <!-- remove divider later -->
        <v-divider></v-divider>
      </div>
    </v-list>
    

    <!-- Snackbar on Error -->
    <v-snackbar
      v-model="on_error.snackbar"
      :timeout="on_error.timeout"
    >
      {{ on_error.text }}


        <v-btn
          color="blue"
          text
          @click="on_error.snackbar = false"
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
    name: 'Pantry',
    data() {
      return {
        selectedItem: "",
        qty: 1,
        all_items: [],
        pantry_items: {},
        items: [],
        on_error: {
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
            // load data
            let session_id = VueCookies.get("session")

            axios.get('http://localhost:5000//pantry?session='+session_id)
            .then(response => {
              if (response.status == 200) {
                this.all_items = response.data["all"]
                this.pantry_items = response.data["pantry"]
                //this.all_items = this.processItems(all_items)
                
                this.processPantry()
              }
            })
            .catch(error => console.log(error))

          } else {
            this.$router.push('settings') 
          }

      },

      itemDelete(id) {
          //api call to delete item from db, reload the items array and load items to template
          //reload can be circumvented if the item is removed from the current view of items, one less api call
          //if page reloads, items are fetched from db anyways
        let session_id = VueCookies.get("session")
        let item_id = id
        let item_qty = this.items.filter(item => item.id == id)[0]["qty"]

        axios.delete('http://localhost:5000/pantry/delete?session='+session_id+'&item_id='+item_id+'&item_qty='+item_qty)
            .then(response => {
              if (response.status == 202) {
              this.$router.go(this.$router.currentRoute)
              }
            }
          ) 
        },
      addItem() {
        // Check if input is valid
        if (this.qty > 0 && this.selectedItem != "") {
          // get the item id from input
          let item_index = this.getKeyByValue(this.all_items.s_ingredient, this.selectedItem)

          // create new Item object
          let newItem = {
            id: this.all_items.n_item_id[item_index],
            qty: this.qty
          }

          // Check Duplicate
          if (Object.values(this.pantry_items.n_item_id).includes(newItem.id)) {
            this.on_error.text = "Item is already in pantry. Delete and re-add."
            this.on_error.snackbar = true
          }
          else {
           // call api
          let session_id = VueCookies.get("session")

          axios.get('http://localhost:5000/pantry/add?session='+session_id+'&item_id='+newItem.id+'&item_qty='+newItem.qty)
            .then(response => {
              if (response.status == 202) {
              this.$router.go(this.$router.currentRoute)
                }
              }
            )  

                        
            // clear fields after adding
            this.selectedItem = ""
            this.qty = 1     
          } 
        } else {
          this.on_error.text = "Please choose an item and a positive amount."
          this.on_error.snackbar = true
        }
    
      },
      processPantry() {
        // loop through all items and put them into this.lists
        for (let index = 0; index < Object.keys(this.pantry_items.n_pantry_id).length; index++) {
          // Dict Consisting of all necessary items
          let ingredient_index = this.getKeyByValue(this.all_items.n_item_id, this.pantry_items.n_item_id[index])
          var item = {
            id: this.pantry_items.n_item_id[index],//item id
            title: this.all_items.s_ingredient[ingredient_index], //is in all items and must be fetched via item id
            qty: this.pantry_items.f_amount_in_stock[index]
          }
          this.items.push(item);

        }

      },
      getKeyByValue(object, value) {
        return Object.keys(object).find(key => object[key] === value);
      }
    },
    beforeMount(){
    this.onload()
  }
}
</script>