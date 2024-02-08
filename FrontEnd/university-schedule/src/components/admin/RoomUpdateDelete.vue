<template>
    <form>
        <div>
            <p>Number:</p>
            <input type="text" v-model="updated_room.number" :class="{ 'invalid': errors.number }"/>
            <ul v-if="errors.number" style="color: red;">
                <li v-for="error in errors.number">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>Description:</p>
            <input type="email" v-model="updated_room.description" :class="{ 'invalid': errors.description }"/>
            <ul v-if="errors.description" style="color: red;">
                <li v-for="error in errors.description">{{ error }}</li>
            </ul>
        </div>

        <div class="btns">
            <button @click.prevent="Back">Back</button>
            <button @click.prevent="UpdateRoom">Update</button>
            <button @click.prevent="DeleteRoom">Delete</button>
        </div>
    </form>
</template>

<script>
/**
 * @authors
 *   xmyron00, Yurii Myronov
 *
 * @file RoomUpdateDelete.vue
 * @brief Component for update or delete room
 */

import axios from 'axios';
import { toast } from 'vue3-toastify';

export default {
    data() {
        return {
            updated_room: {
                number: this.room.number,
                description: this.room.description,
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
    props: {
        room: {
            type: Object,
            default: {}
        },
    },
    methods: {
        Back() {
            this.$emit("back");
        },
        UpdateRoom() {
            if (!isNaN(parseInt(this.room.number, 10))) {
                this.room.number = parseInt(this.room.number, 10);
            }
            const id = this.room["id"];
            Object.keys(this.errors).forEach(key => {
                this.errors[key] = null;
            });
            axios.put(`${import.meta.env.VITE_API_HOST}/room/${id}`, this.updated_room, {headers: this.header})
            .then(response => {
                this.$emit('update-room', id, this.room);
                toast.success("Update room is success!", {
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
        },
        DeleteRoom() {
            this.$emit('delete-room', this.room["id"]);
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

ul {
    margin: 5px;
    padding-left: 20px;
    font-size: 14px;
}

.invalid {
  border-color: red;
}

</style>