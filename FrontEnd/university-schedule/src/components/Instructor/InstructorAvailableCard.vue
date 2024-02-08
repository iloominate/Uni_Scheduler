<template>
  <div :class="cardClass" class="request_card">
    <div class="header">
      <div class="head-name">
        {{request.activity_type.name}}
      </div>
      <div class="cross" >
        <div v-if="!registered" @click="registerActivity">
          <checkmark></checkmark>
        </div>
        <div v-else @click="unregisterActivity">
          <cross></cross>
        </div>
      </div>
    </div>
    <div class="body">
      <div class="repeating">Repeating: {{ this.repeating }}</div>
      <div class="duration">Duration: {{request.duration}}</div>
      <div class="notes-box">
        <div class="notes-label">Guarantor notes</div>
        <div class="notes-icon" @click="checkGuarantorNotes">
          <IconNoteText></IconNoteText>
        </div>
      </div>
      <div v-if="registered" class="notes-box">
        <div class="notes">Your notes</div>
        <div class="notes-icon" @click="registerActivity">
          <IconNoteText></IconNoteText>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import Cross from "@/components/icons/Cross.vue";
import Checkmark from "@/components/icons/Checkmark.vue";
import IconNoteText from "@/components/icons/IconNoteText.vue";

export default {
  components: {Checkmark, Cross, IconNoteText},
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
    registered: {
      type: Boolean,
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
    registerActivity(){
      this.$emit('registerActivity', this.request);
    },
    unregisterActivity(){
      this.$emit('unregisterActivity', this.request);
    },
    checkGuarantorNotes()
    {
      this.$emit('checkGuarantorNotes', this.request);
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
  max-height: 170px;
  border: 3px solid black;
  margin-top: 3px;
  margin-right: 10px;
  border-radius: 10px;
  color: black; /* Цвет текста */
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
  margin-bottom: 7px;
  margin-top: 3px;
  overflow: clip;
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

.notes-box{
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  margin-bottom: 0;
  gap: 5px;
  height: 24px
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