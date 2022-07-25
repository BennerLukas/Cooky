
<template>
<div>
<!-- Login View -->
<v-form v-model="valid" v-if="!isHidden">
    <h1>Login</h1>
    <v-container>
      <v-row>
        <v-col
          cols="12"
          md="4"
        >
          <v-text-field
            v-model="formData.username"
            label="username"
            required
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          md="4"
        >
          <v-text-field
            v-model="formData.password"
            label="password"
            required

            :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
            :type="show ? 'text' : 'password'"
            
            
            @click:append="show = !show"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>
    <v-btn @click="loginPost">Login</v-btn>
  </v-form>

<!-- Account View -->
<v-skeleton-loader
  type="card-avatar, article, actions"
  v-if="isHidden">
</v-skeleton-loader>

</div>
</template>

<script>
import axios from 'axios'
import VueCookies from 'vue-cookies'

  export default {
    data: () => ({
        name:"login",
        isHidden:false,
        formData : {
            username: '',
            password: '',
        },
      valid: false,
      show: false,
    }),
    methods: {
        onload() {
          //check if session exists, if yes, show different view
          var session = VueCookies.isKey("session")
          if (session) {
            //change render
            this.isHidden = true
          }
        },
        loginPost() {
          if (this.formData.username.length > 0) {
            axios.post('http://localhost:5000/login', this.formData)
            .then(function (response) {
              if (response.status == 200) {
                VueCookies.set('session' , response.data.session, "10h")
                window.location.href = "/"; // on success, redirects to explore view
              }
            })
            .catch(error => console.log(error))
        }
      }
    },
    beforeMount(){
    this.onload()
  }
}
</script>