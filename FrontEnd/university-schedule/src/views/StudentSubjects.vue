<!--@authors-->
<!--xrasst00, Sergei Rasstrigin-->

<!--@file StudentSubject.vue-->
<!--@brief Student subject register view-->

<template>
  <navigation
      class="nav-bar"
  >
  </navigation>

  <div class="main-container">
    <div class="subjects-grid">
      <div class="all__subj">All subjects</div>
      <div></div>
      <div class="registered__subj">Registered Subjects</div>
      <div class="all-subjects">
        <RegisterSubjectCard
            v-for="subject in getUnregisteredSubjects()"
            @subjectsUpdate="reloadSubjects"
            :key="subject.id"
            :subject="subject"
            :code="subject.code"
            :s-name="subject.name"
            :s-id="subject.id"
        ></RegisterSubjectCard>
      </div>
      <div class="self-gap">
        <div class="gap-line"></div>
      </div>
      <div class="registered-subjects">
        <registered-subject-card
            v-for="subject in registeredSubjects"
            @subjectsUpdate="reloadSubjects"
            :key="subject.id"
            :subject="subject"
            :code="subject.code"
            :s-name="subject.name"
            :s-id="subject.id"
        ></registered-subject-card>
      </div>
    </div>
  </div>
</template>

<script>
import Navigation from "@/components/Navigation.vue";
import axios from "axios";
import RegisterSubjectCard from "@/components/RegisterSubjectCard.vue";
import RegisteredSubjectCard from "@/components/RegisteredSubjectCard.vue";

export default {
  components: {RegisteredSubjectCard, RegisterSubjectCard, Navigation},
  data(){
    return{
      user: {},
      header: {
        "Authorization": localStorage.getItem("token"),
      },
      subjects:[],
      registeredSubjects:[],
    }
  },

  methods:{
    /**
     * @brief Redirects to the authorization page
     */
    Authorization() {
      this.$router.push('/authorization');
    },
    /**
     * @brief Reloads registered and unregistered subjects
     */
    reloadSubjects(){
      this.getRegisteredSubjects();
      this.getUnregisteredSubjects();
    },
    /**
     * @brief Filters unregistered subjects
     * @returns {Array} - Unregistered subjects
     */
    getUnregisteredSubjects() {
      return this.subjects.filter((subject) =>
          this.registeredSubjects.every((registeredSubject) => registeredSubject.id !== subject.id)
      );
    },
    /**
     * @brief Fetches user data from local storage
     */
    getUser(){
      try{
        const storedUser = localStorage.getItem('user');
        if(storedUser){
          this.user = JSON.parse(storedUser);
        }
      }catch (error){
        console.log(error);
      }
    },
    /**
     * @brief Fetches all subjects
     */
    async getAllSubjects(){
      try{
        await axios.get(`${import.meta.env.VITE_API_HOST}/subject`,{headers: this.header})
            .then(response => {
              this.subjects = response.data.data;
            })
            .catch(error => {
              console.error('Error response: ', error);
            });
      }catch (e) {
        console.log(e);
      }
    },
    /**
     * @brief Fetches registered subjects
     */
    async getRegisteredSubjects(){
      try{
        await axios.get(`${import.meta.env.VITE_API_HOST}/student_subjects/${this.user.id}`,{headers: this.header})
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
  },
  mounted() {
    this.getUser();
    this.getAllSubjects();
    this.getRegisteredSubjects();
  }
}
</script>

<style scoped>
.main-container{
  display: flex;
  justify-content: center;
  align-items: center;
  background: none;
  width: 100%;
  height: 85vh;
}
.subjects-grid{
  display: grid;
  grid-template-columns: 1fr 30px 1fr;
  grid-auto-rows: 20px 1fr;
  grid-row-gap: 20px;
  background: none;
  width: 95%;
  height: 95%;
}
.registered-subjects,
.all-subjects{
  display: flex;
  flex-direction: column;
  align-items: center;
  background: none;
  overflow: auto;
}
.registered-subjects{
  background: none;
}
.registered-subjects::-webkit-scrollbar,
.all-subjects::-webkit-scrollbar {
  width: 12px;
}

.registered-subjects::-webkit-scrollbar-thumb,
.all-subjects::-webkit-scrollbar-thumb {
  background-color: black;
  border-radius: 10px;
}

.registered-subjects::-webkit-scrollbar-track,
.all-subjects::-webkit-scrollbar-track {
  background-color: #f2f2f2;
  border-radius: 10px;
}
.self-gap{
  display: flex;
  justify-content: center;
  align-items: center;
}
.gap-line{
  width: 2px;
  background: rgba(0, 0, 0, 0.5);
  height: 100%;
}
.registered__subj,
.all__subj{
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 30px;
}
</style>