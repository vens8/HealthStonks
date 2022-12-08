<template>
  <div>
    <div class="navbar">
      <!-- <a href="">Home</a> -->
      <!-- <router-link to="/Home" >Home</router-link>
      <a href="#Profile" class="active">Profile</a>
      <a href="#contact">Contact</a> -->
      <!-- <router-link to="/" >Register</router-link>
        <router-link to="/LoginPage" >Login</router-link> -->
        <router-link to="/Home" >Home</router-link>
        <router-link to="/about" >About</router-link> 
        <router-link to="/findingDoc" >Doctor</router-link>
        <router-link to="/findingHosp">Hospital</router-link>
        <router-link to="/findingPharmacy">Pharmacy</router-link>
        <router-link to="/findingInsurance">Insurance</router-link>
        <router-link to="/ProfilePatient" class="active">Profile</router-link>
        <router-link :to="{ name: 'shareFiles' }">Share Files</router-link>
   
    </div>
    <div class="start"><h1>PROFILE PAGE</h1></div>
    <div>
      <div class="prof1">
        <p>
          Name:{{ a.name }}
          <input
            type="text"
            v-model="name"
            placeholder="Edit your Name"
          />
        </p>
        <p>
          Email: {{ a.email }}
          <!-- FROM DB -->
          <!-- <input type=text v-model="fname" placeholder="Enter your Last Name" /> -->
        </p>
        <p>
          Licence Number:{{ a.licenceNo}}
          <!-- <input
            type="text"
            v-model="regnum"
            placeholder="Enter your Registartion Number"
          /> -->
        </p>
        <p>Contact Number:{{ a.phoneNo }}
         <input type=text id="contact" v-model="ohoneNo" placeholder="Edit Contact Number" />
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
        <p>
          Location:{{ a.location }}
          <input type="text" v-model="location" placeholder="Enter your location" />
        </p>
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
        <!-- <p>
          Contact Number:{{ contact }}
          <input
            type="text"
            v-model="contact"
            placeholder="Enter your Contact Number"
          />
        </p> -->
        <!-- TAKE IMAGE OF HOSPITAL FROM DB -->

        <!-- <p>Upload your documents: {{ doc }}</p>
        <upload-files></upload-files> -->
      </div>
    </div>
  </div>
</template>
   <script>
// import UploadFiles from "./UploadFiles.vue";
import UserDataService from "../service/backendDataService";

export default {
  name: "ProfilePharmacy",
  components: {
    //UploadFiles,
  },
  props: {
    msg: String,
  },
  data() {
    return {
      a: this.$store.getters.getUser[0],
      users: null,
    };
  },
  methods: {
    saveProfile: async function () {
      var stakeHolder = "pharmacy"; // Hardcoding for now, otherwise it must be taken from current login state (Vuex store)
      var name = document.getElementById("name").value;
      // var DOB = document.getElementById("DOB").value;
      // DOB = DOB.replaceAll("/", "-");
      // Add gender field here later
      var phoneNo = document.getElementById("phoneNo").value;
      var email = this.$store.getters.getUser[0].email; // Hardcoding for now, otherwise it must be taken from current login state (Vuex store)
      var currentPassword = document.getElementById("currentPassword").value;
      var newPassword = document.getElementById("newPassword").value;
      var newPasswordRepeat =
        document.getElementById("newPasswordRepeat").value;
      // console.log(stakeHolder);
      // console.log(uid);
      // console.log(passWord);
      //var specialty= document.getElementById("specialty").value;
      var licenceNo = document.getElementById("licenceNo").value;
      var location = document.getElementById("location").value;
      // var contact = document.getElementById("contact").value;
   
      var params = {
        stakeholder: stakeHolder,
        email: email,
        name: name,
        licenceNo: licenceNo,
        phoneNo: phoneNo,
        location: location,
        // specialty: specialty,
        currentPassword: currentPassword,
        newPassword: newPassword,
        newPasswordRepeat: newPasswordRepeat,
      };
      params = JSON.stringify(params);
      var b = await UserDataService.updateUser(params, {});
      console.log(b);
    },
    fetchFile: async function(){

      // var params = {
      //   stakeholder: "files",
      //   uploader: 'naman@gmail.com'
      // };
      // params = JSON.stringify(params);
      // var res = await UserDataService.retrieveUser(params);
      // console.log(res.data);

    
    },


    verify: async function(){
      // var params = {
      //   stakeholder: "verify",
      //   uploader: 'naman@gmail.com',
      //   originalFileName: 'sample.pdf'
      // };
      // params = JSON.stringify(params);
      // var res = await UserDataService.retrieveUser(params);
      // console.log(res.data);

    }


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