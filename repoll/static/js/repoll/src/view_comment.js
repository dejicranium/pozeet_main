import Vue from 'vue'
import ConvoComment from './view-converstation-components/ConvoComment.vue'
import ViewComment from './ViewComment.vue'
import axios from 'axios'

Vue.config.devtools = true;

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
   el: '.body-container',
   components: {'comment': ConvoComment},
   delimiters: ["((", "))"],
   render: h => h(ViewComment),
 });
 