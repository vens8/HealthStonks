<template>
  <div>
<!--  <button @click="fetchFiles("Please click to fetch ")">Fetch All Files</button> -->
<!--  {{fetchFiles("Please click to fetch docs")}} -->
  <!--  {{ created() }} -->
    <div class="c" v-for="i in c" :key="i">
      <button
        id="currButton"
        class="button"
        v-on:click="toggle"
        @click="fetchFiles(i.originalFileName)"
      >
        {{ i.originalFileName }}
      </button>
    </div>
  </div>
</template>

<script>
import UserDataService from "../service/backendDataService";
export default {
  name: "displayFiles",
  props: {},
  data: function () {
    return {
      //Dummy dictionary to add the list of dictionary files
      c: [{ originalFileName: "Please click to fetch docs" }],
      email: "",
    };
  },
  methods: {
    fetchFiles: async function (file) {
      var uploaderC = this.$store.getters.getUser[0].email;
      if (file == "Please click to fetch docs") {
        var params = {
          stakeholder: "files",
          uploader: uploaderC,
        };
        // params = JSON.stringify(params);
        var res = await UserDataService.fetchUser(params);
        this.c = res.data;
      } else {
        params = {
          stakeholder: "verify",
          originalFileName: file,
        };
        try {
          res = await UserDataService.retrieveUser(params);
        } catch (err) {
          alert("The file could not be verified");
          return;
        }
        var verificationStatus = res.data[0];
        try {
          var isVerified = verificationStatus.verified;
        } catch (err) {
          alert("The file could not be verified");
          return;
        }
        var url = "";
        if (isVerified) {
          url = verificationStatus.URL;
          alert("The file has been verified \n " + url);
          // window.open(url, "_blank");
        } else {
          alert("This file may have been tampered with!");
          return;
        }
      }
    },
  },
};
</script>
