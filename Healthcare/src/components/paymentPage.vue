<template>
  <div>
    <div class="navbar">
      <a href="#home">Home</a>
      <a href="#Profile">Profile</a>
      <a href="#contact">Contact</a>
      <a href="#FindADoc" class="active">Find A Doctor</a>
    </div>
    <div class="start"><h1>PAYMENT PORTAL</h1></div>
    <div class="buttons">
      <h3>Amount to be paid is</h3>
      <h5>
        To confirm that you want to proceed with this payment please enter the
        OTP
      </h5>
      <button type="submit" @click="submit">Get OTP</button><br /><br />
      <!-- ADD OTP FUNCTIONALITY HERE -->
    </div>
  </div>
</template>
   <script>
export default {
  data() {
    return {
      isActive: false,
    };
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
button {
  background-color: #05c2f7;
  border: thick;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  border-radius: 8px;
  font-size: 26px;
}

input[type="text"]:focus {
  background-color: hsl(0, 0%, 95%);
}
</style>