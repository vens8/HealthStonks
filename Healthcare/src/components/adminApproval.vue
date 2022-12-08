<template>
  <div>
    <div class="navbar">
      <router-link to="/adminHomepage">Home</router-link>
      <router-link to="/adminApproval" class="active"
        >Pending Approval</router-link
      >
      <router-link to="/adminAllusers" @click="AllUsers()"
        >All Users</router-link
      >
    </div>
    <!-- {{fetchApprove()}} -->
    {{ dummy() }}

    <div v-if="a.length === 0">NO pending approval</div>
    <!-- {{this.$store.getters.getUser}} -->
    <!-- {{a}} -->
    <ul style="list-style: none" v-for="z in a" :key="z">
      <!-- loop 1 -->
      <div class="idk" v-if="z.length !== 0">{{ z[0].stakeholder }}</div>
      <li style="list-style: none" v-for="(i, k) in z" :key="i">
        <!-- loop 2 -->
        <ul style="list-style: none">
          <!-- loop 3 -->
          {{
            k + 1
          }}
          <!-- {{i[0].stakeHolder}} -->
          <!-- {{i}} -->
          <li style="list-style: none" v-for="(j, l) in i" :key="j">
            <div
              v-if="
                l !== 'file_id' &&
                l !== 'hashedFile' &&
                l !== 'id' &&
                l !== 'type' &&
                l !== 'uploader' &&
                l !== 'wallet_address' &&
                l !== 'hashedFileName' &&
                l !== 'URL'
              "
            >
              <div v-if="l === 'originalFileName'">
                <div class="idk2">{{ l }} :</div>

                <a :href="i.URL" target="_blank">{{ j }}</a>
                <!-- {{i.URL}}             -->
              </div>
              <div v-else>
                <div class="idk2">{{ l }} :</div>
                {{ j }}
              </div>
            </div>
          </li>

          <button type="button" @click="verify(i.wallet_address, i.hashedFile, i.email, i.originalFileName)">
            verify
          </button>
          <button type="button" @click="approve(k, i.stakeholder)">
            approve
          </button>
          <button type="button" @click="deny(k, i.stakeholder)">deny</button
          ><br />
        </ul>
      </li>
    </ul>
  </div>
