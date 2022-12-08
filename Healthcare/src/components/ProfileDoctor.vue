<template>
    <div class="navbar">
            <router-link to="/Home" class="active">Home</router-link>
        <!-- <router-link :to="{ name: 'RegisterPage' }">Register</router-link> -->
        <!-- <router-link :to="{ name: 'LoginPage' }">Login</router-link> -->
<!--         
        <router-link :to="{ name: 'about' }">About</router-link> 
        <router-link :to="{ name: 'findingDoc' }">Doctor</router-link>
        <router-link :to="{ name: 'findingHosp' }">Hospital</router-link>
        <router-link :to="{ name: 'findingPharmacy' }">Pharmacy</router-link> -->
        <!-- <router-link to="/Home" >Home</router-link> -->
        <router-link to="/about" >About</router-link> 
        <router-link to="/findingDoc" >Doctor</router-link>
        <router-link to="/findingHosp">Hospital</router-link>
        <router-link to="/findingPharmacy">Pharmacy</router-link>
        <router-link to="/findingInsurance">Insurance</router-link>
        <router-link :to="{ name: 'shareFiles' }">Share Files</router-link>
        <!-- <router-link to="/ProfilePatient" class="active">Profile</router-link> -->
    
         <router-link to="/ProfileDoctor" v-if="a.stakeholder=='doctor'">Profile</router-link>

   </div>
   <div class=start><h1>Your Profile</h1></div>
   <div>
      <div class="prof1">
         <p>Name:{{ a.name }}
         <input type=text id="name" v-model="name" placeholder="Edit your Full Name" />
         </p>
         <p>Email: {{ a.email }}
         <!-- FROM DB -->
         <!-- <input type=text v-model="fname" placeholder="Enter your Last Name" /> -->
         </p>
         <p>Contact Number:{{ a.contact }}
         <input type=text id="contact" v-model="contact" placeholder="Edit your contact number" />
         </p>
         <p>Licence Number:{{ a.licenceNo }}
         <input type=text id="licenceNo" v-model="licenceNo" placeholder="Edit your Licence Number" />
         </p>
         <p>DOB:{{ dob }}
         <input type=text id="DOB" v-model="dob" placeholder="Enter your DOB" />
         </p>
         <p>Area of Specialty:{{ a.specialty }}
         <input type=text id="specialty" v-model="specialty" placeholder="Enter your Area of Specialty" />
         </p>
         <p>Location:{{ a.location }}
         <input type=text id="location" v-model="location" placeholder="Enter your location" />
         </p>
         <p>Consultation Fee:{{ a.fee }}
         <input type=text id="fee" v-model="fee" placeholder="Enter your Consultation Fee" />
         </p>
         <p>Current Password:{{ currentPassword }}
         <input type=password id="currentPassword" v-model="currentPassword" placeholder="Enter current password" />
         </p>
         <p>New Password:{{ newPassword }}
         <input type=password id="newPassword" v-model="newPassword" placeholder="Enter new password" />
         </p>
         <p>Repeat New Password:{{ newPasswordRepeat }}
         <input type=password id="newPasswordRepeat" v-model="newPasswordRepeat" placeholder="Enter new password again" />
         </p>         
         <!-- <p>Upload your documents: {{ doc }}</p>
         <upload-files></upload-files>
         <button type="button" @click="saveProfile()">Save Profile</button> -->
         <!-- <p>Upload your documents: {{ doc }}</p>
         <div>
            <form  action = "http://localhost:5000/uploadFile" method=post enctype=multipart/form-data>
               <input id = "file" type=file name=file>
               <br>
               <p>Enter your type</p>
               <input id = 'stakeHolder' name = "stakeholder" type = "text">
               <br>
               <p>Enter your email</p>
               <input id = 'uploader' name = "uploader" type = "text">
               <p>Enter email id of accesors</p>
               <input id = 'accesors' name = "access" type = "text">
               <br>
               <input type=submit value=Upload>

            </form>
         </div> -->
         <button type="button" @click="saveProfile()">Save Profile</button>
         <button type="button" @click="this.$router.push({path:'/displayFiles'})">
      Retrieve
   </button>
      </div>
   </div>
</template>
<script>
       
// import UploadFiles from "./UploadFiles.vue";
import UserDataService from "../service/backendDataService";

   export default {
       name: "profileDoctor",
       components:{
         //   UploadFiles
       },
     props: {
       msg: String,
     },
     data(){
       return {
     a: this.$store.getters.getUser[0],
         users: null,
   };
},
methods: {
      saveProfile: async function () {
      var stakeHolder = "doctor"  // Hardcoding for now, otherwise it must be taken from current login state (Vuex store)
      var name = document.getElementById('name').value;
      var DOB = document.getElementById('DOB').value;
      DOB = DOB.replaceAll('/', '-')
      var licenceNo = document.getElementById('licenceNo').value;
      var fee = document.getElementById('fee').value;
      // Add gender field here later
      var contact = document.getElementById('contact').value;
      var email = this.$store.getters.getUser[0].email;  // Hardcoding for now, otherwise it must be taken from current login state (Vuex store)
      var specialty = document.getElementById('specialty').value;
      var location = document.getElementById('location').value;
      var currentPassword = document.getElementById("currentPassword").value;
      var newPassword = document.getElementById("newPassword").value;
      var newPasswordRepeat = document.getElementById("newPasswordRepeat").value;
      // console.log(stakeHolder);
      // console.log(uid);
      // console.log(passWord);
      var params = { stakeholder: stakeHolder,
                     email: email,
                     name: name,
                     DOB: DOB,
                     phone: contact,
                     specialty: specialty,
                     licenceNo: licenceNo,
                     fee: fee,
                     location: location,
                     currentPassword: currentPassword,
                     newPassword: newPassword,
                     newPasswordRepeat: newPasswordRepeat};
      params = JSON.stringify(params);
      var a = await UserDataService.updateUser(params, {});
      console.log(a);
      }
   },
   }
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
   font-weight:bold;
   border-style: solid;
   border-radius: 5px
}
.start{
   background-color: #82c8f7;
   font-weight:bolder;
   
   color: white;
}
input[type="text"]{
   width:50%;
   padding: 12px 20px;
    margin: 8px 0;
   box-sizing: border-box;
}

input[type=text]:focus {
 background-color: hsl(0, 0%, 95%);
}


</style>