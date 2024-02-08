<template>
    <header>
        <Navigation/>
    </header>

    <main>
        <div class="not-resolved-list">
            <NotResolvedCell 
                v-for="activity in activitiesNotResolved" 
                :key="activity.id" 
                :activity="activity" 
                :rooms="rooms"
                @add-to-calendar="HandleAddToCalendar"
            />
        </div>

        <Calendar
            ref="calendarRef"
            v-if="dataForCalendarReceived"
            :activities="activitiesResolved"
            :is-scheduler="true"
            @remove-from-calendar="HandleRemoveFromCalendar"
        />
    </main>
</template>


<script>
/**
 * @authors
 *   xmyron00, Yurii Myronov
 *
 * @file Scheduler.vue
 * @brief Scheduler view
 */
import Navigation from '../components/Navigation.vue';
import ScheduleCell from '../components/ScheduleCell.vue';
import NotResolvedCell from '../components/NotResolvedCell.vue';
import Calendar from '../components/Calendar.vue';
import axios from 'axios';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
    emits: ["remove-from-calendar", "add-to-calendar"],
    components: {
        Navigation,
        NotResolvedCell,
        ScheduleCell,
        Calendar
    },
    data() {
        return {
            header: {
                "Authorization": localStorage.getItem("token"),
            },

            activitiesNotResolved: [],
            activitiesResolved: [],
            rooms: [],

            dataForCalendarReceived: false,
        };
    },
    methods: {
        GetActivities() {
            this.dataForCalendarReceived = false;
            axios.get(`${import.meta.env.VITE_API_HOST}/schedule-activity`, {headers: this.header})
            .then(response => {
                let activities = response.data.data;
                this.activitiesNotResolved = [];
                this.activitiesResolved = [];
                for (const activity of activities) {
                    if (activity.time === null || activity.room === null || activity.day === null){
                        this.activitiesNotResolved.push(activity);
                    }
                    else {
                        this.activitiesResolved.push(activity);
                    }
                }
                this.dataForCalendarReceived = true;
            })
            .catch(error => {
                console.error('Error response for activity: ', error);
            });
        },
        HandleRemoveFromCalendar(activity) {
            axios.delete(`${import.meta.env.VITE_API_HOST}/scheduler-activity/${activity.id}`, {headers: this.header})
            .then(response => {
                this.GetActivities();
                this.$refs.calendarRef.UpdateCalendar();
                toast.success("Remove from calendar successful!", {
                    autoClose: 3000,
                    position: toast.POSITION.BOTTOM_RIGHT,
                });
            })
            .catch(error => {
                console.log(error);
            });
        },
        HandleAddToCalendar(activity, data) {
            axios.post(`${import.meta.env.VITE_API_HOST}/scheduler-activity/${activity.id}`, data, {headers: this.header})
            .then(response => {
                this.GetActivities();
                this.$refs.calendarRef.UpdateCalendar();
                toast.success("Add to calendar successful!", {
                    autoClose: 3000,
                    position: toast.POSITION.BOTTOM_RIGHT,
                });
            })
            .catch(error => {
                const message = error.response.data[0].replace(/['\[\]]/g, '');
                toast.error(message, {
                    autoClose: 3000,
                    position: toast.POSITION.BOTTOM_LEFT,
                });
            });
        }
    },
    mounted() {
        this.GetActivities();

        axios.get(`${import.meta.env.VITE_API_HOST}/room`, {headers: this.header})
        .then(response => {
            this.rooms = response.data.data;
            this.rooms.sort((a, b) => a.number - b.number);
        })
        .catch(error => {
            console.error('Error response for rooms: ', error);
        });
    }
};

</script>

<style scoped>

.not-resolved-list {
    position: relative;
    margin: 20px;
    background-color: white;
    border-radius: 15px;
    padding: 20px;
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

</style>