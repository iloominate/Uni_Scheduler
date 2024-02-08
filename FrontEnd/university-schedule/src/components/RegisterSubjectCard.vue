<!--@authors-->
<!--xrasst00, Sergei Rasstrigin-->

<!--@file RegisterSubjectCard.vue-->
<!--@brief Component for subject card for Student-->

<template>
  <div class="card">
    <div class="code">{{ this.subject.code }}</div>
    <div class="subject-info">
      <div class="subject-name">{{ this.subject.name }}</div>
    </div>
    <div class="register" @click="registerSubject(this.user_id, this.subject.id)">
      <checkmark></checkmark>
    </div>
  </div>
</template>

<script>

import Checkmark from "@/components/icons/Checkmark.vue";
import axios from "axios";
import {toast} from "vue3-toastify";

export default {
  components: {Checkmark},
  data(){
    return{
      user_id: Number,
      header: {
        "Authorization": localStorage.getItem("token"),
      },
    }
  },

  methods: {
    /**
     * Registers a subject for the user.
     * @param {number} user_id - User ID for registration
     * @param {number} subject_id - ID of the subject to register
     */
    registerSubject(user_id, subject_id){
      axios.post(`${import.meta.env.VITE_API_HOST}/register/${user_id}/${subject_id}`, {}, {headers: this.header})
          .then(response => {
            this.$emit('subjectsUpdate');
            toast.success("Subject was successfully registered!", {
              autoClose: 500,
              position: toast.POSITION.BOTTOM_RIGHT,
            });
          })
          .catch(error => {
            console.error('Error response: ', error);
          });
    }
  },

  mounted() {
    const storedUser = localStorage.getItem('user');
    if(storedUser){
      this.user_id = JSON.parse(storedUser).id;
    }
  },

  props: {
    subject:{
      type: Object,
      required: true,
    },
  },

}
</script>

<style scoped>
.card{
  background: white;
  display: flex;
  border: 3px solid black;
  width: 550px;
  height: 57px;
  font-size: 22px;
  align-items: center;
  margin-bottom: 10px;
}
.subject-info{
  display: flex;
  margin-left: 20px;
  background: teal;
  width: 70%;
  height: 80%;
  align-items: center;
  background: rgba(0, 0, 0, 0.1);
  padding-left: 5px;
  padding-right: 5px;
}
.code{
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 10px;
  height: 80%;
  background: rgba(0, 0, 0, 0.1);
  width: 40px;
  padding: 0 3px;
}
.register{
  display: flex;
  align-items: center;
  margin-left: auto;
  margin-right: 10px;
  height: 80%;
  background: rgba(0, 0, 0, 0.1);
  padding-left: 3px;
  padding-right: 3px;
  cursor: pointer;
}

</style>