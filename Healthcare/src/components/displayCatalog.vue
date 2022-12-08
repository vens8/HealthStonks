<template>
    {{created()}}
    <!-- //<li v-for="(key) in Object.keys(c)">{{key}}:{{c[key]}}</li> -->
    <!-- <li v-for="i in c" :key="i.name">{{i.name}}</li> -->
    <li  style="list-style: none;" v-for="i,k in c" :key="i">
        <ul style="list-style: none;">
            {{k+1}}
        <li style="list-style: none;" v-for=" (j,l) in i" :key="j">
            {{l}}-->{{j}}
    </li>
    </ul>
    </li>
    <!-- <li v-for="i in c" :key="i.location">{{i.location}}</li> -->
</template>

<script>
export default {
    name: "displayCatalog",
    props: {},
    data: function () {
      return {  
        c:[{}],     
      };
    },
    methods:{
    created(){
        //b=localStorage.getItem('dict');
        //<li v-for="(key) in Object.keys(b)">{{key}}:{{b[key]}}</li>
         this.c= JSON.parse(localStorage.getItem('dict'));
        //this.c=this.$route.query.dict
         
   },
}}
</script>

