<template>
  <div class="login">
    <div class="navbar">
      <router-link to="/">Register</router-link>
      <router-link to="/LoginPage" class="active">Login</router-link>
    </div>
    <h2 id="name">Pharm Difficult</h2>

    <div id="id01" class="modal">
      <form
        class="modal-content animate"
        action="/action_page.php"
        method="post"
      >
        <div class="imgcontainer">
          <span
            onclick="document.getElementById('id01').style.display='none'"
            class="close"
            title="Close Modal"
            >&times;
          </span>
          <img
            src=".././assets/pharm-difficult-logo.png"
            alt="Avatar"
            class="avatar"
          />
        </div>

        <div class="container">
          <label for="uname"><b>Unique Identification Number</b></label>
          <div class="tooltip">
            What is this?
            <span class="tooltiptext"
              >Patients/Doctors - Email Address<br />Pharmacies - Licence No<br />Hospitals
              - Reg. no.</span
            >
          </div>
          <input
            id="uid"
            type="text"
            placeholder="Enter UID"
            name="uname"
            required
          />

          <label for="psw"><b>Password</b></label>
          <input
            type="password"
            id="passw"
            placeholder="Enter Password"
            name="psw"
            required
          />

          <label for="stakeHolder"><b>Log in as</b></label>
          <select name="stakeHolder" id="stakeHolder">
            <option value="pharmacy">Pharmacy</option>
            <option value="doctor">Doctor</option>
            <option value="patient">Patient</option>
            <option value="hospital">Hospital</option>
            <option value="insurance">Insurance</option>
            <option value="admin">Admin</option>
          </select>

          <button type="button" @click="login()">Login</button>
        </div>

        <div class="container" style="background-color: #f1f1f1">
          <!-- onclick="document.getElementById('id01').style.display='none'" -->
          <button type="button" class="cancelbtn" @click="test()">
            Cancel
          </button>
          <span class="psw">Forgot <a href="#">password?</a></span>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import UserDataService from "../service/backendDataService";

export default {
  name: "LoginPage",
  data: function () {
    return {
      currentUser: null,
    };
  },
  props: {
    msg: String,
  },
  methods: {
    findData: async function () {
      // var name =
      // var location =
      // var speciality =

      var params = {
        stakeholder: "insurance",
        name: "none",
        location: "none",
        speciality: "none",
      };
      // params = JSON.stringify(params);
      var a = await UserDataService.retrieveUser(params);
      return a;
    },

    login: async function () {
      var stakeHolder = document.getElementById("stakeHolder").value;
      var uid = document.getElementById("uid").value;
      var passWord = document.getElementById("passw").value;
      var params = { stakeholder: stakeHolder, email: uid, password: passWord };
      // params = JSON.stringify(params);
      var a = await UserDataService.retrieveUser(params);
      var x = a.data.length;
      //console.log(a.data);

      if (x == 1) {
        console.log("here");
        var user = a.data;
        user[0]["stakeholder"] = stakeHolder;
        this.$store.dispatch("updateUser", user);
        if (user[0]["stakeholder"] == "admin") {
          this.$store.dispatch('updateAdmin', "true");
          this.$router.push({ path: "/adminHomepage" });
        } else {
          this.$router.push({ path: "/Home" });
        }
      } else {
        if("verifiedUser" in a.data){
          if(a.data.verifiedUser==0){
          alert("Wait for ADMIN approval")}
        }
        else{
        alert("Invalid Credentials");
        }
      }
    },
   
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
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
