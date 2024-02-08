<!--@authors-->
<!--xklima34, Aliaksei Klimau-->
<!--@file UserProfileCard.vue-->
<!--@brief Instructor registered activities schedule view-->

<template>
  <div class="card">
    <div class="container">
      <div class="cross-row">
        <div class="cross" @click=closeProfile>
          <Cross></Cross>
        </div>
      </div>
      <div class="content-row">
        <div class="profile-image">
          <ProfileImage></ProfileImage>
        </div>
        <div class="profile-descr">
          <p class="profile-descr__name">
            <span class="profile-descr__bold">Name: </span>
            <span>{{user.first_name + ' '}}</span>
            <span>{{user.last_name}}</span>
          </p>
          <p class="profile-descr__username">
            <span class="profile-descr__bold">Username: </span>
            <span>{{user.username}}</span>
          </p>
          <p class="profile-descr__email">
            <span class="profile-descr__bold">Email: </span>
            <span>{{user.email}}</span>
          </p>
          <p class="profile-descr__role">
            <span class="profile-descr__bold">Role: </span>
            <span>{{user.permission.description}}</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
<script setup>

import ProfileImage from "@/components/icons/ProfileImage.vue";
import Checkmark from "@/components/icons/Checkmark.vue";
import Cross from "@/components/icons/Cross.vue";
import IconNoteText from "@/components/icons/IconNoteText.vue";
</script>
<script>
export default {
  components: {Checkmark, Cross, IconNoteText},

  props: {
    // User whose profile card is being displayed
    user: {
      type: Object,
      required: true
    }
  },

  methods: {
    // Method for closing progile card
    closeProfile(){
      this.$emit("close-user-profile");
    }
  }
}
</script>

<style scoped>

.card {
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

.container {
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 10px 20px 30px;
  min-width: 700px;
  min-height: 250px;
  border-radius: 20px;
}
.cross-row {
  width: 100%;
  display: flex;
  position: relative;
  justify-content: end;
}

.cross{
  display: flex;
  position: relative;
  justify-content: end;
  align-items: end;
}

.content-row{
  display: flex;
  flex-flow: row;
  font-size: x-large;
  gap: 50px;
}

.profile-image{
  width: 30%;
  justify-content: center;
}

.profile-descr{
  display: flex;
  flex-flow: column;
  gap: 15px;
  justify-content: center;
}

p {
  margin: 0;
}
.profile-descr__bold{
  font-weight: bold;
}
</style>