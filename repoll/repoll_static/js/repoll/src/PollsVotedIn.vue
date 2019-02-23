<template>
    <div id="sub-container">


		<div>
			<feed-item 
				v-for="activity in activities" 
				:activity='activity'>	
			</feed-item>
		</div>
	
	</div>

</template>


<script>
import axios from 'axios';
import FeedItem from './home-components/FeedItem.vue';


    var showSnackbar = function(text){
		var snackbar = document.getElementById('snackbar');
		snackbar.innerHTML = text;

    	snackbar.className = "show";

    // After 3 seconds, remove the show class from DIV
    	setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 4000);

	}
var siteUrl = "";
	


export default {
    name: "PollsVotedIn",
   
	delimiters: ['((','))'],
	components: { 
      'feed-item': FeedItem, 
    },
		data(){
			return{
				activities: [],
			}
		},

		computed:{

		},

		methods:{


		},


		//this is what happens when you load the page.
		//automaticall
		created(){
			axios.get("" + '/get_polls_voted_in').then(response => {
			//this will give a list of polls
			var response_list = response.data.activities;
			this.activities = response_list;

			

			
			});

			//get categories data



		},

}
</script>

