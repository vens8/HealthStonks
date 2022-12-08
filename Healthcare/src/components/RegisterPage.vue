<template>
  <div>
    <div class="navbar">     
      <router-link to="/" class="active">Register</router-link>
      <router-link to="/LoginPage">Login</router-link>  
    </div>
    <div>
      <form class="modal-content animate">
        <div class="imgcontainer">
          <img
            src=".././assets/pharm-difficult-logo.png"
            alt="logo"
            class="avatar"
          />
        </div>

        <label for="stakeHolder"><b>Register as</b></label>
        <select
          name="stakeHolder"
          id="stakeHolderReg"
          @change="show('stakeHolderReg')"
        >
          <option value="none">--Select--</option>
          <option value="pharmacy">Pharmacy</option>
          <option value="doctor">Doctor</option>
          <option value="patient">Patient</option>
          <option value="hospital">Hospital</option>
          <option value="insurance">Insurance Company</option>
        </select>

        <div class="pharmacy hospital insurance">
          <label for="licenceNo"><b>Enter your Licence Number</b></label>
          <input
            id="regNo"
            type="text"
            placeholder="Enter No"
            name="uname"
            required
          />
        </div>
        <div class="doctor patient pharmacy hospital insurance">
          <label for="emailID"><b>Enter associated Email ID</b></label>
          <input
            id="emailID"
            type="email"
            placeholder="Enter email"
            name="email"
            required
          />
        </div>

        <div class="pharmacy hospital doctor patient insurance">
          <button id="getOTP" type="button" @click="sendEmail()">
            Get OTP
          </button>
        </div>
        

        <div class="afterOTP">
          <label for="otp"><b>Enter OTP</b></label>
          <input
          v-on:keypress.prevent
            id="otp"
            maxlength="6"
            minLength="6"
            type="text"
            placeholder="Enter OTP"
            v-model="message" 
            name="otp"
            required
          />
          <!-- <div class="form-group">
    <input type="text" id="text" v-model="message" 
           placeholder="Words..." class="form-control">
  </div> -->
          <div class="keyboard" @click="typeLetter">
          <div class="row">
      <div class="key">1</div>
      <div class="key">2</div>
      <div class="key">3</div>
      
    </div>
    <div class="row">
      <div class="key">4</div>
      <div class="key">5</div>
      <div class="key">6</div>
    
    </div>
    <div class="row">
      <div class="key">7</div>
      <div class="key">8</div>
      <div class="key">9</div>
      
    </div>
        <div class="row">
      <div class="key">0</div>
      <div class="key">Del</div>
     
      
    </div>
    <div>
      <!-- <div class="key" id="space"> </div> -->
    </div>
          </div>
          <label for="psw">Set a Password</label>
          <input
            id="psw"
            type="password"
            maxlength="20"
            placeholder="Enter Password"
            name="psw"
            required
          />
          <label for="psw"><b>Repeat Password</b></label>
          <input
            id="psw-repeat"
            type="password"
            maxlength="20"
            placeholder="Re-enter Password"
            name="psw"
            required
          />
        </div>
        <button type="button" @click="registerStakeHolder()">Register</button>
      </form>
    </div>
  </div>
</template>

