<!--@authors-->
<!--xrasst00, Sergei Rasstrigin-->

<!--@file GuarantorInstructors.vue-->
<!--@brief Guarantor manage instructors view-->

<template>
  <navigation
      class="nav-bar"
  >
  </navigation>
  <ListOfInstructors
      :instructors="instructors"
      :registered_instructors="registered_instructors"
      @unregister_instructor="unregisterInstructor"
      @instructor_register2="registerInstructor"
  >
  </ListOfInstructors>
</template>

<script>

import Navigation from "@/components/Navigation.vue";
import axios from "axios";
import RegisterSubjectCard from "@/components/RegisterSubjectCard.vue";
import RegisteredSubjectCard from "@/components/RegisteredSubjectCard.vue";
import RegisterInstructorCard from "@/components/RegisterInstructorCard.vue";
import ListOfInstructors from "@/components/ListOfInstructors.vue";
import {toast} from "vue3-toastify";

export default {
  components: {ListOfInstructors, RegisterInstructorCard, RegisteredSubjectCard, RegisterSubjectCard, Navigation},
  data(){
    return{
      header: {
        "Authorization": localStorage.getItem("token"),
      },
      instructors : [],
      registered_instructors: [],
      guarantorSubject : {},
      user: {},
    }
  },

  methods:{
    /**
     * @brief Fetches the subject information for the guarantor
     */
    async getSubject(){
      try {
        await axios.get(`${import.meta.env.VITE_API_HOST}/subject?guarantor_id=${this.user.id}`, {headers: this.header})
            .then(response => {
              this.guarantorSubject = response.data.data[0];
            })
            .catch(error=>{
              console.log(error);
            })

      }catch (e) {
        console.log(e);
      }

    },
    /**
     * @brief Fetches user data from local storage
     */
    getUser(){
      const storedUser = localStorage.getItem('user');
      if(storedUser) {
        this.user = JSON.parse(storedUser);
      }
    },
    /**
     * @brief Fetches the list of instructors and separates registered instructors
     */
    async getInstructors(){
      try {
        await axios.get(`${import.meta.env.VITE_API_HOST}/get_all_instructors`, {headers: this.header})
            .then(response => {
              const allInstructors = response.data.data;
              console.log(allInstructors);
              const tempInstructors = [];
              const tempRegisteredInstructors = [];
              allInstructors.forEach(instructor => {
                if (this.guarantorSubject.instructors.includes(instructor.id)) {
                  tempRegisteredInstructors.push(instructor);
                } else {
                  tempInstructors.push(instructor);
                }
              });

              this.instructors = tempInstructors;
              this.registered_instructors = tempRegisteredInstructors;
            })
            .catch(error => {
              console.error('Error response: ', error);
            });
      } catch (e) {
        console.log(e);
      }
    },
    /**
     * @brief Loads user data, subject, and instructors data
     */
    async loadData(){
      this.getUser();
      await this.getSubject();
      await this.getInstructors();
    },
    /**
     * @brief Unregisters an instructor
     * @param {Object} instructor - The instructor to be unregistered
     */
    async unregisterInstructor(instructor) {
      try {
        await axios.delete(`${import.meta.env.VITE_API_HOST}/register_instructor/${instructor.id}/${this.guarantorSubject.id}`, {headers: this.header})
            .then(response => {
              const index = this.registered_instructors.findIndex(regInstructor => regInstructor.id === instructor.id);
              if (index !== -1) {
                const removedInstructor = this.registered_instructors.splice(index, 1)[0];
                this.instructors.push(removedInstructor);
              } else {
                console.log("Instructor not found in registered instructors.");
              }
              toast.success("Instructor was successfully unregistered!", {
                autoClose: 500,
                position: toast.POSITION.BOTTOM_RIGHT,
              });
            });
      } catch (e) {
        console.error(e);
      }
    },
    /**
     * @brief Registers an instructor
     * @param {Object} instructor - The instructor to be registered
     */
    async registerInstructor(instructor) {
      try {
        await axios.post(`${import.meta.env.VITE_API_HOST}/register_instructor/${instructor.id}/${this.guarantorSubject.id}`,{},{headers: this.header})
            .then(response => {
              console.log(response.data);
              const index = this.instructors.findIndex(inst => inst.id === instructor.id);
              if (index !== -1) {
                const removedInstructor = this.instructors.splice(index, 1)[0];
                this.registered_instructors.push(removedInstructor);
              } else {
                console.log("Instructor not found in instructors list.");
              }
              toast.success("Instructor was successfully registered!", {
                autoClose: 1000,
                position: toast.POSITION.BOTTOM_RIGHT,
              });
            });
      } catch (e) {
        console.error(e);
      }
    },

  },

  mounted() {
    this.loadData();
  }

}
</script>

<style scoped>

</style>