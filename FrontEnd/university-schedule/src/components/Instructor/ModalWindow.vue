<!--@authors-->
<!--xklima34, Aliaksei Klimau-->
<!--@file ModalView.vue-->
<!--@brief Window for checking notes in activity registration-->

<template>
  <div class="modal">
    <div class="modal-content">
      <h2>{{ activity.title }}</h2>
      <p>{{ activity.description }}</p>
      <div v-if="isGuarantor">
        <div>
          <textarea v-model="guarantor_notes" readonly></textarea>
        </div>
        <div class="buttons-guarantor">
          <button @click="closeGuarantor">Close</button>
        </div>
      </div>
      <div v-else-if="isRegistered">
        <div>
          <textarea v-model="instructor_notes"></textarea>
        </div>
        <div class="buttons">
          <button @click="register">Save changes</button>
          <button @click="closeInstructor">Close</button>
        </div>
      </div>
      <div v-else>
        <div>
          <textarea v-model="instructor_notes" placeholder="Enter notes..."></textarea>
        </div>
        <div class="buttons">
          <button @click="register">Register activity</button>
          <button @click="closeInstructor">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    activity: {
      type: Object,
      required: true
    },
    isGuarantor: {
      type: Boolean,
      required: true
    },
    isRegistered: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      // Initialize instructor_notes and guarantor_notes with values from the activity prop
      instructor_notes: this.activity.instructor_notes,
      guarantor_notes: this.activity.guarantor_notes
    };
  },
  methods: {

    // Method to register the activity with the provided notes
    register() {
      if (this.instructor_notes === null)
      {
        this.instructor_notes="";
      }
      // Emit the 'register-activity' event with the activity and notes data
      this.$emit('register-activity', { activity: this.activity, notes: this.instructor_notes });
      this.closeInstructor();
    },

    // Method to close the instructor modal
    closeInstructor() {
      this.$emit('close-modal');
    },
    // Method to close the guarantor modal
    closeGuarantor()
    {
      this.$emit('close-guarantor-modal');
    }
  },
};
</script>
<style scoped>

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
}

textarea {
  width: 100%;
  height: 100px;
  margin-bottom: 10px;
  font-size: 20px;
}

.buttons {
  display: flex;
  justify-content: space-between;
}

.buttons-guarantor {
  display: flex;
  justify-content: center;
}

button {
  font-size: 20px;
  padding: 10px 20px;
  border-radius: 5px;
  border: 2px solid black;
  cursor: pointer;
  margin-left: 5px;
  margin-right: 5px;
}

button:first-child {
  background-color: #00cc00;
  color: white;
}

button:last-child {
  background-color: #ff3300;
  color: white;
}
</style>
