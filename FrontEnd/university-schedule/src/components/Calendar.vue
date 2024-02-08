<template>
    <div class="calendar">
        <div class="grid-10">
            <div></div>
            <div>
                <p>8:00</p>
            </div>
            <div>
                <p>9:00</p>
            </div>
            <div>
                <p>10:00</p>
            </div>
            <div>
                <p>11:00</p>
            </div>
            <div>
                <p>12:00</p>
            </div>
            <div>
                <p>13:00</p>
            </div>
            <div>
                <p>14:00</p>
            </div>
            <div>
                <p>15:00</p>
            </div>
            <div>
                <p>16:00</p>
            </div>
        </div>
        <div class="day" v-for="(value, key) in activitiesInCalendar">
            <div>
                <p>{{ key }}</p>
            </div>
            <div class="grid-9">
                <div v-for="sub_mon in value">
                    <div v-for="element in sub_mon" :style="{ 'grid-column': element.from + ' / ' + element.to }">
                        <ScheduleCell
                            :activity="element.activity"
                            :isScheduler="isScheduler"
                            @remove-shedule-cell="handleRemoveScheduleCell"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
/**
 * @authors
 *   xmyron00, Yurii Myronov
 *
 * @file Calendar.vue
 * @brief Component calendar
 */
import ScheduleCell from './ScheduleCell.vue';

export default {
    emits: ["remove-shedule-cell", "remove-from-calendar"],
    components: {
        ScheduleCell,
    },
    props: {
        activities: {
            type: Array,
            default: [],
        },
        isScheduler:{
          type: Boolean,
          default: false,
        }
    },
    data() {
        return {
            activitiesInCalendar: {},
        }
    },
    mounted() {
        this.UpdateCalendar();
    },
    methods: {
        UpdateCalendar() {
            let result = {"Mon": [], "Tue": [], "Wed": [], "Thu": [], "Fri": []};
            const timeToColumn = [
                {"08:00:00": 1},
                {"09:00:00": 2},
                {"10:00:00": 3},
                {"11:00:00": 4},
                {"12:00:00": 5},
                {"13:00:00": 6},
                {"14:00:00": 7},
                {"15:00:00": 8},
                {"16:00:00": 9},
            ];

            for (const activity of this.activities) {

                const matchingObject = timeToColumn.find(obj => obj.hasOwnProperty(activity.time));
                const from = matchingObject[activity.time];
                const to = matchingObject[activity.time] + activity.duration;
                if (result[activity.day].length === 0) {
                    result[activity.day].push([{"activity": activity, "from": from, "to": to}]);
                }
                else {
                    let push = true;

                    for (const sub_mon of result[activity.day]) {
                        for (const element of sub_mon) {
                            push = true;
                            if ((from >= element.from && from < element.to) || (to > element.from && to <= element.to)){
                                push = false;
                                break;
                            }
                        }
                        if (push) {
                            sub_mon.push({"activity": activity, "from": from, "to": to});
                            sub_mon.sort((a, b) => a.from - b.from);
                            break;
                        }
                    }

                    if (!push) {
                        result[activity.day].push([{"activity": activity, "from": from, "to": to}]);
                    }
                }
            }
            // console.log(result);
            this.activitiesInCalendar = result;
        },
        handleRemoveScheduleCell(activity){
            this.$emit("remove-from-calendar", activity);
        },
    }
}

</script>

<style scoped>

.calendar{
    width: calc(100% - 40px);
    margin: 20px;
    background-color: white;
    border-radius: 20px;
}
.grid-10 {
    padding: 5px 10px;
    display: grid;
    grid-template-columns: 70px repeat(9, 1fr);
}

.grid-10 > div {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px 5px;
}

.grid-10 > div > p {
    margin: 0;
    font-size: 22px;
    font-weight: 550;
}

.day {
    min-height: 70px;
    padding: 0px 5px;
    display: grid;
    grid-template-columns: 70px repeat(1, 1fr);
}

.day > div:first-child {
    display: flex;
    justify-content: center;
    align-items: center;
}

.day > div:first-child > p {
    margin: 0;
    font-size: 24px;
    font-weight: 700;
}

.grid-9 {
    width: 100%;
    border-top: 1px solid rgb(0, 0, 0, 0.13);
    border-bottom: 1px solid rgb(0, 0, 0, 0.13);
}

.grid-9 > div {
    padding: 5px 0px;
    display: grid;
    gap: 5px;
    grid-template-columns: repeat(9, 1fr);
}

</style>