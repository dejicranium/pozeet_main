import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'

Vue.config.devtools = true


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
        setTimeout(function(){
           snackbar.className = snackbar.className.replace("show", ""); }
           , 4000);
  
    }


   }
 });
new Vue({
  el: '#app',
  delimiters: ["((", "))"],
  render: h => h(App)
})
