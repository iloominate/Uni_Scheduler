<!--@authors-->
<!--xrasst00, Sergei Rasstrigin-->

<!--@file GuarantRequest.vue-->
<!--@brief Component of card Guarantor's requests-->

<template>
  <div :class="cardClass" class="request_card">
    <div class="header">
      <div class="head-name">
        {{ subject.code }} {{request.activity_type.name}}
      </div>
      <div class="cross" @click="deleteRequest">
        <cross></cross>
      </div>
    </div>
    <div class="body">
      <div class="repeating">Repeating: {{ this.repeating }}</div>
      <div class="duration">Duration: {{request.duration}}</div>
      <div class="notes">Notes: {{request.guarantor_notes}}</div>
    </div>
  </div>
</template>

<script>

import Cross from "@/components/icons/Cross.vue";

export default {
  components: {Cross},
  data(){
    return{
      repeating: '',
    }
  },
  props: {
    request: {
      type: Object,
      required: true,
    },
    subject: {
      type: Object,
      required: true,
    }
  },
  computed: {
    cardClass() {
      return {
        request_card: true, // Base class card
        'lecture-type': this.request.activity_type.name === 'Lecture',
        'exercise-type': this.request.activity_type.name === 'Practice',
        'exam-type': this.request.activity_type.name === 'Exam',
        'laboratory-type': this.request.activity_type.name === 'Laboratory',

      };
    },
  },
  methods:{
    /**
     * @brief Writes the formatted repeating pattern based on activity repetition.
     * @returns {void}
     */
    writeRepeating(){
      switch (this.request.activity_repetition) {
        case(1):
          this.repeating = 'Every week'
          break;
        case(2):
          this.repeating = 'Even week'
          break;
        case(3):
          this.repeating = 'Odd week'
          break;
        case(4):
          this.repeating = 'One time'
          break;
        default:
          this.repeating = 'default'
          break;
      }

    },
    /**
     * @brief Emits an event to delete the request.
     * @returns {void}
     */
    deleteRequest(){
      this.$emit('deleteRequest', this.request);
    },
  },

  mounted() {
    this.writeRepeating();
  }

}
</script>

<style scoped>
.request_card{
  display: flex;
  flex-direction: column;
  background: #84D296;
  min-width: 280px;
  max-width: 280px;
  min-height: 135px;
  max-height: 135px;
  border: 3px solid black;
  margin-top: 3px;
  margin-right: 10px;
  border-radius: 10px;
}
.header{
  height: 40px;
  display: flex;
  align-items: center;
  font-size: 25px;
  font-weight: bold;
  border-bottom: 2px solid black;
}
.body{
  height: 75%;
  display: flex;
  flex-direction: column;
  font-size: 20px;
  padding-top: 3px;
  padding-left: 3px;
  overflow: auto;
}
.cross{
  margin-left: auto;
  width: 13%;
  height: 100%;
  cursor: pointer;
}
.head-name{
  height: 100%;
  display: flex;
  align-items: center;
  margin-left: 5px;
}
.lecture-type {
  background: #84D296; /* Цвет для лекции */
}
.exercise-type {
  background: #FFBB56;
}
.exam-type{
  background: #717EEE;
}
.laboratory-type{
  background: #45BFFF;
}
.body::-webkit-scrollbar {
  width: 8px;
}

.body::-webkit-scrollbar-track {
  background-color: transparent;
}

.body::-webkit-scrollbar-thumb {
  background-color: black;
  border-radius: 8px;
}
</style>