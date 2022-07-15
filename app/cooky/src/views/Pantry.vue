<template>
  <div class="pantry pa-6">
    <v-list
      two-line
      flat
    >
      <h1>Pantry</h1>
        <v-text-field
        v-model="newItemName"
        @click:append="addItem"
        @keyup.enter="addItem"
          class="pa-3"
          outlined
          hide-details
          clearable
          label="Add Item"
          append-icon="mdi-plus"
        ></v-text-field>

      <div
       v-for="item in items"
        :key="item.id">
        <v-list-item
        @click="itemClick(item.id)">
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
    
</div>
</template>

<script>
  export default {
    name: 'Pantry',
    data() {
      return {
        newItemName: "",
        //fetch items from DB
        items: [
          {
            id: 1,
            title: "item1",
            qty: 111
          },
          {
            id: 2,
            title: "item2",
            qty: 9
          },
          {
            id: 3,
            title: "item3",
            qty: 3
          }
        ]
      }
    },
    methods: {
      itemClick(id) {
        let item = this.items.filter(item => item.id === id)[0]
        item.qty = 9 //ToDo: if qty = 0, delete
      },
      itemDelete(id) {
          //api call to delete item from db, reload the items array and load items to template
          //reload can be circumvented if the item is removed from the current view of items, one less api call
          //if page reloads, items are fetched from db anyways
        this.items = this.items.filter(item => item.id !== id)
      },
      addItem() {
        let newItem = {
          id: Date.now(),
          title: this.newItemName,
          qty:0
        }
        this.items.push(newItem)

        //clear field after adding
        this.newItemName = ""
      }
    }
  }
</script>