<template>
    <form>
        <div>
            <p>Number <span style="color: red;">*</span></p>
            <input type="text" v-model="room.number" :class="{ 'invalid': errors.number }"/>
            <ul v-if="errors.number" style="color: red;">
                <li v-for="error in errors.number">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>Description:</p>
            <input type="email" v-model="room.description" :class="{ 'invalid': errors.description }"/>
            <ul v-if="errors.description" style="color: red;">
                <li v-for="error in errors.description">{{ error }}</li>
            </ul>
        </div>

        <div class="btns">
            <button @click.prevent="Back">Back</button>
            <button @click.prevent="CreateRoom">Create</button>
        </div>
    </form>
</template>

<script>
/**
 * @authors
 *   xmyron00, Yurii Myronov
 *
 * @file CreateRoom.vue
 * @brief Component for create room
 */

import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import axios from 'axios';

export default {
    data() {
        return {
            room: {
                number: '',
                description: '',
            },

            errors: {
                number: null,
                description: null,
            },

            header: {
                "Authorization": localStorage.getItem("token"),
            },
        }
    },
    methods: {
        Back() {
            this.$emit("back");
        },
        CreateRoom() {
            Object.keys(this.errors).forEach(key => {
                this.errors[key] = null;
            });
            if (!isNaN(parseInt(this.room.number, 10))) {
                this.room.number = parseInt(this.room.number, 10);
            }
            axios.post(`${import.meta.env.VITE_API_HOST}/room`, this.room, {headers: this.header})
            .then(response => {
                this.$emit('create-room', this.room);
                toast.success("Create room is success!", {
                    autoClose: 3000,
                    position: toast.POSITION.BOTTOM_LEFT
                });
            })
            .catch(error => {
                const serverErrors = error.response.data.errors;
                Object.keys(serverErrors).forEach(key => {
                    this.errors[key] = serverErrors[key];
                });
            });
        }
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

ul {
    margin: 5px;
    padding-left: 20px;
    font-size: 14px;
}

.invalid {
  border-color: red;
}

</style>