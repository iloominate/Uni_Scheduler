<!--@authors-->
<!--xmyron00,Yurii Myronov-->
<!--xrasst00, Sergei Rasstrigin-->

<!--@file ScheduleCellTest.vue-->
<!--@brief Optimized copy of ScheduleCell.vue for CalendarTest-->
<template>
  <div class="all">
    <div
        class="tooltip"
        :style="{'display': isTooltipVisible ? 'block' : 'none'}"
        @mouseenter="showTooltip"
        @mouseleave="hideTooltip"
    >
      <div v-if="activity.subject.code">
        <p>Code:</p>
        <p>{{ activity.subject.code }}</p>
      </div>
      <div v-if="activity.activity_type">
        <p>Type:</p>
        <p>{{ activity.activity_type.name }}</p>
      </div>
      <div v-if="activity.activity_type">
        <p>Duration:</p>
        <p>{{ activity.duration }} hours</p>
      </div>
      <div v-if="activity.instructor">
        <p>Instructor:</p>
        <p>{{ activity.instructor.first_name + " " + activity.instructor.last_name }}</p>
      </div>
    </div>
    <div
        class="cell"
        :style="colors.outside"
        @click="changeActivity"
        :class="{ clickable: true }"
        @mouseenter="showTooltip"
        @mouseleave="hideTooltip"

    >
      <div :style="colors.inside">
        <p :style="colors.title">Subject</p>
        <p class="var">{{ activity.subject.code }}</p>
      </div>
      <div :style="colors.inside">
        <p :style="colors.title">Room</p>
        <p class="var">{{ activity.room.number }}</p>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  props: {
    activity: {
      type: Object,
      default: {}
    },
    isScheduler: {
      type: Boolean,
      default: false
    },
    state:{
      type: String,
      default: 'view'
      // view(default) unregistered registered
    }
  },
  data() {
    return{
      colors: {
        outside: { 'background-color': "#84D296", 'opacity': 1},
        inside: { 'background-color': "#9DDBAB" },
        title: { 'color': "#E2F4E6" }
      },
      isTooltipVisible: false,
      isDialogOpen: false,
    }
  },
  mounted() {
    this.UpdateStyles()
  },
  methods: {
    showTooltip() {
      this.isTooltipVisible = true;
    },
    hideTooltip() {
      this.isTooltipVisible = false;
    },
    UpdateStyles() {
      switch (this.activity.activity_type.name) {
        case "Lecture":
          this.colors = {
            outside: { 'background-color': "#84D296" },
            inside: { 'background-color': "#9DDBAB" },
            title: { 'color': "#E2F4E6" }
          };
          break;
        case "Practice":
          this.colors = {
            outside: { 'background-color': "#FFBB56" },
            inside: { 'background-color': "#FFB13B" },
            title: { 'color': "#FFD89D" }
          };
          break;
        case "Laboratory":
          this.colors = {
            outside: { 'background-color': "#45BFFF" },
            inside: { 'background-color': "#41B4F0" },
            title: { 'color': "#C5CAF6" }
          };
          break;
        case "Exam":
          this.colors = {
            outside: { 'background-color': "#717EEE" },
            inside: { 'background-color': "#8993ED" },
            title: { 'color': "#C5CAF6" }
          };
          break;
      }
      switch (this.state) {
        case "unregistered":
          this.colors.outside.opacity = 0.5;
          break;
        case "registered":
          this.colors.outside.opacity = 1;
          this.colors.outside['border'] = '4px solid green';
          break;
        default:
          break;
      }
    },
    changeActivity() {
      if (this.state === 'unregistered') {
        this.$emit('register_activity', this.activity);
      }
      else if(this.state === 'registered'){
        this.$emit('unregister_activity', this.activity);
      }
    },
  }
};
</script>

<style scoped>

.all {
  position: relative;
}
.cell {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  color: white;
  padding: 10px;
  border-radius: 20px;
}

.tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  padding: 8px;
  background-color: white;
  border: 1px solid rgb(0, 0, 0, 0.2);
  border-radius: 5px;
}

.tooltip > div {
  display: flex;
  gap: 5px;
  white-space: nowrap;
}


.tooltip > div > p:first-child {
  font-weight: 700;
}

.tooltip > div > p{
  margin: 0;
}


.cell:hover .tooltip {
  opacity: 1;
}

.cell > div {
  text-align: center;
  padding: 3px 10px;
  border-radius: 10px;
}

.cell > div > p:first-child {
  font-size: 12px;
}

.cell > div > p {
  margin: 0;
}

.var {
  font-size: 24px;
}

.custom-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 10px;
  background-color: #fff;
  padding: 30px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}

.custom-dialog > p {
  font-size: 20px;
  margin: 0;
  color: rgba(0, 0, 0, 0.7);
}

.custom-dialog > div {
  display: flex;
  gap: 10px;
  padding-top: 20px;
  justify-content: end;
}

.custom-dialog > div > button {
  font-size: 16px;
  padding: 7px 20px;
  border-radius: 5px;
}

.custom-dialog > div > button:first-child {
  background-color: #FF7783;
  border: none;
  color: white;
}

.custom-dialog > div > button:first-child:hover {
  background-color: #FF6975;
  cursor: pointer;
}

.custom-dialog > div > button:last-child {
  background-color: white;
  border: 1px solid gray;
  color: rgba(0, 0, 0, 0.5);
}

.custom-dialog > div > button:last-child:hover {
  background-color: #ebebeb;
  cursor: pointer;
}


.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.clickable {
  cursor: pointer;
}

.clickable:hover {
  filter: invert(10%);
}

</style>