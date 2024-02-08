<!--@authors-->
<!--xklima34, Aliaksei Klimau-->
<!--@file SubjectCard.vue-->
<!--@brief List of cards of existing subjects-->
<template>
    <div class="subject-main">
        <div v-for="subject in subjects" class="subject-card">
            <div class="subject-title">
                <p>{{ subject.code }}</p>
                <p>{{ subject.name }}</p>
            </div>
            <div class="subject-guarantor">
                <p>{{ subject.guarantor.first_name + " " + subject.guarantor.last_name}}</p>
            </div>
            <div class="subject-time-span" v-if="subject.lectureHours || subject.practiceHours || subject.laboratoryHours">
                <p>Time span:</p>
                <ul>
                    <li v-if="subject.lectureHours">{{subject.lectureHours}} lectures</li>
                    <li v-if="subject.practiceHours">{{subject.practiceHours}} practices</li>
                    <li v-if="subject.laboratoryHours">{{subject.laboratoryHours}} laboratory</li>
                </ul>
            </div>
            <div class="subject-description">
                <p>{{ subject.description }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      subjects: []
    };
  },
  methods: {

    // Function to calculate the number of weeks between two dates
    calculateWeeks(activity) {
      const millisecondsInWeek = 7 * 24 * 60 * 60 * 1000;
      const difference = Math.abs(new Date(activity.date_to) - new Date(activity.date_from));
      const weeks =  Math.ceil(difference / millisecondsInWeek);

      // Adjust weeks based on activity repetition
      if (activity.activity_repetition === 2 || activity.activity_repetition === 3){
        return Math.ceil(weeks / 2);
      }
      else{
        return weeks;
      }
    },
    // Function to fetch activities for each subject
    async fetchSubjectActivities() {

      // Iterate through each subject
      for (const subject of this.subjects) {

        // Fetch activities for the current subject
        const response = await axios.get(`${import.meta.env.VITE_API_HOST}/activity?subject=${subject.id}`);
        const activities = response.data.data;

        // Initialize variables to store weeks for each activity type
        let lectureWeeks = 0;
        let practiceWeeks = 0;
        let laboratoryWeeks = 0;

        // Iterate through each activity for the current subject and calculate weeks
        for (const activity of activities) {
          if (activity.activity_type.name === 'Lecture' && lectureWeeks === 0) {
            lectureWeeks = this.calculateWeeks(activity)
          }
          else if (activity.activity_type.name === 'Practice' && practiceWeeks === 0) {

            practiceWeeks = this.calculateWeeks(activity)
          }
          else if (activity.activity_type.name === 'Laboratory' && laboratoryWeeks === 0) {

            laboratoryWeeks = this.calculateWeeks(activity)
          }
        }
        subject.lectureHours = lectureWeeks;
        subject.practiceHours = practiceWeeks;
        subject.laboratoryHours = laboratoryWeeks;
      }
    },
  },
  mounted() {

    // Fetch the list of subjects when the component is mounted
    axios.get(`${import.meta.env.VITE_API_HOST}/subject`)
        .then(response => {
            this.subjects = response.data.data;
            this.fetchSubjectActivities();
        })
        .catch(error => {
            console.error('Error response: ', error);
        });
  }
};
</script>

<style scoped>

.subject-main {
    padding: 0px 30px;
    height: auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
}

.subject-card {
    margin: 20px 0px;
    height: auto;
    width: calc(50% - 100px);
    background-color: white;
    padding: 20px 40px;
    border-radius: 20px;
}

.subject-title {
    display: flex;
    justify-content: space-between;
    font-weight: bold;
    font-size: 28px;
}

.subject-title > p {
    margin: 5px 0px;
    text-align: right
}

.subject-guarantor {
    text-decoration: underline;
    font-weight: bold;
    font-size: 24px;
    color: rgba(0, 0, 0, 0.6);
}

.subject-guarantor > p {
    margin: 5px 0px;
}

.subject-guarantor p:hover {
    cursor: pointer;
    color: rgba(0, 0, 0);
}

.subject-time-span > * {
    margin: 10px 0px;
    font-weight: bold;
    font-size: 20px;
    color: rgba(0, 0, 0, 0.5);
}

.subject-description > p {
    font-size: 18px;
    color: rgba(0, 0, 0, 0.5);
}

</style>