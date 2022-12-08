<template>
  <router-view />
  <!-- <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/>
  <div>
    <LoginPage msg="Please enter your credentials" />
    <RegisterPage /> 
    <ProfilePatient/>
    <FindADocPage/>
  </div>  -->
</template>

<script>
// import RegisterPage from "./components/RegisterPage.vue";
// import LoginPage from "./components/LoginPage.vue";
// import ProfilePatient from "./components/ProfilePatient.vue";
// import FindADocPage from "./components/FindADocPage.vue"

export default {
  name: "App",
  components: {
    // RegisterPage,
    // LoginPage,
    // ProfilePatient,
    // FindADocPage,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
