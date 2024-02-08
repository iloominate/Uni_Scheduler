<!--@authors-->
<!--xrasst00, Sergei Rasstrigin-->

<!--@file GuarantorView.vue-->
<!--@brief Guarantor main page with semester schedule-->

<template>
  <navigation
      class="nav-bar"
  >
  </navigation>
  <div class="main-container">
    <CalendarTest
        style="margin-top: 5px"
        :activities="activities"
        :key="calendarKey"
        :is-scheduler="false"
    ></CalendarTest>
  </div>
</template>

<script>

import Navigation from "@/components/Navigation.vue";
import axios from "axios";
import CalendarTest from "@/components/CalendarTest.vue";

export default {
  components: {CalendarTest, Navigation},
  data(){
    return{
      header: {
        "Authorization": localStorage.getItem("token"),
      },
      user: {},
      guarantorSubject: {},
      activities: [],
      calendarKey: 0,
    }
  },

  methods: {
    /**
     * @brief Fetches the user data from local storage
     */
    getUser(){
      const storedUser = localStorage.getItem('user');
      if(storedUser) {
        this.user = JSON.parse(storedUser);
      }
    },
    /**
     * @brief Fetches the guarantor subject and related activities
     */
    async getGuarantorSubjectAndActivities(){
      try {
        // change to user.id
        await axios.get(`${import.meta.env.VITE_API_HOST}/subject?guarantor_id=${this.user.id}`, {headers: this.header})
            .then(response => {
              this.guarantorSubject = response.data.data[0];
              //console.log(this.guarantorSubject)
              localStorage.setItem('subject', JSON.stringify(this.guarantorSubject));
              axios.get(`${import.meta.env.VITE_API_HOST}/subject_activities/${this.guarantorSubject.id}`, {headers: this.header})
                  .then(response=>{
                    this.activities = response.data.data;
                    this.updateKey();
                  })
            })
            .catch(error => {
              console.error('Error response: ', error);
            });
      }catch (e) {
        console.log(e);
      }
    },
    /**
     * @brief Updates the calendar key to force re-rendering
     */
    updateKey(){
      this.calendarKey += 1;
    }
  },
  async mounted() {
    this.getUser();
    await this.getGuarantorSubjectAndActivities();
  },
}
</script>

<style scoped>
.main-container{
  justify-content: start;
  flex-direction: column;
  display: flex;
  width: 100%;
  height: 90vh;
}
</style>