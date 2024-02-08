<!--@authors-->
<!--xklima34, Aliaksei Klimau-->
<!--@file InstructorActivities.vue-->
<!--@brief Instructor activities registration view-->


<template>
  <navigation class="nav-bar"></navigation>
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
    <div class="all__activities__container">
      <div class="act-title">
        Available activities
      </div>
      <div class="activities-container">
        <InstructorAvailableCard
            v-for="activity in activities"
            :request="activity"
            :key="activity.id"
            :registered="false"
            @registerActivity="writeNotes"
            @checkGuarantorNotes="checkGuarantorNotes"
        >
        </InstructorAvailableCard>

      </div>
    </div>
    <div class="registered__activities__container">
      <div class="act-title">
        Registered activities
      </div>
      <div class="activities-container">
        <InstructorAvailableCard
            v-for="activity in registeredActivities"
            :request="activity"
            :key="activity.id"
            :registered="true"
            @unregisterActivity="unregisterActivity"
            @registerActivity="writeNotes"
            @checkGuarantorNotes="checkGuarantorNotes"
        >
        </InstructorAvailableCard>
      </div>
    </div>

  </div>
  <div v-if="showModal">
    <ModalWindow
        :isRegistered="checkIfRegistered()"
        :isGuarantor=false
        :activity="selectedActivity"
        @close-modal="closeModal"
        @register-activity="registerActivity"
    >
    </ModalWindow>
  </div>

  <div v-if="showGuarantorModal">
    <ModalWindow
        :isRegistered=false
        :isGuarantor=true
        :activity="selectedActivity"
        @close-guarantor-modal="closeGuarantorModal"
    >
    </ModalWindow>
  </div>
</template>

<script>
import Navigation from "@/components/Navigation.vue";
import axios from "axios";
import Calendar from "@/components/Calendar.vue";
import CalendarTest from "@/components/CalendarTest.vue";
import InstructorAvailableCard from "@/components/Instructor/InstructorAvailableCard.vue";
import ModalWindow from "@/components/Instructor/ModalWindow.vue";

export default {
  components: {ModalWindow, InstructorAvailableCard, CalendarTest, Calendar, Navigation},
  data(){
    return{
      user: {},
      registeredSubjects: [],
      selectedSubject: 0,
      activities: [],
      registeredActivities: [],
      showModal: false,
      showGuarantorModal: false,
      selectedActivity:{},
      header: {
        "Authorization": localStorage.getItem("token"),
      },
    }
  },
  methods: {

    // Check if the current activity is registered
    checkIfRegistered() {
      return this.registeredActivities.some(obj => obj.id === this.selectedActivity.id)
    },
    // Open modal for writing notes
    writeNotes(activity){
      this.selectedActivity = activity;
      this.openModal();
    },
    // Open guarantor notes for activity
    checkGuarantorNotes(activity)
    {
      this.selectedActivity = activity;
      this.openGuarantorModal();
    },

    // Register an activity with instructor notes
    async registerActivity(payload) {
      const { activity, notes } = payload;
      const dataToSend = {
        "instructor_notes": notes,
      };
      await axios.post(`${import.meta.env.VITE_API_HOST}/instructor_register_activity/${this.user.id}/${activity.id}`,dataToSend,{headers: this.header})
          .then(response=>{
            this.getScheduleActivities(this.selectedSubject);
          })
          .catch(e=>{
            console.log(e);
          })
      this.closeModal();
    },

    // Unregister an activity
    async unregisterActivity(activity){
      await axios.delete(`${import.meta.env.VITE_API_HOST}/instructor_register_activity/${this.user.id}/${activity.id}`, {headers: this.header})
          .then(response=>{
            this.getScheduleActivities(this.selectedSubject);
          })
          .catch(e=>{
            console.log(e);
          })
      this.closeModal();
    },

    // Get activities for the selected subject
    async getScheduleActivities(subjectId){
      await axios.get(`${import.meta.env.VITE_API_HOST}/instructor_free_activities/${subjectId}`, {headers: this.header})
          .then(response=>{
            this.activities = response.data.data;
            this.getInstructorActivities();
          })
          .catch(e=>{
            console.log(e);
          })
    },

    // Fetch user information and subjects
    async getUserAndSubjects(){
      try{
        const storedUser = localStorage.getItem('user');
        if(storedUser) {
          this.user = JSON.parse(storedUser);
        }
        try{
          // Fetch subjects for the instructor
          await axios.get(`${import.meta.env.VITE_API_HOST}/subject?instructors=${this.user.id}`, {headers: this.header})
              .then(response => {
                this.registeredSubjects = response.data.data;
              })
              .catch(error => {
                console.error('Error response: ', error);
              });
        }catch (e) {
          console.log(e);
        }

      } catch (error){
        console.log(error);
      }
    },

    // Get activities for the instructor
    async getInstructorActivities(){
      await axios.get(`${import.meta.env.VITE_API_HOST}/activity?instructor=${this.user.id}&subject=${this.selectedSubject}`, {headers: this.header})
          .then(response=>{
            this.registeredActivities = response.data.data;
          })

    },

    // Close the modal and reset selected activity
    closeModal(){
      this.showModal = false;
      this.selectedActivity = {};
      this.isRegistered = false;
    },

    // Close the guarantor modal and reset selected activity
    closeGuarantorModal()
    {
      this.showGuarantorModal = false;
      this.selectedActivity = {};
      this.isRegistered = false;
    },

    // Open the modal
    openModal(){
      this.showModal = true;
    },

    // Open the guarantor modal
    openGuarantorModal() {
      this.showGuarantorModal = true;
    }
  },
  watch: {
    // Watch for changes in the selectedSubject and fetch new activities
    async selectedSubject(newValue, oldValue) {
      await this.getScheduleActivities(newValue);
    },
  },
  mounted() {
    // Fetch user and subject information when the component is mounted
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
  height: 60px;
  background: #81d4fa;
  margin-top: 20px;
  margin-left: 170px;
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
.all__activities__container{
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 40vh;
  justify-content: center;
}
.registered__activities__container {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 40vh;
  justify-content: center;
}
.act-title{
  font-size: 25px;
  font-weight: bold;
}
.activities-container{
  background: white;
  display: flex;
  justify-content: start;
  align-items: center;
  padding-left: 20px;
  height: 80%;
  width: 80%;
  border-radius: 15px;
  border: 3px solid teal;
  overflow: auto;
}
.activities-container::-webkit-scrollbar {
  width: 1px;
}

.activities-container::-webkit-scrollbar-track {
  background-color: #d3d3d3;
  border: none;
  border-radius: 5px;
}

.activities-container::-webkit-scrollbar-thumb {
  background-color: black;
  border-radius: 10px;
  border: 3px solid #d3d3d3;
  height: 100%;
}
</style>