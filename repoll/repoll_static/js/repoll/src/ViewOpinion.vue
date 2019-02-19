<template>
    <div class="body-container">
    	<div>
        	<div class="feed-container">
				<div class="feed-card">
					<div class="avatar">
                         <img style="color:darkgrey; font-size:12px;"
						  	v-if='!poll.userPic' src="https://www.w3schools.com/howto/img_avatar.png"/>
						 <img v-else :src='poll.userPic'>
                    </div>
				
                    <div class="beside-avatar-box">

                        <div class="author-details">
                            <p class="name" style='color;black; font-weight:bold; font-size:12px;'>{{poll.userName}}</p>
                            <p class="username"></p>
							<p class='time-added' style='color:darkgrey; font-size: 12px'>{{poll.timeAddedd}}</p>
                        </div>

                        <div class="comment" style='white-space:; font-size:13px; margin-bottom:5px;'>{{poll.opinion}}</div>
						<div style='display:flex; flex-direction:row;'>
							<img id='opinionContextImage' v-for='image in poll.contextImage' :image='image' :src='image.imgLink' style='max-width:60%; max-height:200px; border-radius:5px;'>

						</div>
						<p class='votes'>{{poll.totalVotes}} reactions</p>



						<button @click='addComment("Agree")'><i class="fa fa-check button-icon" aria-hidden="true"></i>Agree</button>
						<button @click='addComment("Disagree")'><i class="far fa-thumbs-down button-icon"></i>Disagree</button>
						<button  @click='openBreakDownWindow'><i class="fas fa-chart-pie button-icon"></i>View Breakdown</button>

					</div>
			

            </div>

			<!--This div will be shown for poll activities --> 
		</div>

	</div>
	<div class='addCommentBox' v-show="intent == 'toComment' && !poll.userHasVoted">
		<form id='comment-form'>
			<p class='chosenOption'>{{chosenOptionName}}</p>
			<textarea type="text" placeholder='Reason' @click="autoResize" name='comment' id='comment-form'></textarea>
			<button @click='comment'>Comment</button>
		</form>
	</div>

		<div class="other-details">
            <div class="tab-header">
                <div class="tab all" style="border-bottom: 1px solid teal;"
				id='*'
				@click='makeTabActive("*")'
				:class="[isActiveTab('*') ? isActiveClass : '']">
                    <p>All</p>
                </div>

                <div class="tab" v-for='option in poll.options'
					 :option='option'
					 :id='option.id'
					 @click='makeTabActive(option.id)'>
                    <p>{{option.option}}</p>
                </div>
            </div>

            <!--COMMENT COMPONENT-->
			<comment v-for='comment in sortedComments' @change_can_agree_state='changeCanAgreeWithCommentsState' :comment='comment' :replies='replies' :can_agree_to_comments='canAgreeToComments'></comment>

		</div>
	</div>
	
</template>


