<template>
<div>
  <div class="navbar">
    <!-- <a href="/" >Home</a>
        <a href="/RegisterPage">Register</a>
        <a href="/LoginPage">Login</a>
        <a href="/about">About Us</a>
        <a href="/findingDoc">Doctor</a>
        <a href="/findingHosp" class="active">Hospital</a>
        <a href="/findingPharmacy">Pharmacy</a>
        <a href="/findingInsurance">Insurance</a>
        <a href="/ProfilePatient">Profile</a> -->
    <router-link to="/Home">Home</router-link>
       
    <!-- <router-link to="/RegisterPage">Register</router-link>
    <router-link to="/LoginPage">Login</router-link> -->
    <router-link to="/about">About</router-link>
    <router-link to="/findingDoc">Doctor</router-link>
    <router-link to="/findingHosp" class="active">Hospital</router-link>
    <router-link to="/findingPharmacy">Pharmacy</router-link>
    <router-link to="/findingInsurance">Insurance</router-link>
     <router-link :to="{ name: 'shareFiles' }">Share Files</router-link>
        <!-- <router-link :to="{ name: 'ProfilePatient' }">Profile</router-link> -->
        <router-link to="/ProfilePatient" v-if="a.stakeholder=='patient'">Profile</router-link>
        <router-link to="/ProfileDoctor" v-if="a.stakeholder=='doctor'">Profile</router-link>
        <router-link to="/ProfileHosp" v-if="a.stakeholder=='hospital'">Profile</router-link>
        <!-- <router-link to="/ProfilePatient">Profile</router-link> -->
        <router-link to="/ProfileInsurance" v-if="a.stakeholder=='insurance'">Profile</router-link>
        <router-link to="/ProfilePharmacy" v-if="a.stakeholder=='pharmacy'">Profile</router-link> 
  </div>
  <div class="hospital">
    <div class="location">
      <label for="hospital"><b>Search Location </b></label>
      <select name="location" id="location" @change="show('location')">
        <option v-for="i in a" :key="i.location">{{ i.location }}</option>
      </select>
    </div>
    <div class="name">
      <label for="hospital"><b>Search Name </b></label>
      <select name="name" id="name" @change="show('name')">
        <option v-for="i in a" :key="i.name">{{ i.name }}</option>
      </select>
    </div>
    <div class="speciality">
      <label for="hospital"><b>Search Type </b></label>
      <select name="speciality" id="speciality" @change="show('type')">
        <option v-for="i in a" :key="i.speciality">{{ i.speciality }}</option>
      </select>
    </div>
    <!-- <button type="button" @click="search()">
        Search
     </button> -->
    <br />
    <button type="button" @click="findData()">Search</button>
    <br />
    <br />
    <button type="button" @click="getAllData()">Fetch</button>
  </div>
</div>
</template>
  <script>
import UserDataService from "../service/backendDataService";
export default {
  name: "findingHosp",
  props: {},
  data: function () {
    return {
      a: [
        {
          name: "Please click Fetch",
          location: "Please click Fetch",
          specialty: "Please click Fetch",
        },
        {
          name: "Please click Fetch",
          location: "Please click Fetch",
          specialty: "Please click Fetch",
        },
        {
          name: "Please click Fetch",
          location: "Please click Fetch",
          specialty: "Please click Fetch",
        },
      ],
      isActive: false,
    };
  },
  methods: {
    getAllData: async function () {
      var params = {
        stakeholder: "hospital",
        name: "none",
        location: "none",
        speciality: "none",
      };
      // params = JSON.stringify(params);
      var res = await UserDataService.fetchUser(params);
      var toShow = res.data;
      console.log(res)
      // toShow = {};
      // console.log('toShow', toShow);
     
      this.a = toShow;
    },
    //Working function to get info from database
    findData: async function () {
      // var name =
      // var location =
      // var speciality =

      // var params = {"stakeholder":"hospital", "name": "none", "none": "Rohini", "speciality":"none"};
      // params = JSON.stringify(params)
      await UserDataService.fetchUser(params);
      this.data.a = [{name:'Naman', location:"Delhi"}, {name:'Sejal', location:"Nigeria"}];
      var locationToFind =
        document.getElementById("location").options[
          document.getElementById("location").selectedIndex
        ].innerHTML;
      var nameToFind =
        document.getElementById("name").options[
          document.getElementById("name").selectedIndex
        ].innerHTML;
      var specialityToFind =
        document.getElementById("speciality").options[
          document.getElementById("speciality").selectedIndex
        ].innerHTML;

      if (locationToFind == "" || locationToFind == null) {
        locationToFind = "none";
      }

      if (nameToFind == "" || nameToFind == null) {
        nameToFind = "none";
      }

      if (specialityToFind == "" || specialityToFind == null) {
        specialityToFind = "none";
      }
      var params = {
        stakeholder: "hospital",
        name: nameToFind,
        location: locationToFind,
        speciality: specialityToFind,
      };
      // params = JSON.stringify(params);
      var res = await UserDataService.fetchUser(params);
      localStorage.setItem("dict", JSON.stringify(res.data));
      // const arr = JSON.parse(localStorage.getItem("dict"));
      this.$router.push({ path: "/displayCatalog" });
    },

    // show: function (id) {
    //   var x = document.getElementById(id).value;
    // },
    //   search: function(){
    //   var locationToFind=document.getElementById("location").options[document.getElementById("location").selectedIndex].innerHTML;
    //   var nameToFind=document.getElementById("name").options[document.getElementById("name").selectedIndex].innerHTML;
    //   var specialityToFind=document.getElementById("speciality").options[document.getElementById("speciality").selectedIndex].innerHTML;
    //   localStorage.setItem('dict',JSON.stringify(this.a));
    //   const arr=JSON.parse(localStorage.getItem('dict'))
    //   //router.push("/displayCatalog");
    //   this.$router.push({path: '/displayCatalog'})
    // },
  },
};
</script>

  <style scoped>
.navbar {
  background-color: #333;
  overflow: hidden;
  top: 0;
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
button {
  background-color: #494949;
  border: thick;
  color: white;
  padding: 15px 32px;
  text-align: center;
  border-radius: 8px;
  text-decoration: none;
  font-size: 26px;
}

input[type="text"]:focus {
  background-color: hsl(0, 0%, 95%);
}
button:hover {
  background-color: #05c2f7;
  transition: 0.7s;
}
</style>