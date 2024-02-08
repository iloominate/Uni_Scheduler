<template>
    <form>
        <div>
            <p>Code</p>
            <input type="text" v-model="update_subject.code" :class="{ 'invalid': errors.code }"/>
            <ul v-if="errors.code" style="color: red;">
                <li v-for="error in errors.code">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>Name</p>
            <input type="email" v-model="update_subject.name" :class="{ 'invalid': errors.name }"/>
            <ul v-if="errors.name" style="color: red;">
                <li v-for="error in errors.name">{{ error }}</li>
            </ul>
        </div>
        <div>
            <p>Description</p>
            <input type="text" v-model="update_subject.description" :class="{ 'invalid': errors.description }"/>
            <ul v-if="errors.description" style="color: red;">
                <li v-for="error in errors.description">{{ error }}</li>
            </ul>
        </div>

        <div class="btns">
            <button @click.prevent="Back">Back</button>
            <button @click.prevent="UpdateSubject">Update</button>
            <button @click.prevent="DeleteSubject">Delete</button>
        </div>
    </form>
</template>

<script>
/**
 * @authors
 *   xmyron00, Yurii Myronov
 *
 * @file SubjectUpdateDelete.vue
 * @brief Component for update or delete subject
 */

import axios from 'axios';
import { toast } from 'vue3-toastify';

export default {
    props: {
        subject: {
            type: Object,
            default: {}
        },
    },
    data() {
        return {
            update_subject: {
                code: this.subject.code,
                name: this.subject.name,
                description: this.subject.description,
                guarantor_id : this.subject.guarantor.id,
            },

            header: {
                "Authorization": localStorage.getItem("token"),
            },

            errors: {
                code: null,
                name: null,
                description: null,
                guarantor_id: null,
            },
        }
    },
    methods: {
        Back() {
            this.$emit("back");
        },
        UpdateSubject() {
            const id = this.subject["id"];
            axios.put(`${import.meta.env.VITE_API_HOST}/subject/${id}`, this.update_subject, {headers: this.header})
            .then(response => {
                this.$emit('update-subject');
                toast.success("Update subject is success!", {
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
        DeleteSubject() {
            this.$emit('delete-subject', this.subject["id"]);
        },
        selectValue(guarantor) {
            this.selectedGuarantor = guarantor.username;
            this.selectedGuarantorID = guarantor.id;
            this.isGuarantorOpen = false;
        }
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