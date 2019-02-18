import Vue from 'vue'
import Notification from './Notification.vue'
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
  el: '#app',
  delimiters: ["((", "))"],
  render: h => h(Notification)
})
