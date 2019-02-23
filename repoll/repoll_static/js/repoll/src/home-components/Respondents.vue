	<template id='respondents-template'>
		<transition name='modal'>
			<div class="modal-mask" v-show='show_respondents_modal'>
				<div class="modal-container">
					<div class="container">
            			<div class="image">
                			<img src="https://pbs.twimg.com/profile_images/1081905771028320256/yajLUZzZ_400x400.jpg"/>
            			</div>
            			<div class="detail">
                			<div class="name">{{user.userName}}</div>
                			<div class="username">{{user.username}}</>
            			</div>
            			<div class="follow">
                			<button class="button">Follow</button>
            			</div>
        			</div>
				</div>
			</div>
		</transition>
	</template>


<script>
	var siteUrl = 'http://localhost:6543'

	export default {
		name: 'Respondents', 
		props: ['show_respondents_modalaa', 'activity'],

		data(){
			return{	
				respondents: [],
			}
		},
		watch:{
			show_respondents_modal: function(val){
				if (val == true){
					axios.get(siteUrl + '/voters/' + this.activity.id, {

					}).then(response=>{
						this.respondents = response.data;
					});
				}
			},
		},

		
	}

</script>