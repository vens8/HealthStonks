<template>
  <div id="demo">
    <vue-metamask ref="metamask" :initConnect="false"></vue-metamask>
    <vue-metamask userMessage="msg" @onComplete="onComplete"> </vue-metamask>
    <button @click="connect">connect</button>

    <button @click="storeOnContract">Call contract</button>
    <button @click="verifyMessage">Call contract</button>

    displays the result of the contract
  </div>

  <!-- <form>
    <input id="file" type="file" name="file" />
    <br />
    
    <button  type="reset" @click="uploadMyFile()">Upload</button>
  </form> -->
</template>
<script>
// import axios from 'axios'
import Web3 from "web3";
import { ethers } from "ethers";
// import VueMetamask from "vue-metamask";
export default {
  name: "testPage",
  components: {
    // VueMetamask,
  },
  data() {
    return {
      msg: "This is demo net work",
    };
  },

  methods: {

    // uploadMyFile: async function () {
    //   console.log("reached");
    //   var formData = new FormData();
    //   var imagefile = document.querySelector("#file");
    //   formData.append("stakeholder", "pharmacy");
    //   formData.append("uploader", "naman20088@iiitd.ac.in");
    //   formData.append("image", imagefile.files[0]);
    //   formData.append("access", "admin");
    //   var response = await axios.post("https://192.168.2.251:5000/uploadFile", formData, {
    //     headers: {
    //       "Content-Type": "multipart/form-data",
    //     },
    //   });
    //   var hashedCheckSum = response.data['hash']
    //   console.log(hashedCheckSum);
    //   this.signMessage(hashedCheckSum);
    // },
    verifyMessage: async function () {
      try {

        var message = "2d8695aeadb329acf796b9dc6956ea1050f4c9acc08897d86e5e48b360db6665"//checksum which is to be fetched from the mongodb.
        var address = "0x4db6dA149E0C58B94C66FfAb202DaD9f6aC6F1aE" //wallet address to be fetched from vuestore which was called from mongodb
        var signature = "0x5e1b697415d95b28be40c0aaa07a407df65678b102e78e1464f1b3f04f34816933e5d09d152a050ca7c5f5d12eefdda88fa6c35376b820ed5ef01860080825f71c" //signed checksum which is to be fetched from the blockchain
        const signerAddr = await ethers.utils.verifyMessage(message, signature);
        if (signerAddr !== address) {
          console.log("Invalid signature");
          return false;
        }
        console.log("Correct signature");
        return true;
      } catch (err) {
        console.log(err);
        console.log("Invalid signature");
        return false;
      }
    },

    // signMessage: async function (message) {
    //   try {
    //     // var message = "Hello";//computed checksum to be fetched from mongodb
    //     console.log(message);
    //     if (!window.ethereum)
    //       throw new Error("No crypto wallet found. Please install it.");

    //     await window.ethereum.send("eth_requestAccounts");
    //     const provider = new ethers.providers.Web3Provider(window.ethereum);
    //     const signer = provider.getSigner();
    //     const signature = await signer.signMessage(message);
    //     const address = await signer.getAddress();
    //     console.log(message, address, signature);
    //     this.storeOnContract(signature);
    //     return {
    //       message,
    //       signature,
    //       address,
    //     };
    //   } catch (err) {
    //     alert(err.message);
    //   }
    // },
    // verifyMessage: async function () {
    //   try {

    //     var message = "Hello"//checksum which is to be fetched from the mongodb.
    //     var address = "0x4db6dA149E0C58B94C66FfAb202DaD9f6aC6F1aE" //wallet address to be fetched from vuestore which was called from mongodb
    //     var signature = "0xc0f370c8195a1f7edcc7b8fdacdf0ef9f52454606b2db90b682bd346dedf1b9c0161d7b8ded1553f15c782c282c4f06dea1de238b30a5d9bc8e52d39bbe9745d1c" //signed checksum which is to be fetched from the blockchain
    //     const signerAddr = await ethers.utils.verifyMessage(message, signature);
    //     if (signerAddr !== address) {
    //       console.log("Invalid signature");
    //       return false;
    //     }
    //     console.log("Correct signature");
    //     return true;
    //   } catch (err) {
    //     console.log(err);
    //     console.log("Invalid signature");
    //     return false;
    //   }
    // },

    // signMessage: async function () {
    //   try {
    //     var message = "Hello";//computed checksum to be fetched from mongodb
    //     console.log(message);
    //     if (!window.ethereum)
    //       throw new Error("No crypto wallet found. Please install it.");

    //     await window.ethereum.send("eth_requestAccounts");
    //     const provider = new ethers.providers.Web3Provider(window.ethereum);
    //     const signer = provider.getSigner();
    //     const signature = await signer.signMessage(message);
    //     const address = await signer.getAddress();
    //     console.log(message, address, signature);
    //     return {
    //       message,
    //       signature,
    //       address,
    //     };
    //   } catch (err) {
    //     alert(err.message);
    //   }
    // },

    storeOnContract: async function () {
      // method for calling the contract method
      let web3 = new Web3(window.ethereum);
      let contractAddress = "0x09a2fD8CEBBc51D28A5F39d4f5157644f10df05D";

      let abi = JSON.parse(
        `[{"inputs":[{"internalType":"string","name":"x","type":"string"}],"name":"addString","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"dict","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]`
      );

      let contract = new web3.eth.Contract(abi, contractAddress);
      // const accounts = await web3.eth.getAccounts();
      // contract.methods
      //   .addString(signedHashedChecksum)
      //   .send({ from:accounts[0] })
      //   .then((result) => (console.log(result)));
      var result = await contract.methods
        .dict("0x4db6dA149E0C58B94C66FfAb202DaD9f6aC6F1aE")
        .call();

      // console.log(result);
      // console.log(contract.options.jsonInterface);
    },

    onComplete(data) {
      console.log("data:", data);
      var metamaskWalletAddress = data["metaMaskAddress"];
      console.log(metamaskWalletAddress);
    },

    connect() {
      this.$refs.metamask.init();
    },
  },
};
</script>

<style scoped></style>
