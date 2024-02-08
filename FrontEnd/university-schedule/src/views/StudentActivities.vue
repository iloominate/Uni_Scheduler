<!--@authors-->
<!--xrasst00, Sergei Rasstrigin-->

<!--@file StudentActivities.vue-->
<!--@brief Student activities register view-->

<template>

  <navigation class="nav-bar"
  ></navigation>
  <div class="main-container">
    <div class="subject-picker">
      <div class="subject-title">
        Subject:
      </div>
      <div class="select-body">
        <select v-model="selectedSubject" class="custom-select">
          <option
              v-for="subject in registeredSubjects"
              :key="subject.id"
              :value="subject.id"
          >
            {{ subject.code }}
          </option>
        </select>
      </div>

    </div>
    <CalendarTest style="margin-top: 5px"
                  :activities="activities"
                  :key="calendarKey"
                  :is-scheduler="false"
                  @register_activity="registerActivity"
                  @unregister_activity="unregisterActivity"
    >
    </CalendarTest>
  </div>

</template>

<script>
import Navigation from "@/components/Navigation.vue";
import axios from "axios";
import Calendar from "@/components/Calendar.vue";
import CalendarTest from "@/components/CalendarTest.vue";
import {toast} from "vue3-toastify";

export default {
  components: {CalendarTest, Calendar, Navigation},
  data(){
    return{
      user: {},
      registeredSubjects: [],
      header: {
        "Authorization": localStorage.getItem("token"),
      },
      selectedSubject: 0,
      activities: [],
      calendarKey: 0,
      registeredActivities: [],

    }
  },
  methods: {
    /**
     * @brief Registers an activity for the user
     * @param {Object} activity - The activity to be registered
     */
    async registerActivity(activity){
      await axios.post(`${import.meta.env.VITE_API_HOST}/student_register_activity/${this.user.id}/${activity.id}`,{},{headers: this.header})
          .then(response=>{
            this.getStudentActivities();
            toast.success("Activity was successfully registered!", {
              autoClose: 500,
              position: toast.POSITION.BOTTOM_RIGHT,
            });
          })
          .catch(e=>{
            console.log(e);
          })
    },
    /**
     * @brief Unregisters an activity for the user
     * @param {Object} activity - The activity to be unregistered
     */
    async unregisterActivity(activity){
      await axios.delete(`${import.meta.env.VITE_API_HOST}/student_register_activity/${this.user.id}/${activity.id}`,{headers: this.header})
          .then(response=>{
            this.getStudentActivities();
            toast.success("Activity was successfully unregistered!", {
              autoClose: 500,
              position: toast.POSITION.BOTTOM_RIGHT,
            });
          })
          .catch(error=>{
            let message = error.response.data.detail.replace(/['\[\]]/g, '');
            toast.error(message, {
              autoClose: 500,
              position: toast.POSITION.BOTTOM_LEFT,
              hideProgressBar: true,
            });
          })
    },
    /**
     * @brief Fetches schedule activities for a specific subject
     * @param {number} subjectId - The ID of the subject
     */
    async getScheduleActivities(subjectId){
      await axios.get(`${import.meta.env.VITE_API_HOST}/subject_activities/${subjectId}`, {headers: this.header})
          .then(response=>{
            this.activities = response.data.data;
            this.getStudentActivities();
          })
          .catch(e=>{
            console.log(e);
          })
    },
    /**
     * @brief Updates the calendar key to force re-rendering
     */
    updateCalendarKey() {
      this.calendarKey += 1;
    },
    /**
     * @brief Updates activity types based on registration status
     */
    activityTypes(){
      this.activities.forEach(activity => {
        const registeredActivity = this.registeredActivities.find(
            registered => registered.id === activity.id
        );
        activity.regtype = registeredActivity ? 'registered' : 'unregistered';
      });
    },
    /**
     * @brief Fetches user data and registered subjects
     */
    async getUserAndSubjects(){
      try{
        const storedUser = localStorage.getItem('user');
        if(storedUser){
          this.user = JSON.parse(storedUser);
          try{
            await axios.get(`${import.meta.env.VITE_API_HOST}/student_subjects/${this.user.id}`, {headers: this.header})
                .then(response => {
                  this.registeredSubjects = response.data.data;
                })
                .catch(error => {
                  console.error('Error response: ', error);
                });
          }catch (e) {
            console.log(e);
          }
        }
      } catch (error){
        console.log(error);
      }
    },
    /**
     * @brief Fetches student activities for the selected subject
     */
    async getStudentActivities(){
      await axios.get(`${import.meta.env.VITE_API_HOST}/student_activities_subject/${this.user.id}/${this.selectedSubject}`, {headers: this.header})
          .then(response=>{
            this.registeredActivities = response.data.data;
            this.activityTypes();
            this.updateCalendarKey();
          })
          .catch(e=>{
            console.log(e);
          })
    }
  },
  watch: {
    /**
     * @brief Watches for changes in the selectedSubject and fetches corresponding activities
     * @param {number} newValue - The new selected subject ID
     * @param {number} oldValue - The previous selected subject ID
     */
    async selectedSubject(newValue, oldValue) {
        await this.getScheduleActivities(newValue);
    },
  },
  mounted() {
    this.getUserAndSubjects();
  }
}
</script>

<style scoped>
.nav-bar{
  margin-top: 5px;
  margin-bottom: 0;
}
.main-container{
  width: 100%;
  height: 90vh;
  display: flex;
  flex-direction: column;
}
.subject-picker{
  width: 190px;
  min-height: 60px;
  background: rgba(0,0,0,0.1);
  margin-top: 20px;
  margin-left: 30px;
  display: flex;
  align-items: center;
  font-size: 22px;
  font-weight: bold;
  border: 3px solid black;
  border-radius: 10px;

}
.select-body{
  margin-left: 15px;
  height: 70%;
  display: flex;
  flex-grow: 1;
  align-items: center;

}
.custom-select{
  height: 70%;
  width: 80%;
  margin-left: 10px;
  font-size: 18px;
  border: 2px solid black;
}
.subject-title{
  margin-left: 10px;
}
</style>