<script>
var siteUrl = "http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com:6543";
	const activityPOSTURL = "";

    import axios from 'axios';
	import Comment from './view-converstation-components/ConvoComment.vue'
    export default {
        name: 'ViewOpinion', 
        components: {
            'comment': Comment,
        },
		props: ['comment', 'can_agree_to_comments'],
		
        data(){
			return{
            	some: 'deji',
				loading: true,
            	poll: {}, //it'a list because we want it to be reactive.
				chosenOption: 0,
				user_logged_in: false,
				comments: [], 
				activeTab: '*',
				tabs: [],
				isActiveClass: 'isActive',
				intent: '',
				chosenOptionName: '',
				canAgreeToComments: false, //this will make us know whether user can press agree on another comment
				commentToAgreeWith: 0, 
			}
             
        },


        methods:{


			openBreakDownWindow(){

				window.open("" + '/opinion/demographic-metrics/' + this.poll.id);
			
			
			},
			changeCanAgreeWithCommentsState(optionVotedFor){
				this.canAgreeToComments = false;
				this.changePollData('userHasVoted', true);
				this.changePollData('totalVotes', this.poll.totalVotes + 1);
				
				for (var i = 0; i < this.poll.options.length; i++){
					if (this.poll.options[i].id  == optionVotedFor){
						this.poll.options[i].score += 1;
						break;
					}
				}
			},
			autoResize(event){
				event.preventDefault();
				var textarea = event.target;
				textarea.addEventListener('input', function(){
					var currentHeight = textarea.offsetHeight;
					var scrollHeight = textarea.scrollHeight;
					if (scrollHeight > currentHeight){
						textarea.style.height = scrollHeight + 'px';
					}
				});
			},

            changePollData(id, value){
                this.$set(this.poll, id, value);
            },

			makeTabActive(tabName){
				this.activeTab = tabName;

				var tabs = document.getElementsByClassName('tab');
				var activeTab = document.getElementById(this.activeTab);
				
				for (let i =0; i < tabs.length; i++){
					tabs[i].style.borderBottom = '0px solid';
				}
				activeTab.style.borderBottom = "2px solid teal";

				
			},

			isActiveTab(tabName){
				this.activeTab == tabName;
			},


			optionChosen(id){
				this.chosenOption = id;

			},



			vote(){
				var vm = this;
				if (this.user_logged_in == false){
					return 0;
				}

				this.changePollData('userHasVoted', true);
				this.canAgreeToComments = false;
				this.changePollData('totalVotes', this.poll.totalVotes + 1);
				
				for (var i = 0; i < this.poll.options.length; i++){
					if (this.poll.options[i].id  == this.chosenOption){
						this.poll.options[i].score += 1;
						break;
					}
				}
				axios.post(activityPOSTURL + '/vote/',{
					poll_id: vm.poll.id, 
					option_id: vm.chosenOption,
				}).then(function(response){
					
				}).catch(function(error){
				
				});

				

			
			},

			addComment(optionName){
				if (this.user_logged_in == false){
					return 0;
					
				}
				this.chosenOptionName = optionName;
				this.intent = 'toComment';

				//look for the id of the option that has the option name;
				var optionWithName = this.poll.options.filter(o=> o.option == optionName);
				//make it the id of the option the chosen option
				this.chosenOption = optionWithName[0].id;
			},

			comment(event){
				event.preventDefault();
				var commentForm = document.getElementById('comment-form');
				var formData = new FormData(commentForm);
				formData.append('opinion_id', this.poll.id);
				formData.append('option_id', this.chosenOption);
				var request =  new XMLHttpRequest();
				var vm = this;

				request.open('POST', activityPOSTURL + "/comment/");
				request.onreadystatechange = function(){
					if (request.readyState = XMLHttpRequest.DONE){
						if (request.status == 200){
							vm.changePollData('userHasVoted', true);
							vm.changePollData('totalVotes', vm.poll.totalVotes + 1);
							vm.canAgreeToComments = false;
							for (var i = 0; i < this.poll.options.length; i++){
								if (this.poll.options[i].id  == this.chosenOption){
								this.poll.options[i].score += 1;
								break;
							}
							window.location.reload();				
						}

					}
					else{

					}
				}
			}
			request.send(formData);

        	},

		},
		computed:{
			
			totalVotes(){
				return this.poll.totalVotes;
			},


			sortedComments(){
				if (this.activeTab != '*'){
					return this.comments.filter(a=> a.optionId == this.activeTab);
				
				}

				//when active tab is "All"
				return this.comments;

			},

		},

        created(){
            var vm = this;
			
			var idOfPollToBeViewed = document.getElementById('idOfPollToBeViewed').innerHTML;
			idOfPollToBeViewed = parseInt(idOfPollToBeViewed);
            axios.get("" + '/opinion/' + idOfPollToBeViewed)
			
            .then(function(response){
				vm.user_logged_in = response.data.user_logged_in;
                vm.changePollData('opinion', response.data.opinion);
                vm.changePollData('userName', response.data.userName);
                vm.changePollData('type', response.data.type);
                vm.changePollData('id', response.data.id);
                vm.changePollData('userPic', response.data.userPic);
                vm.changePollData('totalVotes', response.data.numOfVotes);
				vm.changePollData('numOfShares', response.data.numOfShares);
				vm.changePollData('numOfLikes', response.data.numOfLikes);
                vm.changePollData('options', response.data.options);
                vm.changePollData('userHasVoted', response.data.userHasVoted);
				vm.changePollData('imageInfo', response.data.imageInfo);
				vm.changePollData('timeAdded', response.data.timeAdded);
				vm.changePollData('userIsFollowing', response.data.userIsFollowing);
				vm.changePollData('contextImage', response.data.contextImage);

				//should users be allowed to agree to a comment?
				//it all starts from knowing whether they have voted before.
				if (vm.poll.userHasVoted){
					vm.canAgreeToComments == false;
				}
				else{
					vm.canAgreeToComments = true;
				}
				
				vm.loading = false;
            }).catch(function(error){
					vm.loading = false;
			    }
            
            );


			axios.get('http://localhost:6543/comments/opinion/' + idOfPollToBeViewed,{

			}).then(function(response){
				vm.comments = response.data.comments;
			})
        },

    }


</script>

<style scoped>
.comment {
box-sizing: border-box;
word-wrap: break-word;
padding-bottom: 2px;
width: 100%;
border-radius: 0;
margin-top: 0F; 
margin-bottom: 0;
white-space: pre-wrap;
}

.addCommmentBox {
	height: 0px;
}
</style>
