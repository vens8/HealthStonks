<template>
  <div>
    <div>
      <div class="navbar">
        <router-link to="/RegProfile" class="active"
          >Register Profile</router-link
        >
        <router-link to="/LoginPage">Login</router-link>
      </div>
    </div>

    <div>
      <vue-metamask ref="metamask" :initConnect="false"></vue-metamask>
      <vue-metamask userMessage="msg" @onComplete="onComplete"> </vue-metamask>

      <div class="start"><h1>Enter Details--></h1></div>
      <p>Name:</p>
      <input
        id="fullname"
        type="text"
        v-model="name"
        maxlength="100"
        placeholder="Edit your Name"
      />

      <button @click="connect">Connect Wallet</button>
      <label id="wallet_address"> </label>
      <p>Contact Number:</p>
      <input
        type="text"
        id="contact"
        v-model="phoneNo"
        maxlength="10"
        placeholder="Edit Contact Number"
      />

      <p>Upload your documents:</p>

      <p>Upload Profile Image:</p>

      <!-- {{ a.stakeHolder }} -->
      <form>
        <input id="file" type="file" name="file" />
        <br />

        <!-- <button type="reset" @click="uploadFile()">Upload</button> -->
      </form>

      <p>Upload Identification Document(Aadhar Card/Licence ):</p>
      <form>
        <input id="fileAdhaar" type="file" name="file" />
        <br />

        <!-- <button type="reset" @click="uploadAdhaar()">Upload</button> -->
      </form>

      <div class="b2">
        <br />
        <button type="button" @click="saveProfile()">Register</button>
      </div>
    </div>
  </div>
</template>

