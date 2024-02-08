<!--@authors-->
<!--xrasst00, Sergei Rasstrigin-->

<!--@file GuarantorActivities.vue-->
<!--@brief Guarantor manage activities view-->

<template>
  <navigation
      class="nav-bar"
  >
  </navigation>
  <div class="main-container">
    <div class="request-container">
      <div class="title">
        <div class="title__body">Unresolved requests</div>
      </div>
      <div class="list__request">
        <div class="list_body">
          <guarant-request
              v-for="request in requests"
              :key="request.id"
              :request="request"
              :subject="guarantorSubject"
              @deleteRequest="deleteRequest"
          ></guarant-request>
        </div>
      </div>
      <div class="request__form">
        <div class="form-box">
          <div class="select-type">
            <div class="input-label">Type:</div>
            <select class="custom-select" v-model="selectedType">
              <option
                  v-for="typeOption in typeOptions"
                  :key="typeOption.value"
                  :value="typeOption.value"
              >
                {{ typeOption.text }}
              </option>
            </select>
          </div>

          <div class="select-duration">
            <div class="input-label">Duration:</div>
            <select class="custom-select" v-model="selectedDuration">
              <option
                  v-for="duration in durationOptions"
                  :key="duration.value"
                  :value="duration.value"
              >
                {{ duration.text }}
              </option>
            </select>
          </div>

          <div class="select-repeating">
            <div class="input-label">Repeating:</div>
            <select class="custom-select" v-model="selectedRepeating">
              <option
                  v-for="repeating in repeatingOptions"
                  :key="repeating.value"
                  :value="repeating.value"
              >
                {{ repeating.text }}
              </option>
            </select>
          </div>
          <div class="select-date">
            <div class="input-date">
              <div class="input-label">
                Date:
              </div>

              <VDatePicker
                  v-model="range"
                  is-range
                  :masks="masks"
                  v-model.string="customer.birthday"
              >
                <template #default="{ inputValue, inputEvents }">
                  <div>
                    <input
                        :value="inputValue.start"
                        v-on="inputEvents.start"
                        class="custom-select custom-date"
                        placeholder="Date from"
                    />
                    <input
                        :value="inputValue.end"
                        v-on="inputEvents.end"
                        class="custom-date custom-select"
                        placeholder="Date to"
                    />
                  </div>
                </template>
              </VDatePicker>
            </div>
          </div>

          <div class="notes">
            <div class="notes-label">Notes:</div>
            <textarea class="custom-textarea" v-model="notes"></textarea>
          </div>
        </div>
      </div>
      <div class="send__request">
        <div class="send_body" @click="sendRequest">Add request</div>
      </div>
    </div>
  </div>


</template>

<script>

import Navigation from "@/components/Navigation.vue";
import GuarantRequest from "@/components/GuarantRequest.vue";
import axios from "axios";
import {reactive, ref} from "vue";
import Cross from "@/components/icons/Cross.vue";
import {toast} from "vue3-toastify";


