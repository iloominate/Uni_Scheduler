<template>
    <header>
        <Navigation />
    </header>

    <main>
        <div class="admin">
            <div>
                <div class="title">
                    <h2>User</h2>
                    <img src="../assets/add-item.svg" alt="" @click="NewUser">
                </div>
                <UserList 
                    v-if="isUserLoad && isUserListOpen"
                    :userArray="userArray"
                    @edit-user="EditUser"
                />
                <CreateUser
                    v-if="permissions.length > 0 && isCerateUserOpen"
                    :permissions="permissions"
                    @back="UserBack"
                    @create-user="CreateUser"
                />
                <UserUpdateDelete
                    v-if="isUserLoad && permissions.length > 0 && isUpdateDeleteUserOpen"
                    :user="user"
                    :permissions="permissions"
                    @back="UserBack"
                    @update-user="UpdateUser"
                    @delete-user="DeleteUser"
                />
            </div>
            <div>
                <div class="title">
                    <h2>Subject</h2>
                    <img src="../assets/add-item.svg" alt="" @click="NewSubject">
                </div>
                <SubjectList 
                    v-if="isSubjectLoad && isSubjectListOpen"
                    :subjectArray="subjectArray"
                    @edit-subject="EditSubject"
                />
                <CreateSubject
                    v-if="isCerateSubjectOpen"
                    :guarantors="guarantors"
                    @back="SubjectBack"
                    @create-subject="CreateSubject"
                />
                <SubjectUpdateDelete
                    v-if="isSubjectLoad && isUpdateDeleteSubjectOpen"
                    :subject="subject"
                    :guarantors="guarantors"
                    @back="SubjectBack"
                    @update-subject="UpdateSubject"
                    @delete-subject="DeleteSubject"
                />
            </div>
            <div>
                <div class="title">
                    <h2>Room</h2>
                    <img src="../assets/add-item.svg" alt="" @click="NewRoom">
                </div>
                <RoomList 
                    v-if="isRoomLoad && isRoomListOpen"
                    :roomArray="roomArray"
                    @edit-room="EditRoom"
                />
                <CreateRoom
                    v-if="isCerateRoomOpen"
                    @back="RoomBack"
                    @create-room="CreateRoom"
                />
                <RoomUpdateDelete
                    v-if="isRoomLoad && isUpdateDeleteRoomOpen"
                    :room="room"
                    @back="RoomBack"
                    @update-room="UpdateRoom"
                    @delete-room="DeleteRoom"
                />
            </div>
        </div>
    </main>
</template>
  
<script>
/**
 * @authors
 *   xmyron00, Yurii Myronov
 *
 * @file Admin.vue
 * @brief Admin view
 */
import Navigation from '../components/Navigation.vue';

import UserList from '../components/admin/UserList.vue';
import CreateUser from '../components/admin/CreateUser.vue';
import UserUpdateDelete from '../components/admin/UserUpdateDelete.vue';

import SubjectList from '../components/admin/SubjectList.vue';
import CreateSubject from '../components/admin/CreateSubject.vue';
import SubjectUpdateDelete from '../components/admin/SubjectUpdateDelete.vue';

import RoomList from '../components/admin/RoomList.vue';
import CreateRoom from '../components/admin/CreateRoom.vue';
import RoomUpdateDelete from '../components/admin/RoomUpdateDelete.vue';

