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
      <div v-if="activity.guarantor_notes">
        <p>Guarantor notes:</p>
        <p>{{ activity.guarantor_notes }}</p>
      </div>
      <div v-if="activity.instructor">
        <p>Instructor:</p>
        <p>{{ activity.instructor.first_name + " " + activity.instructor.last_name }}</p>
      </div>
      <div v-if="activity.instructor_notes">
        <p>Instructor notes:</p>
        <p>{{ activity.instructor_notes }}</p>
      </div>
    </div>
    <div 
      class="cell" 
      :style="colors.outside"
      @mouseenter="showTooltip"
      @mouseleave="hideTooltip"
      @click="handleClick"
      :class="{ clickable: isClickable }"
    >
      <div class="col-1" :style="colors.inside">
          <p :style="colors.title">Subject</p>
          <p class="var">{{ activity.subject.code }}</p>
      </div>
      <div class="col-2">
        <div class="custom-select" ref="customSelectRoom" @click.stop="toggleDropdownRoom">
          {{ selectedRoom || 'Room' }}
          <div v-if="isRoomOpen" class="dropdown" ref="dropdown" @click.stop>
            <div v-for="room in rooms" :key="room" @click="selectValue('room', room.number)">
              {{ room.number }}
            </div>
          </div>
        </div>
        <div class="sub-col">
          <div class="custom-select" @click.stop="toggleDropdownDay">
            {{ selectedDay || 'Day' }}
            <div v-if="isDayOpen" class="dropdown" ref="dropdown" @click.stop>
              <div v-for="day in days" :key="day" @click="selectValue('day', day)">
                {{ day }}
              </div>
            </div>
          </div>
          <div class="custom-select" @click.stop="toggleDropdownTime">
            {{ selectedTime || 'Time' }}
            <div v-if="isTimeOpen" class="dropdown" ref="dropdown" @click.stop>
              <div v-for="time in times" :key="time" @click="selectValue('time', time)">
                {{ time }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

    <div v-if="isDialogOpen" class="custom-dialog">
      <p>Do you want to add activity to schudule?</p>
      <div>
        <button @click="handleConfirm">Add</button>
        <button @click="closeDialog">Cancel</button>
      </div>
    </div>

    <div v-if="isDialogOpen" class="overlay"></div>
</template>

<script>
/**
 * @authors
 *   xmyron00, Yurii Myronov
 *
 * @file NotResolvedCell.vue
 * @brief Component for scheduler view
 */

export default {
  emits: ["add-to-calendar"],

  props: {
    activity: {
      type: Object,
      default: {}
    },
    rooms: {
      type: Array,
      default: {}
    }
  },

  data() {
    return {
      isRoomOpen: false,
      selectedRoom: null,

      isDayOpen: false,
      selectedDay: null,
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],

      isTimeOpen: false,
      selectedTime: null,
      times: ['8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'],

      colors: {
        outside: { 'background-color': "#84D296" },
        inside: { 'background-color': "#9DDBAB" },
        title: { 'color': "#E2F4E6" }
      },

      isClickable: false,
      isTooltipVisible: false,
      isDialogOpen: false,
    };
  },

  watch: {
    selectedRoom(newValue) {
      this.checkClickable();
    },
    selectedDay(newValue) {
      this.checkClickable();
    },
    selectedTime(newValue) {
      this.checkClickable();
    },
  },

  mounted() {
    document.addEventListener("click", this.closeDropdownIfClickedOutside);
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
    };
  },

  methods: {
    selectValue(option, value) {
      switch (option) {
        case "room":
          this.selectedRoom = value;
          this.isRoomOpen = false;
          break;
        case "day":
          this.selectedDay = value;
          this.isDayOpen = false;
          break;
        case "time":
          this.selectedTime = value;
          this.isTimeOpen = false;
          break;
      }
    },
    toggleDropdownRoom() {
      this.isRoomOpen = !this.isRoomOpen;
      this.isDayOpen = false;
      this.isTimeOpen = false;
      if (this.isRoomOpen) {
        this.$nextTick(() => {
          this.$refs.dropdown.focus();
        });
      }
    },
    toggleDropdownDay() {
      this.isDayOpen = !this.isDayOpen;
      this.isRoomOpen = false;
      this.isTimeOpen = false;
      if (this.isDayOpen) {
        this.$nextTick(() => {
          this.$refs.dropdown.focus();
        });
      }
    },
    toggleDropdownTime() {
      this.isTimeOpen = !this.isTimeOpen;
      this.isRoomOpen = false;
      this.isDayOpen = false;
      if (this.isTimeOpen) {
        this.$nextTick(() => {
          this.$refs.dropdown.focus();
        });
      }
    },
    checkClickable() {
      this.isClickable = this.selectedRoom !== null && this.selectedDay !== null && this.selectedTime !== null;
    },

    handleClick() {
      if (this.isClickable) {
        this.isDialogOpen = true;
      }
    },

    handleConfirm() {
      const room = this.rooms.find(room => room.number === this.selectedRoom);
      const time = `${this.selectedTime}:00`;
      const data = {
        room_id: room.id,
        time: time,
        day: this.selectedDay
      };
      this.$emit("add-to-calendar", this.activity, data);
      this.closeDialog();
    },

    closeDialog() {
      this.isDialogOpen = false;
    },
    showTooltip() {
      this.isTooltipVisible = true;
    },
    hideTooltip() {
      this.isTooltipVisible = false;
    },

    closeDropdownIfClickedOutside(event) {
      this.isRoomOpen = false;
      this.isDayOpen = false;
      this.isTimeOpen = false;
    },
  },
};
</script>

<style scoped>

.all {
  position: relative;
}

.cell {
    display: flex;
    gap: 10px;
    width: fit-content;
    justify-content: center;
    color: white;
    padding: 15px 10px;
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

.col-1 {
    text-align: center;
    padding: 3px 10px;
    border-radius: 10px;
}

.col-1 > p:first-child {
    font-size: 12px;
}

.col-1 > p {
    margin: 0;
}

.var {
    font-size: 28px;
}

.col-2{
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.sub-col{
  display: flex;
  gap: 5px;
}


.custom-select {
  position: relative;
  display: flex;
  justify-content: center;
  padding: 5px 10px;
  border: 1px solid white;
  border-radius: 7px;
  cursor: pointer;
  color: white;
  font-size: 10px;
  font-weight: 700;
}

.dropdown {
  background-color: white;
  position: absolute;
  top: 100%;
  left: auto;
  right: auto;
  padding: 0px 7px;
  width: fit-content;
  border: 1px solid rgb(0, 0, 0, 0.2);
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  max-height: 80px;
  outline: none;
  overflow-y: auto;
  overflow-x: hidden;
  z-index: 1;
}

.dropdown div:not(:last-child) {
  cursor: pointer;
  padding: 7px 0px;
  border-bottom: 1px solid #ccc;
  color: rgb(0, 0, 0, 0.5);
}


.dropdown div:last-child {
  cursor: pointer;
  padding: 7px 0px;
  color: rgb(0, 0, 0, 0.5);
}


.dropdown div:hover {
  color: rgb(0, 0, 0);
}

.clickable {
  cursor: pointer;
}

.clickable:hover {
  filter: invert(10%);
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
  background-color: #84D296;
  border: none;
  color: white;
}

.custom-dialog > div > button:first-child:hover {
  background-color: #9DDBAB;
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

</style>