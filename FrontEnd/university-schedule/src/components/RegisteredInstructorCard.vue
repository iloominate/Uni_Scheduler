<!--@authors-->
<!--xrasst00, Sergei Rasstrigin-->

<!--@file RegisteredInstructorCard.vue-->
<!--@brief Component for instructor card of instructors for Guarantor-->

<template>
  <div class="card">
    <div class="instructor_name">PhD {{ instructor.first_name }} {{ instructor.last_name }}</div>
    <div class="cross" @click="sendDataToList">
      <cross></cross>
    </div>

  </div>
</template>

<script>

import Checkmark from "@/components/icons/Checkmark.vue";
import Cross from "@/components/icons/Cross.vue";

export default {
  components: {Cross, Checkmark},
  data(){
    return{

    }
  },
  props:{
    instructor:{
      type: Object,
      required: true,
    }
  },
  methods:{
    sendDataToList(){
      /**
       * @brief Sends instructor information to the parent component.
       * @returns {void}
       */
      this.$emit('instructor_register', this.instructor);
    }
  },


}
</script>

<style scoped>
.card{
  display: flex;
  width: 400px;
  height: 50px;
  background: none;
  border: 4px solid black;
  margin-top: 20px;
  border-radius: 15px;
  align-items: center;
}
.instructor_name{
  display: flex;
  justify-content: left;
  align-items: center;
  border-right: 3px solid black;
  font-size: 23px;
  font-weight: bold;
  margin-left: 10px;
  height: 100%;
  width: 80%;
}
.cross{
  margin-left: auto;
  height: 100%;
  margin-right: 12px;
  margin-top: 12px;
  cursor: pointer;
}
</style>