</template>
<script>
//import { json } from 'body-parser';
import Web3 from "web3";
import { ethers } from "ethers";
import UserDataService from "../service/backendDataService";
export default {
  name: "adminApproval",
  props: {},
  data: function () {
    return {
      check:0,
      a: this.$store.getters.getUser,
      // a: [
      //   [{
      //     name: "Hungry ",
      //     location: "Lost",
      //     stakeHolder: "pharmacy",
      //   },
      //   {
      //     name: "Hungry ",
      //     location: "Lost",
      //     stakeHolder: "pharmacy",
      //   }
      // ],[
      //   {
      //     name: "Please click Fetch",
      //     location: "Please click Fetch",
      //     stakeHolder: "patient",
      //   },
      //   {
      //     name: "Please click Fetch",
      //     location: "Please click Fetch",
      //     stakeHolder: "patient",
      //   },]
      // ],

      //dic:[],
      isActive: false,
    };
  },
  methods: {
    AllUsers: async function () {
      var b = await UserDataService.retrieveVerifiedUsers();
      this.a = b.data;
      this.$store.dispatch("updateUser", this.a);
    },

    dummy: function () {
      this.a = this.$store.getters.getUser;
    },
    //0:doc
    //1:hosp
    //2:insu
    //3:pat
    //4:pharm
    approve(k, stake) {

      var user_email;
      var verifiedFile = this.check;
      var params;
      if (stake == "doctor") {
        user_email = this.a[0][k].email;

        params = {
          stakeholder: stake,
          email: user_email,
          verifiedFile: verifiedFile,
        };
        // params = JSON.stringify(params);
        UserDataService.approveUser(params);
      } else if (stake == "hospital") {
        user_email = this.a[1][k].email;
        params = {
          stakeholder: stake,
          email: user_email,
          verifiedFile: verifiedFile,
        };
        // params = JSON.stringify(params);
        UserDataService.approveUser(params);
      } else if (stake == "insurance") {
        user_email = this.a[2][k].email;
        params = {
          stakeholder: stake,
          email: user_email,
          verifiedFile: verifiedFile,
        };
        // params = JSON.stringify(params);
        UserDataService.approveUser(params);
      } else if (stake == "patient") {
        user_email = this.a[3][k].email;
        params = {
          stakeholder: stake,
          email: user_email,
          verifiedFile: verifiedFile,
        };
        // params = JSON.stringify(params);
        UserDataService.approveUser(params);
      } else if (stake == "pharmacy") {
        user_email = this.a[4][k].email;
        params = {
          stakeholder: stake,
          email: user_email,
          verifiedFile: verifiedFile,
        };
        // params = JSON.stringify(params);
        UserDataService.approveUser(params);
        this.fetchApprove();
      }
    },

    verify: async function (wallet_address, hashedFile, email, fileName) {
      
      //TODO: Test this
      var params = {
        stakeholder: "verify",
        uploader: email,
        originalFileName: fileName,
      };
      try{
        var res = await UserDataService.retrieveUser(params);
      }catch(err){
        alert("Looks like the user has not uploaded his file!")
        return;
      }
      var verificationStatus = res.data[0];
      try{
        var isVerified = verificationStatus.verified;
      }catch(err){
        alert("Looks like the user has not uploaded his file!")
        return;
      }
      var url = "";
      if (isVerified) {
        url = verificationStatus.URL;
        alert("The file has been verified but signature verification to be done\n " );
        // window.open(url, "_blank");
      } else {
        alert("This file may have been tampered with!");
        return -1;
      }

      //TODO: Test this end

      var signedFile = await this.getSignaturedFileFromSmartContract(
        wallet_address
      );

      if(!signedFile){
        this.check = 0;
        return false;
      }
      var signerAddress = await this.getTheSignerOfHashedFile(
        signedFile,
        hashedFile
      );
      if (signerAddress == wallet_address) {
        this.check=1;
        alert("File has not been tampered with and the user is also legitimate can be seen from "+url);
        return true;
      } else {
        this.check=0;
        alert("ALERT: The file has not been tampered with but the signer is incorrect");
        return false;
      }
    },
    getSignaturedFileFromSmartContract: async function (wallet_address) {
      let web3 = new Web3(window.ethereum);
      let contractAddress = "0x09a2fD8CEBBc51D28A5F39d4f5157644f10df05D";

      let abi = JSON.parse(
        `[{"inputs":[{"internalType":"string","name":"x","type":"string"}],"name":"addString","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"dict","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]`
      );

      let contract = new web3.eth.Contract(abi, contractAddress);
      try{
        var result = await contract.methods.dict(wallet_address).call();
        return result;

      }catch(err){
        alert("The file has was not uploaded on the Goerli Network")
      }
    },

    getTheSignerOfHashedFile: async function (signedFile, hashedFile) {
      try {
        var message = hashedFile; //checksum which is to be fetched from the mongodb.
        var signature = signedFile; //signed checksum which is to be fetched from the blockchain
        const signerAddr = await ethers.utils.verifyMessage(message, signature);
        return signerAddr;
      } catch (err) {
        return false;
      }
    },

    deny(k, stake) {
      var user_email;
      var verifiedFile = this.check;
      var params;
      if (stake == "doctor") {
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
        this.fetchApprove();
      }
    },
      
    fetchApprove: async function () {
        
      var b = await UserDataService.retrieveUnverifiedUsers();
      // b = JSON.stringify(b);
      this.a = b.data;
      this.$store.dispatch("updateUser", this.a);
      this.dummy();
    },



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

.idk {
  font-weight: bolder;
  font-size: 3rem;
  color: #82c8f7;
}
.idk2 {
  font-weight: bolder;
}
</style>