import axios from 'axios';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
    emits: [
        "edit-user", "back", "create-user", "update-user", "delete-user",
        "edit-subject", "create-subject", "update-subject", "delete-subject",
        "edit-room", "create-room", "update-room", "delete-room"
    ],
    data() {
        return{
            header: {
                "Authorization": localStorage.getItem("token"),
            },

            user: {},
            permissions: [],
            userArray: [],
            guarantors: [],

            isUserListOpen: true,
            isCerateUserOpen: false,
            isUpdateDeleteUserOpen: false,
            isUserLoad: false,

            subjectArray: [],
            subject: {},

            isSubjectListOpen: true,
            isCerateSubjectOpen: false,
            isUpdateDeleteSubjectOpen: false,
            isSubjectLoad: false,

            roomArray: [],
            room: {},

            isRoomListOpen: true,
            isCerateRoomOpen: false,
            isUpdateDeleteRoomOpen: false,
            isRoomLoad: false,
        }
    },
    components: {
        Navigation,

        UserList,
        CreateUser,
        UserUpdateDelete,

        SubjectList,
        CreateSubject,
        SubjectUpdateDelete,

        RoomList,
        CreateRoom,
        RoomUpdateDelete
    },
    mounted() {
        this.GetUserList();

        axios.get(`${import.meta.env.VITE_API_HOST}/permission`, {headers: this.header})
        .then(response => {
            this.permissions = response.data.data;
        })
        .catch(error => {
            for (const key in error.response.data.errors) {
                if (error.response.data.errors.hasOwnProperty(key)) {
                    const errorDes = error.response.data.errors[key];
                    const errorMessage = `${key}: ${errorDes}`;
    
                    toast.error(errorMessage, {
                        autoClose: 3000,
                        position: toast.POSITION.BOTTOM_LEFT,
                    });
                }
            }
        });

        this.GetSubjectList();
        this.GetRoomList();
    },
    methods: {
        GetUserList(){
            axios.get(`${import.meta.env.VITE_API_HOST}/user`, {headers: this.header})
            .then(response => {
                this.userArray = response.data.data;
                this.userArray.sort((a, b) => {
                    const nameA = a.first_name.toUpperCase();
                    const nameB = b.first_name.toUpperCase();

                    if (nameA < nameB) {
                    return -1;
                    }

                    if (nameA > nameB) {
                    return 1;
                    }

                    return 0;
                });
                this.guarantors = this.userArray.filter(user => user.permission.level === 2);
                this.GetGuarantors();
                this.isUserLoad = true;
            })
            .catch(error => {
                for (const key in error.response.data.errors) {
                    if (error.response.data.errors.hasOwnProperty(key)) {
                        const errorDes = error.response.data.errors[key];
                        const errorMessage = `${key}: ${errorDes}`;
        
                        toast.error(errorMessage, {
                            autoClose: 3000,
                            position: toast.POSITION.BOTTOM_LEFT,

                        });
                    }
                }
            });
        },
        UserBack() {
            this.GetUserList();
            this.isUserListOpen = true;
            this.isCerateUserOpen = false;
            this.isUpdateDeleteUserOpen = false;
        },
        NewUser() {
            this.isUserListOpen = false;
            this.isCerateUserOpen = true;
            this.isUpdateDeleteUserOpen = false;
        },
        CreateUser() {
            this.GetUserList();
            this.GetGuarantors();
            this.isUserListOpen = true;
            this.isCerateUserOpen = false;
            this.isUpdateDeleteUserOpen = false;
        },
        EditUser(user){
            this.user = user;
            this.isUserListOpen = false;
            this.isCerateUserOpen = false;
            this.isUpdateDeleteUserOpen = true;
        },
        UpdateUser(){
            this.GetUserList();
            this.GetGuarantors();
            this.isUserListOpen = true;
            this.isCerateUserOpen = false;
            this.isUpdateDeleteUserOpen = false;
        },
        DeleteUser(id){
            axios.delete(`${import.meta.env.VITE_API_HOST}/user/${id}`, {headers: this.header})
            .then(response => {
                this.GetUserList();
                this.isUserListOpen = true;
                this.isCerateUserOpen = false;
                this.isUpdateDeleteUserOpen = false;
                toast.success("Delete user is success!", {
                    autoClose: 3000,
                    position: toast.POSITION.BOTTOM_RIGHT
                });
            })
            .catch(error => {
                for (const key in error.response.data.errors) {
                    if (error.response.data.errors.hasOwnProperty(key)) {
                        const errorDes = error.response.data.errors[key];
        
                        toast.error(errorDes, {
                            autoClose: 3000,
                            position: toast.POSITION.BOTTOM_RIGHT,
                        });
                    }
                }
            });
        },
        GetGuarantors(){
            this.guarantors = this.guarantors.filter(guarantor => {
                const existsInSubjectArray = this.subjectArray.some(subject => {
                    return subject.guarantor.id === guarantor.id;
                });

                return !existsInSubjectArray;
            });
        },

        GetSubjectList() {
            axios.get(`${import.meta.env.VITE_API_HOST}/subject`, {headers: this.header})
            .then(response => {
                this.subjectArray = response.data.data;
                this.subjectArray.sort((a, b) => {
                    const nameA = a.code.toUpperCase();
                    const nameB = b.code.toUpperCase();

                    if (nameA < nameB) {
                    return -1;
                    }

                    if (nameA > nameB) {
                    return 1;
                    }

                    return 0;
                });
                this.isSubjectLoad = true;

                this.GetGuarantors();
            })
            .catch(error => {
                for (const key in error.response.data.errors) {
                    if (error.response.data.errors.hasOwnProperty(key)) {
                        const errorDes = error.response.data.errors[key];
                        const errorMessage = `${key}: ${errorDes}`;
        
                        toast.error(errorMessage, {
                            autoClose: 3000,
                            position: toast.POSITION.BOTTOM_LEFT,
                        });
                    }
                }
            });
        },
        SubjectBack() {
            this.isSubjectListOpen = true;
            this.isCerateSubjectOpen = false;
            this.isUpdateDeleteSubjectOpen = false;
        },
        NewSubject() {
            this.isSubjectListOpen = false;
            this.isCerateSubjectOpen = true;
            this.isUpdateDeleteSubjectOpen = false;
        },
        CreateSubject(subject) {
            this.GetSubjectList();
            this.GetGuarantors();
            this.isSubjectListOpen = true;
            this.isCerateSubjectOpen = false;
            this.isUpdateDeleteSubjectOpen = false;
        },
        EditSubject(subject) {
            this.subject = subject;
            this.isSubjectListOpen = false;
            this.isCerateSubjectOpen = false;
            this.isUpdateDeleteSubjectOpen = true;
        },
        UpdateSubject() {
            this.GetSubjectList();
            this.isSubjectListOpen = true;
            this.isCerateSubjectOpen = false;
            this.isUpdateDeleteSubjectOpen = false;
        },
        DeleteSubject(id){
            axios.delete(`${import.meta.env.VITE_API_HOST}/subject/${id}`, {headers: this.header})
            .then(response => {
                this.GetSubjectList();
                this.GetGuarantors();
                this.isSubjectListOpen = true;
                this.isCerateSubjectOpen = false;
                this.isUpdateDeleteSubjectOpen = false;
                toast.success("Delete subject is success!", {
                    autoClose: 3000,
                    position: toast.POSITION.BOTTOM_LEFT
                });
            })
            .catch(error => {
                for (const key in error.response.data.errors) {
                    if (error.response.data.errors.hasOwnProperty(key)) {
                        const errorDes = error.response.data.errors[key];
                        const errorMessage = `${key}: ${errorDes}`;
        
                        toast.error(errorMessage, {
                            autoClose: 3000,
                            position: toast.POSITION.BOTTOM_LEFT,
                        });
                    }
                }
            });
        },

        GetRoomList() {
            axios.get(`${import.meta.env.VITE_API_HOST}/room`, {headers: this.header})
            .then(response => {
                this.roomArray = response.data.data;
                this.roomArray.sort((a, b) => a.number - b.number);
                this.isRoomLoad = true;
            })
            .catch(error => {
                for (const key in error.response.data.errors) {
                    if (error.response.data.errors.hasOwnProperty(key)) {
                        const errorDes = error.response.data.errors[key];
                        const errorMessage = `${key}: ${errorDes}`;
        
                        toast.error(errorMessage, {
                            autoClose: 3000,
                            position: toast.POSITION.BOTTOM_LEFT,
                        });
                    }
                }
            });
        },
        RoomBack() {
            this.isRoomListOpen = true;
            this.isCerateRoomOpen = false;
            this.isUpdateDeleteRoomOpen = false;
        },
        NewRoom() {
            this.isRoomListOpen = false;
            this.isCerateRoomOpen = true;
            this.isUpdateDeleteRoomOpen = false;
        },
        CreateRoom() {
            this.GetRoomList();
            this.isRoomListOpen = true;
            this.isCerateRoomOpen = false;
            this.isUpdateDeleteRoomOpen = false;
        },
        EditRoom(room) {
            this.room = room;
            this.isRoomListOpen = false;
            this.isCerateRoomOpen = false;
            this.isUpdateDeleteRoomOpen = true;
        },
        UpdateRoom() {
            this.GetRoomList();
            this.isRoomListOpen = true;
            this.isCerateRoomOpen = false;
            this.isUpdateDeleteRoomOpen = false;
        },
        DeleteRoom(id){
            axios.delete(`${import.meta.env.VITE_API_HOST}/room/${id}`, {headers: this.header})
            .then(response => {
                this.GetRoomList();
                this.isRoomListOpen = true;
                this.isCerateRoomOpen = false;
                this.isUpdateDeleteRoomOpen = false;
                toast.success("Delete room is success!", {
                    autoClose: 3000,
                    position: toast.POSITION.BOTTOM_LEFT
                });
            })
            .catch(error => {
                for (const key in error.response.data.errors) {
                    if (error.response.data.errors.hasOwnProperty(key)) {
                        const errorDes = error.response.data.errors[key];
                        const errorMessage = `${key}: ${errorDes}`;
        
                        toast.error(errorMessage, {
                            autoClose: 3000,
                            position: toast.POSITION.BOTTOM_LEFT,
                        });
                    }
                }
            });
        },
    }
};
</script>

<style scoped>

template {
    max-height: 100%;
}

.admin {
    margin: 20px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    align-content: start;
}

.admin > div {
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    height: fit-content;
}

.title {
    display: flex;
    align-items: center;
    justify-content: center;
}

h2 {
    margin: 10px;
}

img {
    width: 25px;
    height: 25px;
}

img:hover{
    cursor: pointer;
}

</style>

