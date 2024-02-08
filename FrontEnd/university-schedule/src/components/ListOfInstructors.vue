<!--@authors-->
<!--xrasst00, Sergei Rasstrigin-->

<!--@file ListOfInstructors.vue-->
<!--@brief Component for list of instructors GuarantorView-->

<template>
  <div class="main-container">
    <div class="subjects-grid">
      <div class="all__subj">All Instructors</div>
      <div></div>
      <div class="registered__subj">Registered Instructors</div>
      <div class="all-subjects">
        <RegisterInstructorCard
            v-for="instructor in instructors"
            :key="instructor.id"
            :instructor="instructor"
            @instructor_register="this.registerInstructor"
        >
        </RegisterInstructorCard>
      </div>
      <div class="self-gap">
        <div class="gap-line"></div>
      </div>
      <div class="registered-subjects">
        <registered-instructor-card
            v-for="instructor in registered_instructors"
            :key="instructor.id"
            :instructor="instructor"
            @instructor_register="this.unregisterInstructor"
        >
        </registered-instructor-card>

      </div>
    </div>
  </div>
</template>

<script>

import RegisterInstructorCard from "@/components/RegisterInstructorCard.vue";
import RegisteredInstructorCard from "@/components/RegisteredInstructorCard.vue";

export default {
  components: {RegisteredInstructorCard, RegisterInstructorCard},
  props:{
    instructors : {
      type: Array,
      required: true,
    },
    registered_instructors : {
      type: Array,
      required: false,
    }
  },
  methods:{
    /**
     * @brief Registers an instructor.
     * @param {Object} instructor - The instructor to register.
     * @returns {void}
     */
    registerInstructor(instructor){
      this.$emit('instructor_register2', instructor);

    },
    /**
     * @brief Unregisters an instructor.
     * @param {Object} instructor - The instructor to unregister.
     * @returns {void}
     */
    unregisterInstructor(instructor){
      this.$emit('unregister_instructor', instructor);

    }
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