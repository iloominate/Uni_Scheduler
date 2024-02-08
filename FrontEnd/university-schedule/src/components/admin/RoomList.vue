<template>
    <div class="search">
        <input v-model="searchQuery" placeholder="Search by number" />
        <button @click="searchRooms">
          <img src="../../assets/search.svg" alt="">
        </button>
      </div>
    <div class="list">
        <div v-for="(room, index) in paginatedRoomArray" :key="index" @click="EditRoom(room)">
            <p>Room №{{ room.number }}</p>
            <img src="../../assets/edit-item.svg" alt="">
        </div>
    </div>
    <div v-if="totalPages > 1" class="pagination">
        <button @click="prevPage">
            <img src="../../assets/prev-page.svg" alt="">
        </button>
        <span>Page {{ currentPage }}</span>
        <button @click="nextPage">
            <img src="../../assets/next-page.svg" alt="">
        </button>
    </div>
</template>


<script>
/**
 * @authors
 *   xmyron00, Yurii Myronov
 *
 * @file RoomList.vue
 * @brief Component for read rooms
 */

export default {
    data() {
        return {
            currentPage: 1,
            itemsPerPage: 5,
            searchQuery: "",
        };
    },
    props: {
        roomArray: {
            type: Array,
            default: [],
        },
    },
    computed: {
      totalPages() {
        return Math.ceil(this.filteredRoomArray.length / this.itemsPerPage);
      },
      paginatedRoomArray() {
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        return this.filteredRoomArray.slice(startIndex, endIndex);
      },
      filteredRoomArray() {
        return this.roomArray.filter(room =>
          room.number.toString().includes(this.searchQuery)
        );
      },
    },
    methods: {
        EditRoom(room){
            this.$emit("edit-room", room);
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage += 1;
            }
        },

        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage -= 1;
            }
        },
        searchRooms() {
        this.currentPage = 1;
      },
    }
}

</script>


<style scoped>

.list {
    display: flex;
    flex-direction: column;
    max-height: 470px;
    overflow: auto;
}

.list > div {
    border: 1px solid rgb(0, 0, 0, 0.5);
    border-radius: 10px;
    padding: 10px;
    margin: 5px 10px;
    display: flex;
    justify-content: space-between;
}

p {
    margin: 0;
}

.list > div:hover {
    cursor: pointer;
    background-color: rgb(0, 0, 0, 0.05);
}

img {
    width: 20px;
    height: 20px;
}

.pagination {
    border: 1px solid rgb(0, 0, 0, 0.2);
    border-radius: 20px;
    margin: 5px auto;
    width: fit-content;
    display: flex;
    gap: 15px;
    align-items: center;
    overflow: hidden;
}

.pagination > button {
    border: none;
    background-color: white;
    padding: 10px;
}

.pagination > button:hover{
    background-color: rgb(0,0,0, 0.05);
}

.pagination > button > img {
    width: 15px;
    height: 15px;
}

.search {
    margin: 5px 10px;
    display: flex;
}

.search > input {
  width: 100%;
  box-sizing: border-box;
  border-radius: 7px 0px 0px 7px;
  border-color: rgb(0, 0, 0, 0.2);
  border-style: solid none solid solid;
  border-width: 1px;
  padding: 7px;
}

.search > button {
  background-color: white;
  border-radius: 0px 7px 7px 0px;
  border-color: rgb(0, 0, 0, 0.2);
  border-width: 1px;
}

</style>