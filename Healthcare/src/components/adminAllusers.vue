<template>
    <div>
        <div class="navbar">
    <router-link to="/adminHomepage" >Home</router-link>
    <router-link to="/adminApproval" @click="Approve()">Pending Approvals</router-link>
    <router-link to="/adminAllusers" class="active">All Users</router-link>    
        </div>
  {{dummy()}}
        <!-- {{this.$store.getters.getUser}} -->
        <!-- {{a}} -->
    <ul style="list-style: none;" v-for="z in a" :key="z">
      <!-- loop 1 -->
   <div v-if="a.length === 0">NO pending approval</div>
    <li  style="list-style: none;" v-for="i,k in z" :key="i">
      <!-- loop 2 -->
        <ul style="list-style: none;">
          <!-- loop 3 -->
          {{k+1}}
            <!-- {{i[0].stakeHolder}} -->
            <!-- {{i}} -->
             <li style="list-style: none;" v-for=" (j,l) in i" :key="j">
              <div v-if="l !=='file_id' && l!=='hashedFile' && l!=='id' && l!=='type' && l!=='uploader' && l!=='wallet_address' && l!=='hashedFileName' && l!=='URL'">
                <div v-if="l==='originalFileName'">
           <div class="idk2"> {{l}}  :  </div>
        
              <a :href=i.URL target="_blank">{{j}}</a>    
              <!-- {{i.URL}}             -->
              </div>
              <div  v-else>
                 <div class="idk2">{{l}}  : </div>  {{j}}
              </div>
              </div>            
            </li>
            
    <button type="button" @click="deny(k,i.stakeholder)">Delete</button>
    
    
    </ul>
    </li>
  </ul>
    </div>
</template>
<script>
//import { json } from 'body-parser';
import UserDataService from "../service/backendDataService";
export default {
  name: "findingDoc",
 
  props: {},
  data: function () {
    return {
      a: this.$store.getters.getUser,
      
    isActive: false,
      
    };
  },
  methods: {
    Approve: async function () {
      var b = await UserDataService.retrieveUnverifiedUsers();
      this.a=b.data;
      this.$store.dispatch("updateUser", this.a);
    },
    dummy:function(){
      this.a=this.$store.getters.getUser;
    },
    deny(k, stake) {
      var user_email;
      var verifiedFile = this.check;
      var params;
      console.log("helloooo");
      if (stake == "doctor") {
        console.log("hello");
        user_email = this.a[0][k].email;
        params = {
          stakeholder: stake,
          email: user_email,
          verifiedFile: verifiedFile,
        };
        // params = JSON.stringify(params);
        UserDataService.denyUser(params);
      } else if (stake == "hospital") {
        user_email = this.a[1][k].email;
        params = {
          stakeholder: stake,
          email: user_email,
          verifiedFile: verifiedFile,
        };
        // params = JSON.stringify(params);
        UserDataService.denyUser(params);
      } else if (stake == "insurance") {
        user_email = this.a[2][k].email;
        params = {
          stakeholder: stake,
          email: user_email,
          verifiedFile: verifiedFile,
        };
        // params = JSON.stringify(params);
        UserDataService.denyUser(params);
      } else if (stake == "patient") {
        user_email = this.a[3][k].email;
        params = {
          stakeholder: stake,
          email: user_email,
          verifiedFile: verifiedFile,
        };
        // params = JSON.stringify(params);
        UserDataService.denyUser(params);
      } else if (stake == "pharmacy") {
        user_email = this.a[4][k].email;
        params = {
          stakeholder: stake,
          email: user_email,
          verifiedFile: verifiedFile,
        };
        // params = JSON.stringify(params);
        UserDataService.denyUser(params);
      }
    },
  }
 
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
.idk{
  font-weight:bolder;
   font-size: 3rem;
   color:  #82c8f7;
}
.idk2{
  font-weight:bolder;
}


</style>