<script>
import Web3 from "web3";
import { ethers } from "ethers";
import VueMetamask from "vue-metamask";
import axios from "axios";
import UserDataService from "../service/backendDataService";
export default {
  name: "RegProfile",
  components: {
    VueMetamask,
  },
  props: {
    msg: String,
  },
  data() {
    return {
      a: this.$store.getters.getUser[0],
    };
  },
  methods: {
    uploadFile: async function () {
      console.log("reached");
      var formData = new FormData();
      var imagefile = document.querySelector("#file");
      formData.append("stakeholder", this.a.stakeHolder);
      formData.append("uploader", this.a.email);
      formData.append("type", "image");
      var uploadField = document.getElementById("file");
      if (uploadField.files[0].size > 5000000) {
        alert("File is too big!");
        this.value = "";
        return;
      }

      formData.append("image", imagefile.files[0]);
      formData.append("access", "admin");
      var response = await axios.post(
        "https://192.168.2.251:5000/uploadFile",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      var hashedCheckSum = response.data["hash"];
      console.log(hashedCheckSum);
    },

    uploadAdhaar: async function () {
      console.log("reached");
      var formData = new FormData();
      var imagefile = document.querySelector("#fileAdhaar");
      var uploadField = document.getElementById("fileAdhaar");
      formData.append("type", "poi");
      if (uploadField.files[0].size > 5000000) {
        alert("File is too big!");
        this.value = "";
        return;
      }
      formData.append("type", "poi");
      formData.append("stakeholder", this.a.stakeHolder);
      formData.append("uploader", this.a.email);
      formData.append("image", imagefile.files[0]);
      formData.append("access", "admin");
      var response = await axios.post(
        "https://192.168.2.251:5000/uploadFile",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      var hashedCheckSum = response.data["hash"];
      console.log(hashedCheckSum);
      await this.signMessage(hashedCheckSum);
    },
    signMessage: async function (message) {
      try {
        // var message = "Hello";//computed checksum to be fetched from mongodb
        console.log(message);
        if (!window.ethereum)
          throw new Error("No crypto wallet found. Please install it.");

        await window.ethereum.send("eth_requestAccounts");
        const provider = new ethers.providers.Web3Provider(window.ethereum);
        const signer = provider.getSigner();
        const signature = await signer.signMessage(message);
        const address = await signer.getAddress();
        console.log(message, address, signature);
        await this.storeOnContract(signature);
        return {
          message,
          signature,
          address,
        };
      } catch (err) {
        alert(err.message);
      }
    },
    saveProfile: async function () {
      //addded here
      //var params = {"stakeholder":"insurance", "email": "none", "location": "none", "speciality":"none"};
      // params = JSON.stringify(params)
      //var a = await UserDataService.retrieveUser(params);
      // var name1 = document.getElementById("name").value;
      //   if (!(name1.length > 0)) {
      //     alert("Please enter Name");
      //     return;
      //   }
      var wallet_address =
        document.getElementById("wallet_address").textContent;

      if (wallet_address.length == 0) {
        alert("Please connect your wallet");
        return;
      }
      var stakeHolder = this.a.stakeHolder; // Hardcoding for now, otherwise it must be taken from current login state (Vuex store)
      if (!stakeHolder) {
        alert(
          "Suspicious Behaviour, please go to register page and try again."
        );
        return;
      }

      var name = document.getElementById("fullname").value;
      if (name.length > 100) {
        alert("Looks like you have a long name, just your first name will do!");
        return;
      }
      if (name.length == 0) {
        alert("How should we address you? Please enter a name");
        return;
      }

      var phoneNo = document.getElementById("contact").value;
      if (phoneNo.length != 10) {
        alert("Phone number should be of length 10");
        return;
      }

      var regexForPhoneNo = /^[0-9]+$/;
      if (!phoneNo.match(regexForPhoneNo)) {
        alert("Please input numeric characters only");
        return;
      }

      // if(Number(phoneNo) === NaN){
      //   alert("Phone number should only have digits");
      //   return;
      // }

      var uploadField = document.getElementById("fileAdhaar");

      if (uploadField.files.length < 1) {
        alert("Adhaar File has not been uploaded");
        return;
      }
      if (uploadField.files[0].size > 5000000) {
        alert("Adhaar File is too big!");
        this.value = "";
        return;
      }

      uploadField = document.getElementById("file");

      if (uploadField.files.length < 1) {
        alert("Profile pic has not been uploaded");
        return;
      }
      if (uploadField.files[0].size > 5000000) {
        alert("Profile pic is too big!");
        this.value = "";
        return;
      }

      //console.log(this.$store.getters.getUser[0]);
      //var email = a.email; // Hardcoding for now, otherwise it must be taken from current login state (Vuex store)
      //    var currentPassword = document.getElementById("currentPassword").value;
      //    var newPassword = document.getElementById("newPassword").value;
      //    var newPasswordRepeat =
      //      document.getElementById("newPasswordRepeat").value;
      // console.log(stakeHolder);
      // console.log(uid);
      // console.log(passWord);
      //var specialty= document.getElementById("specialty").value;
      //    var location = document.getElementById("location").value;
      // var contact = document.getElementById("contact").value;

      var params = {
        request: "register",
        stakeHolder: stakeHolder,
        email: this.a.email,
        name: name,
        phoneNo: phoneNo,
        wallet_address: wallet_address,
        //  location: location,
        // specialty: specialty,
        //  currentPassword: currentPassword,
        //  newPassword: newPassword,
        //  newPasswordRepeat: newPasswordRepeat,
      };
      if (this.a.stakeHolder != "patient") {
        var licenceNo = this.a.licenceNo;
        params["licenceNo"] = licenceNo;
      }
      //    message="User registered successfully. Request sent to admin for approval";
      // params = JSON.stringify(params);

      await this.uploadFile();
      await this.uploadAdhaar();
      var b = await UserDataService.registerUser(params);
      console.log(b);
      var one = 1;
      if (one == 1) {
        alert("Successfully Registered! Wait for ADMIN approval.");
      } else {
        return;
      }
    },
    fetchFile: async function () {
      // var params = {
      //   stakeholder: "files",
      //   uploader: 'naman@gmail.com'
      // };
      // params = JSON.stringify(params);
      // var res = await UserDataService.retrieveUser(params);
      // console.log(res.data);
    },

    storeOnContract: async function (signedHashedChecksum) {
      // method for calling the contract method
      let web3 = new Web3(window.ethereum);
      let contractAddress = "0x09a2fD8CEBBc51D28A5F39d4f5157644f10df05D";

      let abi = JSON.parse(
        `[{"inputs":[{"internalType":"string","name":"x","type":"string"}],"name":"addString","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"dict","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]`
      );

      let contract = new web3.eth.Contract(abi, contractAddress);
      const accounts = await web3.eth.getAccounts();
      contract.methods
        .addString(signedHashedChecksum)
        .send({ from: accounts[0] })
        .then((result) => console.log(result));
      // contract.methods
      //   .dict("0x4db6dA149E0C58B94C66FfAb202DaD9f6aC6F1aE")
      //   .call()
      //   .then((result) => console.log(result));
      // console.log(contract.options.jsonInterface);
    },

    onComplete(data) {
      console.log("data:", data);
      var metamaskWalletAddress = data["metaMaskAddress"];
      console.log(metamaskWalletAddress);
      document.getElementById("wallet_address").innerHTML =
        metamaskWalletAddress;
    },

    connect() {
      this.$refs.metamask.init();
    },

    verify: async function () {
      // var params = {
      //   stakeholder: "verify",
      //   uploader: 'naman@gmail.com',
      //   originalFileName: 'sample.pdf'
      // };
      // params = JSON.stringify(params);
      // var res = await UserDataService.retrieveUser(params);
      // console.log(res.data);
    },
    sendEmail: async function () {
      var email = document.getElementById("emailID").value;
      if (!(email.length > 0)) {
        alert("Please enter email ID");
        return;
      }
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

.b2 {
  text-align: center;
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
