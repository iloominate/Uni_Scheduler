<!--@authors-->
<!--xklima34, Aliaksei Klimau-->
<!--@file Navigation.vue-->
<!--@brief Navigation bar-->

<template>

  <div v-if="showProfile">
    <UserProfileCard
        :user = "user"
        @close-user-profile="closeUserProfile"
    ></UserProfileCard>
  </div>

    <div class="header">
        <div class="user" @click="showUserProfile">
            <img src="../assets/avatar.svg" alt="">
            <div>
                <p class="username">{{ username }}</p>
                <p class="status">{{ status }}</p>
            </div>
        </div>
        <div class="menu">
            <div v-for="button in buttons" :key="button.text" class="menu-item" @click="handleButtonClick(button)">
                <p class="btn-route">{{ button.text }}</p>
                <div v-if="button.dropdown && button.isShow" class="dropdown">
                    <div v-for="item in button.dropdown" :key="item.text" @click="handleButtonClick(item)">
                        <p class="btn-route">{{ item.text }}</p>
                    </div>
                </div>
            </div>
            <div class="btn-login" @click="Auth">
                {{ authButton }}
            </div>
        </div>
    </div>
</template>

<script>
import UserProfileCard from "@/components/UserProfileCard.vue";

export default {
  components: {UserProfileCard},
    data() {
        return {
            showProfile: false,
            username: 'Anonymous',
            status: '',
            buttons: [
                { text: 'Home', route: '/' },
            ],
            authButton: 'login',
            user: {},
            currentPage: '',
        }
    },
    mounted() {
        // Initialize user data and set current page based on the route
        this.UpdateUserData();
        switch(this.$route.path){
            case "/admin":
                this.currentPage = "Administration";
                break;
            case "/scheduler":
                this.currentPage = "Schedule";
                break;
            case "/":
                this.currentPage = "Home";
                break;
            case "/student/subjects":
            case "/student/activities":
            case "/student":
              this.currentPage = "Student";
              break;
            case "/guarantor":
            case "/guarantor/instructors":
            case "/guarantor/activities":
              this.currentPage = "Guarantor";
              break;
            case "/instructor":
            case "/instructor/activities":
              this.currentPage = "Instructor";
              break;
        }
        if(this.status === 'Guarantor'){
          if(this.currentPage === 'Guarantor'){
            this.buttons.push({ text: 'InstructorMode', route: '/instructor' })
          }
          else if(this.currentPage === 'Instructor'){
            this.buttons = [
              {text:'Home', route: '/'},
              {text:'Schedule',  route:'/instructor'},
              {text:'Activities', route:'/instructor/activities'},
              {text: 'GuarantorMode', route: '/guarantor' },
            ]
          }
        }


    },
    methods: {
        // Update user data from localStorage and change navigation buttons accordingly
        UpdateUserData() {
            if (localStorage.getItem("token")){
                this.user = JSON.parse(localStorage.getItem('user'));
                if (this.user){
                    this.username = this.user.username;
                    this.status = this.user.permission.description
                }
                // Set authentication button based on token presence
                this.authButton = localStorage.getItem("token") ? "logout" : "login";
            }

            switch(this.status){
                case "Admin":
                    this.buttons = [
                        { text: 'Subjects', route: '/' },
                        { text: 'Scheduler',route: '/scheduler' },
                        {
                            text: 'Instructor',
                            dropdown: [
                                {
                                    text: 'Schedule',
                                    route: '/instructor',
                                    isShow: false,
                                },
                                {
                                    text: 'Activities',
                                    route: '/instructor/activities',
                                    isShow: false,
                                },
                            ],
                        },
                        {
                            text: 'Guarantor',
                            dropdown: [
                                {
                                    text: 'Schedule',
                                    route: '/guarantor',
                                    isShow: false,
                                },
                                {
                                    text: 'Instructors',
                                    route: '/guarantor/instructors',
                                    isShow: false,
                                },
                                {
                                    text: 'Activities',
                                    route: '/guarantor/activities',
                                    isShow: false,
                                },
                            ],
                        },
                        { text: 'Admin', route: '/admin' },
                    ];
                    break;
                case "Scheduler":
                    this.buttons = [
                        { text: 'Subjects', route: '/' },
                        { text: 'Schedule', route: '/scheduler' }
                    ];
                    break;
                case "Student":
                  this.buttons = [
                    {text:'Home', route: '/'},
                    {text:'Schedule',  route:'/student'},
                    {text:'Subjects',  route:'/student/subjects'},
                    {text:'Activities', route:'/student/activities'},
                  ]
                  break;

                case "Guarantor":
                  this.buttons = [
                    {text:'Home', route: '/'},
                    {text:'Schedule',  route:'/guarantor'},
                    {text:'Instructors',  route:'/guarantor/instructors'},
                    {text:'Activities', route:'/guarantor/activities'},
                  ]
                  break;

                case "Instructor":
                  this.buttons = [
                    {text:'Home', route: '/'},
                    {text:'Schedule',  route:'/instructor'},
                    {text:'Activities', route:'/instructor/activities'},
                  ]
                  break;

                default:
                    break;
            }

        },
        // Authentication action (Login or Logout)
        Auth() {
            if (localStorage.getItem("token")){
                 localStorage.clear();
                this.$router.push('/');
            }
            else{
                this.$router.push('/authorization');
            }
            
        },

        // Navigate to the home page
        ToHome() {
            this.$router.push('/');
        },

        // Handle button clicks
        handleButtonClick(button) {
            if (button.route) {
                this.$router.push(button.route);
            } else if (button.dropdown) {
                button.isShow = !button.isShow;
            }
        },
        // Show user profile card if user is registered
        showUserProfile() {
          if (this.user !== null)
            this.showProfile = true;
        },
        // Close user profile card
        closeUserProfile() {
          this.showProfile = false;
        }
    }

};
</script>

<style scoped>

.header {
    margin: 20px;
    background-color: white;
    border-radius: 15px;
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
}

.btn-login {
    background: rgba(0, 0, 0, 0.7);
    padding: 10px 20px;
    border-radius: 20px;
    color: rgba(255,255,255,1);
    font-size: 16px;
    text-transform: uppercase;
}

.btn-login:hover {
    background: rgba(0, 0, 0, 0.6);
    cursor: pointer;
}

.menu {
    display: flex;
    align-items: center;
    gap: 30px;
}

.menu-item{
    color: rgba(0, 0, 0, 0.6);
    margin: 5px;
    border: none;
    background: none;
    font-size: 16px;
    font-weight: bold;
}

/* .menu-item:hover {
    text-decoration: underline;
    cursor: pointer;
    color: black;
} */


.user {
    display: flex;
    gap: 20px;
    flex-wrap: nowrap;
    align-items: center;
}

.user img {
    color: rgba(0, 0, 0, 0.6);
    height: 50px;
    width: 50px;
}

.username {
    margin: 0px;
    font-size: 20px;
    font-weight: bold;
    color: rgba(0, 0, 0, 0.7);
}

.status {
    margin: 0px;
    font-size: 14px;
    font-weight: bold;
    color: rgba(0, 0, 0, 0.4);
}

.dropdown {
    display: flex;
    flex-direction: column;
    position: absolute;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
    white-space: nowrap;
    z-index: 1;
}

.btn-route {
    background: none;
    margin: 0;
}

.btn-route:hover {
    text-decoration: underline;
    cursor: pointer;
    color: black;
}

.dropdown div {
    padding: 10px;
    cursor: pointer;
}

.menu-item {
    cursor: pointer;
    position: relative;
}

</style>