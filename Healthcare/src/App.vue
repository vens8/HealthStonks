<template>
  <div class="wrapper">
    <testPage/>
  </div>
</template>

<script>
import testPage from './components/test.vue'

export default {
  components: {
    testPage
  },
  methods:{
    first(){
      this.$store.dispatch('updateUser', {airport: "Adsadasda"});
    },
    second(){
      this.$store.dispatch('updateUser', {airport: "plplplp"});
    },
    third(){
      console.log(this.$store.getters.getUser);
    }
  },
  
}
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

.wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-column-gap: 1rem;
  max-width: 960px;
  margin: 0 auto;
}

p,
h3 {
  grid-column: span 3;
}
</style>


