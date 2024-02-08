<!--@authors-->
<!--xrasst00, Sergei Rasstrigin-->

<!--@file StudentView.vue-->
<!--@brief Student main page view-->

<template>
  <navigation
      class="nav-bar"
  >
  </navigation>
  <div class="main-container">

    <div class="range-picker">

      <div class="schedule-bttns">
        <div class="schedule-bttn">
          <button class="schedule-button" :class="{ 'selected-schedule': !weeklySchedule }" @click="annualScheduleFunc">
            semester schedule
          </button>
        </div>
        <div class="schedule-bttn">
          <button class="schedule-button" :class="{ 'selected-schedule': weeklySchedule }" @click="weeklyScheduleFunc">
            weekly schedule
          </button>
        </div>
      </div>

      <div class="picker-data" v-if="weeklySchedule">
        <div class="date-range">
          {{ startDate }} - {{ endDate }}
        </div>
        <div class="arrow-buttons">
          <button @click="decreaseDate()" class="bttn">←</button>
          <button @click="increaseDate()" class="bttn">→</button>
        </div>
      </div>
    </div>

    <CalendarTest style="margin-top: 0px"
                  :activities="activities"
                  :key="calendarKey"
                  :is-scheduler="false"
    >
    </CalendarTest>

  </div>



</template>

<script>

import Navigation from "@/components/Navigation.vue";
import axios from "axios";
import ScheduleCell from "@/components/ScheduleCell.vue";
import RegisterInstructorCard from "@/components/RegisterInstructorCard.vue";
import GuarantRequest from "@/components/GuarantRequest.vue";
import Calendar from "@/components/Calendar.vue";
import CalendarTest from "@/components/CalendarTest.vue";

export default {
  components: {CalendarTest, Calendar, GuarantRequest, RegisterInstructorCard, ScheduleCell, Navigation},
  data(){
    return{
      user: {}, /**< User information */
      header: {
        "Authorization": localStorage.getItem("token"), /**< Authorization token from local storage */
      },
      startDate: '18.09.2023', /**< Start date for activities */
      endDate: '24.09.2023', /**< End date for activities */
      activities: [], /**< Array to store fetched activities */
      calendarKey: 0, /**< Key to force re-render of CalendarTest component */
      weeklySchedule: true, /**< Flag for weekly schedule */
    }
  },

  methods:{
    /**
     * @brief Redirects to the authorization page
     */
    Authorization() {
      this.$router.push('/authorization'); /**< Redirects to the authorization page */
    },
    /**
     * @brief Fetches user information and activities from local storage
     */
    getUserAndActivities(){
      try{
        const storedUser = localStorage.getItem('user'); /**< Get user data from local storage */
        if(storedUser){
          this.user = JSON.parse(storedUser); /**< Parse user data */
          this.getActivities(); /**< Fetch user activities */
        }

      }catch (error){
        console.log(error);
      }
    },
    /**
     * @brief Updates the key to force re-rendering of the CalendarTest component
     */
    updateKey(){
      this.calendarKey += 1;
    },
    /**
     * @brief Fetches activities based on the selected schedule type
     */
    async getActivities(){
      if(this.weeklySchedule){
        const date_from = this.convertDate(this.startDate);
        const date_to = this.convertDate(this.endDate);
        await axios.get(`${import.meta.env.VITE_API_HOST}/student_activities/${this.user.id}?date_from=${date_from}&date_to=${date_to}`,{headers: this.header})
            .then(response=>{
              this.activities = response.data.data;
              this.updateKey();
            })
            .catch(e=>{
              console.log(e);
            })
      }
      else{
        await axios.get(`${import.meta.env.VITE_API_HOST}/student_activities/${this.user.id}`,{headers: this.header})
            .then(response=>{
              this.activities = response.data.data;
              this.updateKey();
            })
            .catch(e=>{
              console.log(e);
            })
      }

    },
    /**
     * @brief Formats a given date to a specific string format
     * @param {Date} date - The date object to be formatted
     * @returns {string} - Formatted date string
     */
    formatDate(date) {
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();

      return `${day < 10 ? '0' : ''}${day}.${month < 10 ? '0' : ''}${month}.${year}`;
    },
    /**
     * @brief Increases the displayed date range by 7 days
     */
    increaseDate() {
      const startDateArr = this.startDate.split('.').map(Number);
      const endDateArr = this.endDate.split('.').map(Number);

      const start = new Date(startDateArr[2], startDateArr[1] - 1, startDateArr[0]);
      const end = new Date(endDateArr[2], endDateArr[1] - 1, endDateArr[0]);

      start.setDate(start.getDate() + 7);
      end.setDate(end.getDate() + 7);

      this.startDate = this.formatDate(start);
      this.endDate = this.formatDate(end);
      this.getActivities();
    },
    /**
     * @brief Decreases the displayed date range by 7 days
     */
    decreaseDate() {
      const startDateArr = this.startDate.split('.').map(Number);
      const endDateArr = this.endDate.split('.').map(Number);

      const start = new Date(startDateArr[2], startDateArr[1] - 1, startDateArr[0]);
      const end = new Date(endDateArr[2], endDateArr[1] - 1, endDateArr[0]);

      start.setDate(start.getDate() - 7);
      end.setDate(end.getDate() - 7);

      this.startDate = this.formatDate(start);
      this.endDate = this.formatDate(end);
      this.getActivities();
    },
    /**
     * @brief Converts a date string to a specific format
     * @param {string} inputDate - The date string to be converted
     * @returns {string} - Converted date string
     */
    convertDate(inputDate) {
      const [day, month, year] = inputDate.split('.');
      return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
    },
    /**
     * @brief Switches to displaying weekly schedule and fetches activities
     */
    weeklyScheduleFunc(){
      this.weeklySchedule = true;
      this.getActivities();
    },
    /**
     * @brief Switches to displaying annual schedule and fetches activities
     */
    annualScheduleFunc(){
      this.weeklySchedule = false;
      this.getActivities();
    },

  },
  mounted() {
    this.getUserAndActivities();

  },

}
</script>

<style scoped>
.nav-bar{
  margin-top: 5px;
  margin-bottom: 0;
}
.main-container{
  align-items: center;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 90vh;
}
.range-picker{
  width: 100%;
  height: 40px;
  display: flex;
  justify-content: start;
  align-items: center;
  margin-top: 30px;
}
.picker-data{
  display: flex;
  background: white;
  align-items: center;
  height: 100%;
  min-width: 320px;
  border: 3px solid black;
  border-radius: 10px;
  margin-right: 40px;
  margin-left: auto;
  margin-bottom: 5px;
}
.date-range{
  margin-right: 15px;
  margin-left: 15px;
  font-size: 16px;
  font-weight: bold;
}
.arrow-buttons{
  margin-right: 5px;
  display: flex;
  justify-content: space-between;
  margin-left: auto;

}
.bttn{
  margin-right: 10px;
  border: 3px solid darkred;
  cursor: pointer;
  height: 25px;
  width: 32px;
}
.schedule-bttn{
  margin-left: 10px;
  height: 100%;
}
.schedule-bttns{
  display: flex;
  height: 100%;
  width: fit-content;
  align-items: center;
  margin-left: 5%;

}
.schedule-button{
  height: 100%;
  font-size: 20px;
  border: none;
  background: white;
  cursor: pointer;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  border-right: 2px solid black;
  border-top: 2px solid black;
  border-left: 2px solid black;
  background: rgba(0, 0, 0, 0.1);
  opacity: 0.5;
}
.schedule-button:hover{
  background: white;
  opacity: 1;
}
.selected-schedule{
  background: white;
  opacity: 1;
}
</style>