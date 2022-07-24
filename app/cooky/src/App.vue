<template>
  <v-app id="cooky">


    <v-main>
      <router-view></router-view>
    </v-main>


    <v-bottom-navigation
      app
      :value="value"
      color="primary"
    >
    
      <v-btn
        v-for="item in items"
        :to="item.to">

        <span>{{ item.title }}</span>

        <v-icon>{{ item.icon }}</v-icon>
        
      </v-btn>
      
    </v-bottom-navigation>

  </v-app>
</template>

<script>
  
  export default {
    data() {
      return {
    value: "1",
    items: [
          { title: 'Explore', icon: 'mdi-chef-hat', to:'/' },
          { title: 'Pantry', icon: 'mdi-fridge', to:'/pantry' },
          { title: 'Settings', icon: 'mdi-account', to:'/settings' },
        ] }},// navigation items
  }
</script>