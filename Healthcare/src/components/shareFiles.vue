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
    <router-link to="/findingHosp" >Hospital</router-link>
    <router-link to="/findingPharmacy">Pharmacy</router-link>
    <router-link to="/findingInsurance">Insurance</router-link>
     <router-link :to="{ name: 'shareFiles' }" class="active">Share Files</router-link>
        <!-- <router-link :to="{ name: 'ProfilePatient' }">Profile</router-link> -->
        <router-link to="/ProfilePatient" v-if="a.stakeholder=='patient'">Profile</router-link>
        <router-link to="/ProfileDoctor" v-if="a.stakeholder=='doctor'">Profile</router-link>
        <router-link to="/ProfileHosp" v-if="a.stakeholder=='hospital'">Profile</router-link>
        <!-- <router-link to="/ProfilePatient">Profile</router-link> -->
        <router-link to="/ProfileInsurance" v-if="a.stakeholder=='insurance'">Profile</router-link>
        <router-link to="/ProfilePharmacy" v-if="a.stakeholder=='pharmacy'">Profile</router-link> 
  </div>
  <form>
    <input id="file" type="file" name="file" />
    <br />
    <select name="fileTypes" id="type">
      <option value="prescription">Prescription</option>
      <option value="bill">Bill</option>
      <option value="medicalRecord">Medical Record</option>
      <option value="refund">Refund</option>
    </select>
    <br />
    <label>Give acess to (enter email):</label>
    <input id="access" type="email" />

    <button type="reset" @click="uploadMyFile()">Upload</button>
  </form>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "testPage",
  components: {},
  data() {
    return {
      msg: "This is demo net work",
      a:this.$store.getters.getUser[0],
    };
  },

  methods: {
    uploadMyFile: async function () {
      var access = document.getElementById("access").value;
      console.log(access);
      var type = document.getElementById("type").value;
      console.log(type);

      if (!/^\w+([\\.-]?\w+)*@\w+([\\.-]?\w+)*(\.\w{2,3})+$/.test(access)) {
        alert("You have entered an invalid email address!");
        return;
      }

      access = access.concat(",admin");
      console.log("reached");
      var formData = new FormData();
      var imagefile = document.querySelector("#file");
      formData.append("stakeholder", this.a.stakeholder);
      formData.append("uploader", this.a.email);
      formData.append("type", type);
      formData.append("access", access);

      var uploadField = document.getElementById("file");

      if (uploadField.files.length < 1) {
        alert("File has not been uploaded");
        return;
      }

      if (uploadField.files[0].size > 5000000) {
        alert("File is too big!");
        this.value = "";
        return;
      }

      formData.append("image", imagefile.files[0]);
      formData.append("access", "admin");
      await axios.post(
        "https://192.168.2.251:5000/uploadFile",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      // var hashedCheckSum = response.data["hash"];
      // console.log(
      //   hashedCheckSum.concat(
      //     "These were random characters. You really think we will console log?"
      //   )
      // );
    },
  },
};
</script>

<style scoped>
#id01 {
  display: block;
}
* {
  margin: 0;
  padding: 0;
}

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

#name {
  float: left;
  color: #05c2f7;
}

body {
  font-family: Arial, Helvetica, sans-serif;
}

/* Full-width input fields */
input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
}
select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

/* Set a style for all buttons */
button {
  background-color: #0bece8;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
}

button:hover {
  opacity: 0.8;
}

/* Extra styles for the cancel button */
.cancelbtn {
  width: auto;
  padding: 10px 18px;
  background-color: #f44336;
}

/* Center the image and position the close button */
.imgcontainer {
  text-align: center;
  margin: 24px 0 12px 0;
  position: relative;
}

img.avatar {
  width: 40%;
  border-radius: 50%;
}

.container {
  padding: 16px;
}

span.psw {
  float: right;
  padding-top: 16px;
}

/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0, 0, 0); /* Fallback color */
  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
  padding-top: 60px;
}

/* Modal Content/Box */
.modal-content {
  background-color: #fefefe;
  margin: 5% auto 15% auto; /* 5% from the top, 15% from the bottom and centered */
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
}

/* The Close Button (x) */
.close {
  position: absolute;
  right: 25px;
  top: 0;
  color: #000;
  font-size: 35px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: red;
  cursor: pointer;
}

.animate {
  -webkit-animation: animatezoom 0.6s;
  animation: animatezoom 0.6s;
}

@-webkit-keyframes animatezoom {
  from {
    -webkit-transform: scale(0);
  }
  to {
    -webkit-transform: scale(1);
  }
}

@keyframes animatezoom {
  from {
    transform: scale(0);
  }
  to {
    transform: scale(1);
  }
}

@media screen and (max-width: 300px) {
  span.psw {
    display: block;
    float: none;
  }
  .cancelbtn {
    width: 100%;
  }
}

/* Tooltip container */
.tooltip {
  position: relative;
  display: inline-block;
  margin-left: 10px;
  border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
}

/* Tooltip text */
.tooltip .tooltiptext {
  visibility: hidden;
  width: 240px;
  background-color: black;
  color: #fff;
  text-align: center;
  padding: 5px 0;
  border-radius: 6px;

  /* Position the tooltip text - see examples below! */
  position: absolute;
  z-index: 1;
}

/* Show the tooltip text when you mouse over the tooltip container */
.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
