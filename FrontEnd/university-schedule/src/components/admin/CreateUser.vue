<template>
    <form>
        <div>
            <p>Username <span style="color: red;">*</span></p>
            <input type="text" v-model="user.username" :class="{ 'invalid': errors.username }"/>
            <ul v-if="errors.username" style="color: red;">
                <li v-for="error in errors.username">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>Email <span style="color: red;">*</span></p>
            <input type="email" v-model="user.email" :class="{ 'invalid': errors.email }"/>
            <ul v-if="errors.email" style="color: red;">
                <li v-for="error in errors.email">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>Password  <span style="color: red;">*</span></p>
            <div class="password">
                <input class="password-input" :type="showPassword ? 'text' : 'password'" v-model="user.password" :class="{ 'invalid': errors.password }"/>
                <img v-if="showPassword" @click="togglePasswordVisibility" src="../../assets/Eye.svg" alt="Hide Password" />
                <img v-else @click="togglePasswordVisibility" src="../../assets/EyeOff.svg" alt="Show Password" />
            </div>
            <ul v-if="errors.password" style="color: red;">
                <li v-for="error in errors.password">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>First name <span style="color: red;">*</span></p>
            <input type="text" v-model="user.first_name" :class="{ 'invalid': errors.first_name }"/>
            <ul v-if="errors.first_name" style="color: red;">
                <li v-for="error in errors.first_name">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>Last name <span style="color: red;">*</span></p>
            <input type="text" v-model="user.last_name" :class="{ 'invalid': errors.last_name }"/>
            <ul v-if="errors.last_name" style="color: red;">
                <li v-for="error in errors.last_name">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>Permission <span style="color: red;">*</span></p>
            <div class="custom-select" @click.stop="toggleDropdownPermission" :style="{'color': selectedPermission ? 'initial' : 'rgb(0,0,0,0.5)'}" :class="{ 'invalid': errors.permission_id }">
                {{ selectedPermission || 'Permission' }}
                <div v-if="isPermissionOpen" class="dropdown" ref="dropdown" @click.stop>
                <div v-for="permission in permissions" :key="permission.description" @click="selectValue(permission)">
                    {{ permission.description }}
                </div>
                </div>
            </div>
            <ul v-if="errors.permission_id" style="color: red;">
                <li v-for="error in errors.permission_id">{{ error }}</li>
            </ul>
        </div>

        <div class="btns">
            <button @click.prevent="Back">Back</button>
            <button @click.prevent="CreateUser">Create</button>
        </div>
    </form>
</template>

<script>
/**
 * @authors
 *   xmyron00, Yurii Myronov
 *
 * @file CreateUser.vue
 * @brief Component for create user
 */

import axios from 'axios';
import { toast } from 'vue3-toastify';

export default {
    data() {
        return {
            user: {
                username: '',
                email: '',
                password: '',
                first_name: '',
                last_name: '',
                permission_id : null,
            },
            isPermissionOpen: false,
            selectedPermission: null,
            showPassword: false,

            errors: {
                username: null,
                email: null,
                password: null,
                first_name: null,
                last_name: null,
                permission_id: null,
            },

            header: {
                "Authorization": localStorage.getItem("token"),
            },
        }
    },
    props: {
        permissions: {
            type: Array,
            default: []
        }
    },
    methods: {
        Back() {
            this.$emit("back");
        },
        CreateUser() {
            Object.keys(this.errors).forEach(key => {
                this.errors[key] = null;
            });
            axios.post(`${import.meta.env.VITE_API_HOST}/user`, this.user, {headers: this.header})
            .then(response => {
                this.$emit("create-user");
                toast.success("Create user is success!", {
                    autoClose: 3000,
                    position: toast.POSITION.BOTTOM_RIGHT
                });
            })
            .catch(error => {
                const serverErrors = error.response.data.errors;
                Object.keys(serverErrors).forEach(key => {
                    this.errors[key] = serverErrors[key];
                });
            });
        },
        toggleDropdownPermission() {
            this.isPermissionOpen = !this.isPermissionOpen;
        },
        selectValue(permission) {
            this.selectedPermission = permission.description;
            this.isPermissionOpen = false;
            this.user.permission_id = permission.id;
        },
        togglePasswordVisibility() {
            this.showPassword = !this.showPassword;
        },
    }
}

</script>

<style scoped>

form > div {
    border-radius: 10px;
    margin: 20px 10px;
}

form > div > p {
    margin: 10px 0px;
}

form > div > input {
    width: 100%;
    padding: 5px;
    font-size: 16px;
    border: 1px solid rgb(0, 0, 0, 0.4);
    border-radius: 5px;
}

.btns {
    display: flex;
    justify-content: end;
    gap: 10px;
}

.btns > button {
    font-size: 18px;
    padding: 7px 20px;
    border: none;
    color: white;
    font-weight: 600;
    border-radius: 7px;
}

.btns > button:first-child {
    background-color: #00A7FF;
}

.btns > button:first-child:hover {
    background-color: #45BFFF;
    cursor: pointer;
}

.btns > button:last-child {
    background-color: #70C784;
}

.btns > button:last-child:hover {
    background-color: #84D296;
    cursor: pointer;
}

.custom-select {
    position: relative;
    display: flex;
    border: 1px solid rgb(0, 0, 0, 0.4);
    border-radius: 5px;
    cursor: pointer;
    width: 100%;
    padding: 5px;
    font-size: 16px;
    color: rgb(0, 0, 0);
}

.dropdown {
  background-color: white;
  position: absolute;
  top: 100%;
  padding: 0px 7px;
  width: fit-content;
  border: 1px solid rgb(0, 0, 0, 0.2);
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  outline: none;
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


.password {
    position: relative;
}

.password-input {
    display: flex;
    justify-content: space-between;
    width: 100%;
    padding: 5px;
    border: 1px solid rgb(0, 0, 0, 0.4);
    border-radius: 5px;
    font-size: 16px;
}

.password > img {
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
}

ul {
    margin: 5px;
    padding-left: 20px;
    font-size: 14px;
}

.invalid {
  border-color: red;
}

</style>