<script>
import UserDataService from "../service/backendDataService";
// import emailjs from "emailjs-com";
// import backendDataService from '../service/backendDataService';
export default {
  name: "RegisterPage",
  props: {},
  data: function () {
    return {
      message:"",
      rules: [
        { message: "One lowercase letter required.", regex: /[a-z]+/ },
        { message: "One uppercase letter required.", regex: /[A-Z]+/ },
        { message: "8 characters minimum.", regex: /.{8,}/ },
        { message: "One number required.", regex: /[0-9]+/ },
      ],
      password: "",
      checkPassword: "",
      passwordVisible: false,
      submitted: false,
      currOtp: null,
    };
  },
  methods: {
      typeLetter: function(){
      if (event.target.className !== "keyboard") {
        var key = event.target.innerHTML || event.target.id;
        if (key === 'Del') {
          this.message = this.message.substr(0,this.message.length - 1) 
        }
        else if (key === 'space') {
          this.message += " ";
        }
        else {
         this.message += key;
        }
      }
    },
    // Working function to get info from database
    // findData: async function(){
    //     // var name =
    //     // var location =
    //     // var speciality =

    //     var params = {"stakeholder":"pharmacy", "name": "none", "location": "Rohini", "speciality":"none"};
    //     params = JSON.stringify(params)
    //     var a = await backendDataService.retrieveUser(params);
    //     console.log(a.data);
    // },

    sendEmail: async function () {
      var email = document.getElementById("emailID").value;
      if (!(email.length > 0)) {
        alert("Please enter email ID");
        return;
      }

      if (!(/^\w+([\\.-]?\w+)*@\w+([\\.-]?\w+)*(\.\w{2,3})+$/.test(email))) {
        alert("You have entered an invalid email address!");
        return;
        
      } 

      if(email.length>150){
        alert("Invalid email")
        return;
      }
      

      if (email.length > 0) {
        var emailDict = { email: email };
        var response = await UserDataService.sendOTP(emailDict);
        console.log(response);
      }
      var a = document.getElementsByClassName("afterOTP");
      console.log(a);
      for (var i = 0; i < a.length; i++) {
        a[i].style.display = "block";
      }
      var x = document.getElementById("getOTP");
      x.disabled = true;
      x.innerHTML = "OTP Sent";
      setTimeout(function () {
        x.disabled = false;
        x.innerHTML = "Get OTP";
      }, 50000);
    },
    show: function (id) {
      var x = document.getElementById(id).value;
      if (x == "doctor" || x == "patient") {
        var toHide = document.getElementsByClassName(
          "pharmacy hospital insurance"
        );
        for (var i = 0; i < toHide.length; i++) {
          toHide[i].style.display = "none";
        }
        var toShow = document.getElementsByClassName("doctor patient");
        for (i = 0; i < toShow.length; i++) {
          toShow[i].style.display = "block";
        }
      } else if (x == "pharmacy" || x == "hospital" || x == "insurance") {
        toHide = document.getElementsByClassName("doctor patient");
        for (i = 0; i < toHide.length; i++) {
          toHide[i].style.display = "none";
        }
        toShow = document.getElementsByClassName("pharmacy hospital insurance");
        for (i = 0; i < toShow.length; i++) {
          toShow[i].style.display = "block";
        }
      }
      //   return "Welcome to this tutorial on " + this.name + " - " + this.topic;
    },
    registerStakeHolder: async function () {
      // console.log(this.$data.currOtp); // IMP: Remove this at the end - only for testing
      var stakeHolder = document.getElementById("stakeHolderReg").value;
      var password = document.getElementById("psw").value;
      var passwordRepeat = document.getElementById("psw-repeat").value;
      var enteredOTP = document.getElementById("otp").value;
      var email = document.getElementById("emailID").value;

      if (stakeHolder == "patient") {
        console.log("patient");
        this.$store.dispatch("updateUser", [
          {
            stakeHolder: stakeHolder,
            email: email,
          },
        ]);
      } else {
        this.$store.dispatch("updateUser", [
          {
            stakeHolder: stakeHolder,
            email: email,
            licenceNo: document.getElementById("regNo").value,
          },
        ]);
      }
      var curr = this.$store.getters.getUser;
      console.log(curr);

      if (password != passwordRepeat) {
        alert("Passwords do not match");
        return;
      }

      var regexForPassword = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$/;
      if(!(password.match(regexForPassword))){
        alert("Password should be between between 8 to 15 characters which contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character");
        return;
      }
      var emailDict = { email: email, otp: enteredOTP };
      var response = await UserDataService.verify(emailDict);
      var verified = response["data"]["verified"];

      if (verified == 1) {
        console.log("Correct OTP");
      } else {
        alert("OTP is incorrect");
        return;
      }

      if (stakeHolder == "none") {
        alert("Please select a stakeholder");
        return;
      } else if (stakeHolder == "patient") {
        // PATIENT
        // var email = document.getElementById("emailID").value;
        if (email.length == 0) {
          // Add later: regex to validate email format
          alert("Please enter a valid Email Address");
          return;
        }
        //added here
        //var user1={"stakeholder":stakeHolder, "email":email};
        //this.$store.dispatch('updateUser', user1);
        //console.log(this.$store.getters.getUser[0]);

        var addedToDB = await UserDataService.createUser({
          stakeholder: "patient",
          registrationNum: "",
          name: "",
          DOB: "",
          gender: "",
          email: email,
          password: password,
          phone: "",
          joiningDate: "",
          pcpID: "",
          insuranceID: "",
          wallet_address: ""
        });
        if (addedToDB["data"]["status"] != 0) {
          this.$router.push("/RegProfile");
        } else {
          alert("Email already exists");
        }
      } else if (stakeHolder == "doctor") {
        // DOCTOR
        // email = document.getElementById("emailID").value;
        if (email.length == 0) {
          // Add later: regex to validate email format
          alert("Please enter a valid Email Address");
          return;
        }

        addedToDB = await UserDataService.createUser({
          stakeholder: "doctor",
          licenceNo: "",
          name: "",
          DOB: "",
          gender: "",
          email: email,
          password: password,
          phone: "",
          specialty: "",
          location: "",
          joiningDate: "",
          consultationFee: "",
          wallet_address: ""
        });

        if (addedToDB["data"]["status"] != 0) {
          this.$router.push("/RegProfile");
        } else {
          alert("Email already exists");
        }
      } else if (stakeHolder == "pharmacy") {
        // PHARMACY
        // email = document.getElementById("emailID").value;
        var regNo = document.getElementById("regNo").value;
        console.log(email);
        console.log(regNo);
        if (email.length == 0 || regNo.length == 0) {
          alert("Please enter email ID and Registration number");
          return;
        }

        // TODO: Check if already exist
        addedToDB = await UserDataService.createUser({
          stakeholder: "pharmacy",
          licenceNo: regNo,
          name: "",
          email: email,
          password: password,
          phone: "",
          location: "",
          image1: "",
          image2: "",
          joiningDate: "",
          wallet_address: ""
        });
        if (addedToDB["data"]["status"] != 0) {
          this.$router.push("/RegProfile");
        } else {
          alert("Email already exists");
        }
      } else if (stakeHolder == "hospital") {
        // HOSPITAL
        // email = document.getElementById("emailID").value;
        regNo = document.getElementById("regNo").value;
        if (email.length == 0 || regNo.length == 0) {
          alert("Please enter email ID and Registration number");
          return;
        }

        addedToDB = await UserDataService.createUser({
          stakeholder: "hospital",
          licenceNo: regNo,
          name: "",
          email: email,
          password: password,
          phone: "",
          location: "",
          specialty: "",
          image1: "",
          image2: "",
          wallet_address: ""
        });

        if (addedToDB["data"]["status"] != 0) {
          this.$router.push("/RegProfile");
        } else {
          alert("Email already exists");
        }
      } else if (stakeHolder == "insurance") {
        // INSURANCE
        // email = document.getElementById("emailID").value;
        regNo = document.getElementById("regNo").value;
        if (email.length == 0 || regNo.length == 0) {
          alert("Please enter email ID and Registration number");
          return;
        }

        addedToDB = await UserDataService.createUser({
          stakeholder: "insurance",
          licenceNo: regNo,
          name: "",
          email: email,
          password: password,
          phone: "",
          location: "",
          image1: "",
          image2: "",
          wallet_address: ""
        });

        if (addedToDB["data"]["status"] != 0) {
          this.$router.push("/RegProfile");
        } else {
          alert("Email already exists");
        }
      }
    },
  },
};
</script>

<style scoped>
body {
  font-family: Arial, Helvetica, sans-serif;
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

input[type="text"],
input[type="email"],
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
.afterOTP {
  display: none;
}
.doctor {
  display: none;
}
.hospital {
  display: none;
}
.pharmacy {
  display: none;
}
.insurance {
  display: none;
}
.doctor {
  display: none;
}


.keyboard {
  display:flex;
  flex-direction:column;
  align-items:center; /* Y-axes in this case */
}

.row {
  display:flex;
  align-content:space-around;
}

.key {
  padding:10px;
  height:60px;
  width:60px;
  border-bottom: 1px solid black;
  border-right: 1px solid black;
  cursor: pointer;
}

#space {
  width:400px;
}

.key:first-child {
  border-left: 1px solid black; 
}

.row:first-child {
  border-top: 1px solid black;
}

input {
  margin-top:50px;
}




</style>
