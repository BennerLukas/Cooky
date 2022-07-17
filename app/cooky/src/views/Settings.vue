
<template>
<v-form v-model="valid">
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
    <v-btn @click="createPost">Login</v-btn>
  </v-form>


</template>

<script>
import axios from 'axios'

  export default {
    data: () => ({
        name:"login",
        formData : {
            username: '',
            password: '',
        },
      valid: false,
      show: false,
    }),
    methods: {
        createPost() {
            axios.post('http://localhost:5000/login', this.formData)
            .then(response => console.log(response))
            .catch(error => console.log(error))
        }
    }
  }
</script>