export default {
  components: {Cross, GuarantRequest, Navigation},
  data(){
    return{
      masks: ref({
        modelValue: 'YYYY-MM-DD',
      }),
      customer: reactive({
        name: 'Nathan Reyes',
        birthday: '1983-01-21',
      }),

      range: ref(null),
      header: {
        "Authorization": localStorage.getItem("token"),
      },
      selectedType: 0,
      typeOptions : [
        {text: 'Lecture', value: 1},
        {text: 'Exercise', value: 2},
        {text: 'Laboratory', value: 3},
        {text: 'Exam', value: 4}
      ],
      selectedDuration: 0,
      durationOptions : [
        {text: '1 hour', value: 1},
        {text: '2 hour', value: 2},
        {text: '3 hour', value: 3},
        {text: '4 hour', value: 4},
      ],
      selectedRepeating: 0,
      repeatingOptions : [
        {text: 'Every week', value: 1},
        {text: 'One time', value: 4},
        {text: 'Odd week', value: 3},
        {text: 'Even week', value: 2},
      ],
      notes: '',
      requests: {},
      guarantorSubject: {},
      selectedDate: null,
    }
  },
  methods:{
    /**
     * Sends a request to create a new activity entry.
     */
    sendRequest(){
      const dataToSend = {
        "guarantor_notes": this.notes,
        "duration": this.selectedDuration,
        "activity_type_id": this.selectedType,
        "subject_id": this.guarantorSubject.id, // CHANGE TO DYNAMIC {FOR TEST}
        "date_from": this.range.start,
        "date_to": this.range.end,
        "activity_repetition_id": this.selectedRepeating,
      };
      axios.post(`${import.meta.env.VITE_API_HOST}/activity`, dataToSend, {headers: this.header})
          .then(response=>{
            this.getRequests()
            toast.success("Request was successfully created!", {
              autoClose: 5000,
              position: toast.POSITION.BOTTOM_RIGHT,
            });
          })
          .catch(error=>{
            let message = error.response.data.detail.replace(/['\[\]]/g, '');
            toast.error(message, {
              autoClose: 5000,
              position: toast.POSITION.BOTTOM_LEFT,
            });
          });

      this.selectedRepeating = 0;
      this.selectedDuration = 0;
      this.selectedType = 0;
      this.notes = '';
      this.range = ref(null);

    },
    /**
     * Retrieves the list of requests for display.
     */
    async getRequests(){
      // change to subject id
      await axios.get(`${import.meta.env.VITE_API_HOST}/get_requests/${this.guarantorSubject.id}`, {headers: this.header})
          .then(response=>{
            this.requests = response.data.data;
          })
          .catch(error=>{
            console.log(error)
          });
    },
    /**
     * Retrieves information about the subject.
     */
    getSubject(){
      try {
        // change to user.id
        const storedSubject = localStorage.getItem('subject');
        if(storedSubject) {
          this.guarantorSubject = JSON.parse(storedSubject);
        }

      }catch (e) {
        console.log(e);
      }
    },
    /**
     * Deletes a request.
     * @param {Object} activity - The activity to be deleted.
     */
    async deleteRequest(activity){
      await axios.delete(`${import.meta.env.VITE_API_HOST}/activity/${activity.id}`, {headers: this.header})
          .then(response=>{
            this.getRequests();
            toast.success("Request was successfully deleted!", {
              autoClose: 5000,
              position: toast.POSITION.BOTTOM_RIGHT,
            });
          })
          .catch(error=>{
            let message = error.response.data.detail.replace(/['\[\]]/g, '');
            toast.error(message, {
              autoClose: 5000,
              position: toast.POSITION.BOTTOM_LEFT,
            });
          })

    }

  },
  async mounted() {
    this.getSubject();
    await this.getRequests();
  }
}
</script>

<style scoped>
.main-container{
  background: none;
  display: flex;
  height: 108vh;
  justify-content: center;
}
.request-container{
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 95%;
  width: 60%;
  background: white;
  border-radius: 10px;
  border: 3px solid black;
}
.title{
  width: 100%;
  height: 7%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
}
.list__request{
  width: 100%;
  height: 23%;
  display: flex;
  justify-content: center;
}
.list_body{
  background: #eea15a;
  border-radius: 10px;
  display: flex;
  height: 100%;
  width: 90%;
  padding-left: 10px;
  justify-content: left;
  align-items: center;
  overflow: auto;
  border: 2px solid black;
}
.request__form{
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
}
.send__request{
  width: 100%;
  height: 8%;
}
.form-box{
  height: 95%;
  width: 50%;
  background: #eea15a;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  border: 2px solid black;
}
.list_body::-webkit-scrollbar {
  width: 1px;
}

.list_body::-webkit-scrollbar-track {
  background-color: #d3d3d3;
  border: none;
  border-radius: 5px;
}

.list_body::-webkit-scrollbar-thumb {
  background-color: black;
  border-radius: 10px;
  border: 3px solid #d3d3d3;
  height: 100%;
}
.select-type{
  margin-top: 8px;
  width: 100%;
  height: 15%;
  display: flex;
  flex-direction: column;
  justify-items: center;
  font-size: 24px;
  font-weight: bold;
}
.select-duration{
  display: flex;
  flex-direction: column;
  justify-items: center;
  font-size: 24px;
  font-weight: bold;
  width: 100%;
  height: 15%;
  margin-top: 10px;
}
.select-repeating{
  width: 100%;
  height: 15%;
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  justify-items: center;
  font-size: 24px;
  font-weight: bold;
}
.select-date{
  width: 100%;
  height: 15%;
  display: flex;
  margin-top: 10px;
  flex-direction: column;
  font-size: 24px;
  font-weight: bold;
}
.notes{
  flex-grow: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  font-size: 24px;
  font-weight: bold;
  margin-top: 3px;
}
.input-label{
  margin-left: 5%;
}
.custom-select{
  width: 90%;
  align-self: center;
  height: 35px;
  border: 2px solid black;
  font-size: 22px;
  cursor: pointer;
}
.notes-label{
  margin-left: 5%
}
.custom-textarea {
  width: 85%;
  height: 40%;
  border: 2px solid black;
  resize: none;
  font-size: 19px;
  align-self: center;
  padding: 10px;
}
.send__request{
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 25px;
}
.send_body{
  margin-top: 3px;
  border-bottom: 2px solid black;
  cursor: pointer;
}
.input-date{
  display: flex;
  flex-direction: column;
  align-items: start;
}
.custom-date{
  margin-left: 5.1%;
  height: 25px;
  width: 40.7%;
}

</style>