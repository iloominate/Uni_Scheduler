<!--@authors-->
<!--xklima34, Aliaksei Klimau-->
<!--@file Authorization.vue-->
<!--@brief Authorization view-->

<template>
  <section>

    <div class="form-box">
      <div class="form-value">
        <form action="" @submit.prevent>
          <h2 class="login_name">Login</h2>
          <div class="inputbox">
            <input v-model="postData.username" type="text" >
            <label for="">Username</label>
          </div>
          <div class="inputbox">
            <input v-model="postData.password" type="password" >
            <label for="">Password</label>
          </div>
          <div class="bttns">
            <button class="login_bttn" @click="sendGetUser">Log in</button>
            <button class="home_bttn" @click="ToHome">Home</button>
          </div>

        </form>
      </div>
    </div>

  </section>
</template>

<script>
import axios from "axios";
import Navigation from "@/components/Navigation.vue";

export default {
  components: {Navigation},

  data(){
    return{
      postData: {
        username: '',
        password: '',
      }
    }
  },
  methods:{

    // Authorize and retrieve user data
    sendGetUser() {
      localStorage.clear();

      // Check if user is authorized
      axios.post(`${import.meta.env.VITE_API_HOST}/auth/token`, this.postData)
          .then(response => {
            const token = response.data.access;
            localStorage.setItem('token', 'Bearer ' + token);
            const headers = {
              'Authorization': 'Bearer ' + token,
            };

            // Get user info from backend
            axios.get(`${import.meta.env.VITE_API_HOST}/my-info`, {headers:headers})
                .then(response => {
                  const user = response.data;
                  localStorage.setItem('user', JSON.stringify(user));
                  switch (user.permission.description) {
                    case 'Admin':
                      this.$router.push('/admin')
                      break;
                    case 'Guarantor':
                      this.$router.push('/guarantor')
                      break;
                    case 'Instructor':
                      this.$router.push('/instructor')
                      break;
                    case 'Scheduler':
                      this.$router.push('/scheduler')
                      break;
                    case 'Student':
                      this.$router.push('/student')
                      break;
                    default:
                      break;
                  }
                })
                .catch(error => {
                  console.error('Error get user data.');
                });
          })
          .catch(error => {
            console.log("Wrong user or password.");
          });
    },

    // Navigate to home page
    ToHome() {
      this.$router.push('/');
    },
  },
}
</script>

<style scoped>
*{
  margin: 0;
  padding: 0;
}
section{
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100%;
  background: none;
}

.form-box{
  position: relative;
  width: 400px;
  height: 450px;
  background: white;
  border-radius: 20px;
  border: none;
  display: flex;
  justify-content: center;
  align-items: center;
}

h2{
  font-size: 2em;
  color: black;
  text-align: center;
}
.inputbox{
  position: relative;
  margin-top: 40px;
  margin-bottom: 20px;
  width: 310px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.1);
}
.inputbox label {
  position: absolute;
  top: 50%;
  left: 5px;
  transform: translateY(-40%);
  color: rgba(0, 0, 0, 0.6);
  font-size: 1em;
  font-weight: bold;
  pointer-events: none;
  transition: .5s;
  height: 40px;
}



input:focus ~ label,
input:valid ~ label{
  top: -5px;
}
.inputbox input{
  width: 100%;
  height: 50px;
  background: transparent;
  border: none;
  outline: none;
  font-size: 20px;
  padding: 0 35px 0 5px;
  color: black;
}
.bttns{
  display: flex;
  justify-content: center;
  gap: 20px;
}
button{
  width: 30%;
  height: 40px;
  border-radius: 10px;
  border: none;
  color: white;
  cursor: pointer;
  outline: none;
  font-size: 1em;
  font-weight: 600;
}
.home_bttn{
  background-color: #45BFFF;
}
.login_bttn{
  background-color: #84D296;
}

</style>