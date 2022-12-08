<template>
  <div>
    <div class="navbar">
      <router-link to="/" class="active">Home</router-link>
      <router-link to="/adminApproval" @click="Approve()"
        >Pending Approvals</router-link
      >
      <router-link to="/adminAllusers" @click="AllUsers()"
        >All Users</router-link
      >
    </div>
    <div>
      <h1>Welcome to ADMIN HomePage</h1>
    </div>
  </div>
</template>

<script>
import UserDataService from "../service/backendDataService";
export default {
  name: "adminHomePage",

  props: {},
  data: function () {
    return {
      a: [[{}]],
      isActive: false,
    };
  },
  methods: {
    AllUsers: async function () {
      var b = await UserDataService.retrieveVerifiedUsers();
      this.a = b.data;
      this.$store.dispatch("updateUser", this.a);
    },
    Approve: async function () {
      var b = await UserDataService.retrieveUnverifiedUsers();
      // b = JSON.stringify(b);
      this.a = b.data;

      this.$store.dispatch("updateUser", this.a);
    },
  },
};
</script>

<style scoped>
.navbar {
  background-color: #333;
  overflow: hidden;
  text-align: center;
  top: 0;
  font-size: 17px;
  width: 100%;
}

/* Style the links inside the navigation bar */
.navbar a {
  float: left;
  display: block;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
}

/* Change the color of links on hover */
.navbar a:hover {
  background-color: #ddd;
  color: black;
}

/* Add a color to the active/current link */
.navbar a.active {
  background-color: #05c2f7;
  color: white;
}

body {
  font-family: Arial, Helvetica, sans-serif;
}
.prof1 {
  text-align: left;
  padding: 5rem;
  font-size: 1.5rem;
  font-weight: bold;
  border-style: solid;
  border-radius: 5px;
}
.start {
  background-color: #82c8f7;
  font-weight: bolder;

  color: white;
}
input[type="text"] {
  width: 50%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
}

input[type="text"]:focus {
  background-color: hsl(0, 0%, 95%);
}
</style>
