<template>
    <form>
        <div>
            <p>Username:</p>
            <input type="text" v-model="update_user.username" :class="{ 'invalid': errors.username }"/>
            <ul v-if="errors.username" style="color: red;">
                <li v-for="error in errors.username">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>Email:</p>
            <input type="email" v-model="update_user.email" :class="{ 'invalid': errors.email }"/>
            <ul v-if="errors.email" style="color: red;">
                <li v-for="error in errors.email">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>First name:</p>
            <input type="text" v-model="update_user.first_name" :class="{ 'invalid': errors.first_name }"/>
            <ul v-if="errors.first_name" style="color: red;">
                <li v-for="error in errors.first_name">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>Last name:</p>
            <input type="text" v-model="update_user.last_name" :class="{ 'invalid': errors.last_name }"/>
            <ul v-if="errors.last_name" style="color: red;">
                <li v-for="error in errors.last_name">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>Permission:</p>
            <div class="custom-select" @click.stop="toggleDropdownPermission" :class="{ 'invalid': errors.permission_id }">
                {{ selectedPermission }}
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
            <button @click.prevent="UpdateUser">Update</button>
            <button @click.prevent="DeleteUser">Delete</button>
        </div>
    </form>
</template>

<script>
/**
 * @authors
 *   xmyron00, Yurii Myronov
 *
 * @file UserUpdateDelete.vue
 * @brief Component for update or delete user
 */

import axios from 'axios';
import { toast } from 'vue3-toastify';

export default {
    props: {
        user: {
            type: Object,
            default: {}
        },
        permissions: {
            type: Array,
            default: []
        }
    },
    data() {
        return {
            update_user: {
                username: this.user.username,
                email: this.user.email,
                password: this.user.password,
                first_name: this.user.first_name,
                last_name: this.user.last_name,
                permission_id : this.user.permission_id,
            },

            isPermissionOpen: false,
            selectedPermission: this.user.permission.description,
            header: {
                "Authorization": localStorage.getItem("token"),
            },

            errors: {
                username: null,
                email: null,
                password: null,
                first_name: null,
                last_name: null,
                permission_id: null,
            },
        }
    },
    methods: {
        Back() {
            this.$emit("back");
        },
        UpdateUser() {
            const id = this.user["id"];
            const permission = this.permissions.find(p => p.description === this.selectedPermission);
            this.update_user["permission_id"] = permission.id;
            Object.keys(this.errors).forEach(key => {
                this.errors[key] = null;
            });
            axios.put(`${import.meta.env.VITE_API_HOST}/user/${id}`, this.update_user, {headers: this.header})
            .then(response => {
                this.$emit('update-user');
                toast.success("Update user is success!", {
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
        DeleteUser() {
            this.$emit('delete-user', this.user["id"]);
        },
        toggleDropdownPermission() {
            this.isPermissionOpen = !this.isPermissionOpen;
        },
        selectValue(permission) {
            this.selectedPermission = permission.description;
            this.isPermissionOpen = false;
        },
    }
};

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

.btns > button:not(:last-child) {
    background-color: #00A7FF;
}

.btns > button:not(:last-child):hover {
    background-color: #45BFFF;
    cursor: pointer;
}

.btns > button:last-child {
    background-color: #FF6975;
}

.btns > button:last-child:hover {
    background-color: #FF7783;
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

.dropdown div:hover {
  color: rgb(0, 0, 0);
}

.dropdown div:last-child {
  cursor: pointer;
  padding: 7px 0px;
  color: rgb(0, 0, 0, 0.5);
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
}

.password > img {
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(20%);
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