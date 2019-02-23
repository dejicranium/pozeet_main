import Vue from 'vue'
import Profile from './Profile.vue'
import FeedItem from './home-components/FeedItem.vue'
import Sample from './Sample.vue'

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
   el: '#app-container',
  components: {'profile': Profile}

 })
 