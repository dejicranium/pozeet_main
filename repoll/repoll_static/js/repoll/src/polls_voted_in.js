import Vue from 'vue'
import PollsVotedIn from './PollsVotedIn.vue';
import axios from 'axios'


Vue.mixin({ 
    methods:{
      changeButtonContent: (button, text) => {
       button.innerHTML = text;
     },
   
     showSnackbar: text => {
         var snackbar = document.getElementById('snackbar');
         snackbar.innerHTML = text;
   
         snackbar.className = "show";
   
       // After 3 seconds, remove the show class from DIV
         setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 4000);
   
     }
 
 
    }
  });
 
 new Vue({
   el: '#container',
   render: h => h(PollsVotedIn),
 })
 