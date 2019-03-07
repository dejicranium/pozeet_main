    <template>
	<div class='body-container'>
		<authentication-modal :activity_to_refer="activity_to_refer" :categories="sortedCategoriesList" :show_authentication_modal="showAuthenticationModal" @close_auth_modal="closeModal"></authentication-modal>	


        <div class="feed-container">
            <div class="feed-card" tabindex='0'>
                

				<div class="avatar">
                     <img v-if='poll.userPic == null' src="https://www.w3schools.com/howto/img_avatar.png"/> 
					 <img v-else :src='poll.userPic'>
                </div>


                <div class="beside-avatar-box">
                    <div class="author-details" @click="openUserProfile">
                        <p class="name" style="font-size: 12px;">{{poll.userName}}</p>
                        <p class="username" style="font-size:12px; color:darkgrey">({{poll.username}})</p>
						<p class='time-added' style="font-size:12px; color:darkgrey;">{{poll.timeAdded}}</p>

					</div>

                    <h6 class="poll-question"><a :href="'/poll/' + poll.id + '/'">{{poll.question}}</a></h6>

					<div class="poll-info">
						<div v-if='poll.hasUrlInfo' class='link-info' style='display:flex; padding: 5px;; flex-direction:row; border:0.5px solid lightgrey; border-radius:10px;'>
							<img :src='poll.infoPageThumb' width='150' height='100' style='margin-right:5px;'/>
							<div style='display:flex; flex-direction:column'>
								<h4>{{poll.infoPageTitle}}</h4>
								<p>{{poll.infoPageDescription}}</p>
							</div>
						</div>
						<div v-if='poll.info' style='margin-bottom:3px; white-space:;'>
							{{poll.info}}
						</div>

						<div v-if='poll.imageInfo'>
							<img :src='poll.imageInfo' style=' max-width: 100%; max-height:300px; border-radius:10px'>
						</div>
					</div>


					<template v-if='!poll.hasEnded'>						
						<!-- this is the default. Shows when the user has not voted -->
						<template v-if='!poll.isPicturePoll'>
							<template v-if='!poll.userHasVoted && !poll.seenPollResults'>
								<div class='options' v-for='option in poll.options' :option='option'>
										<label>
											<input type="radio" @click='optionChosen(option.id)' name='option' :value='option.id'>
											<span class='checkmark'></span>
											{{option.option}}
										</label>

								</div>
							</template>
						<!-- once the user has voted, this template will come up! --> 
						<!--<template v-else-if='userHasVoted && !isPicturePoll'>
						--> 
							<template v-else-if="poll.userHasVoted || poll.seenPollResults">
								<div class='options'>
	 								<div class="ans-cnt" v-for="option in calculatedScores" :option='option'>
										<div class="ans">
                                			<div class="ans-voted">
                                    			<span class="percent">{{option.percent}}</span>
                                    			<span class="txt">{{option.option}}</span>
                                			</div>
                                			<span class="first-bg"></span>
                                			<span :class="{bg:true}" :style='{width: option.percent}'></span>
                            			</div>
									</div>
                    			</div>
							</template>

						</template>

						<template v-else>
							<template v-if='!poll.userHasVoted && !poll.seenPollResults'>
				   				<div class='picture-options'>
									<label v-for='option in poll.options' :option="option">
										<input type='radio' @click='optionChosen(option.id)' name='option' :value='option.id'/>
										<img :src='option.image'/>
							
										<span class='checkbox'></span>

										<span>{{option.option}}</span>
						 			</label>

				   				</div>
							</template>

							<template v-else-if='poll.userHasVoted || poll.seenPollResults'>
				   				<div class='picture-options'>
									<label v-for='option in calculatedScores' :option="option">
										<input type='radio'  @click='optionChosen(option.id)' name='option' :value='option.id'/>
										<img :src='option.image'/>
							
										<!--<span class='checkbox' style='opacity:0'></span>-->
										<label style='background-color: rgba(0, 0, 0, .1);' :style='{width:option.percent}'>
										<span style='color:black;font-weight:bold;'>{{option.percent}}</span>
										</label>
						 			</label>

				   				</div>

							</template>
						</template>
					</template>

					<template v-else>
						<template v-if='!poll.isPicturePoll'>
								<div class='options'>
	 								<div class="ans-cnt" v-for="option in calculatedScores" :option='option'>
										<div class="ans">
                                			<div class="ans-voted">
                                    			<span class="percent">{{option.percent}}</span>
                                    			<span class="txt">{{option.option}}</span>
                                			</div>
                                			<span class="first-bg"></span>
                                			<span :class="{bg:true}" :style='{width: option.percent}'></span>
                            			</div>
									</div>
                    			</div>
						</template>
						
						<template v-else>
				   			<div class='picture-options'>
								<label v-for='option in calculatedScores' :option="option">
									<input type='radio' @click='optionChosen(option.id)' name='option' :value='option.id'/>
									<img :src='option.image'/>
							
										<!--<span class='checkbox' style='opacity:0'></span>-->
									<label style='background-color: rgba(0, 0, 0, .1);' :style='{width:option.percent}'>
									<span style='color:black;font-weight:bold;'>{{option.percent}}</span>
									</label>
						 		</label>

				   			</div>

						</template>
					</template> 

					<div style='display:flex; flex-direction="row"'>
                    	<p class="votes">{{poll.totalVotes}} votes </p>
                    <p class="votes" style="color:darkgrey;cursor:pointer;"> {{poll.timeRemaining}}</p>
					
					</div>

					<button v-on:click='vote' v-show='!poll.userHasVoted && !poll.seenPollResults' id='vote-btn'><i class="far fa-check-circle button-icon"></i>Vote</button>
                    <button v-on:click='addComment' v-show='!poll.userHasVoted && !poll.seenPollResults' id='comment-btn'><i class="far fa-comment button-icon"></i>Comment</button>
                    <button v-on:click='seeResults' v-show='!poll.userHasVoted && !poll.seenPollResults'><i class="far fa-chart-bar button-icon"></i>Results</button>
					<button  @click='openBreakDownWindow' v-show='poll.userHasVoted || poll.seenPollResults'><i class="fas fa-chart-pie button-icon"></i>View Breakdown</button>
                </div>
					
			</div>
		</div>

<div class='addCommentBox start' v-show="intent == 'toComment' && !poll.userHasVoted">
		<form id='comment-form'>
			<p class='chosenOption'>{{chosenOptionName}}</p>
			<textarea type="text" placeholder='Reason' @click="autoResize" name='comment' id='comment-form'></textarea>
			<button @click='comment'>Comment</button>
		</form>
	</div>

		<div class="other-details">
            <div class="tab-header">
                <div class="tab all" style="border-bottom: 1px solid teal;"
				onclick="showTabContent(this, 'polls')" 
				id='*'
				@click='makeTabActive("*")'
				:class="[isActiveTab('*') ? isActiveClass : '']">
                    <p>All</p>
                </div>

                <div class="tab" v-for='option in poll.options'
					
					 :option='option'
					 :id='option.id'
					 onclick="showTabContent(this, 'opinions')" 
					 @click='makeTabActive(option.id)'
					 >
					 
                    <p>{{option.option}}</p>
                </div>





				<!--
                <div class="tab" onclick="showTabContent(this, 'c_and_s')" @click='getCommentsAndReplies'>
                    <p>Comments & Replies</p>
                </div>

            	<div class="tab" onclick="showTabContent(this, 'l_and_s')">
                    <p>Likes & Shares</p>
                </div>

				-->
            </div>
			<comment v-for='comment in sortedComments' 
			@change_can_agree_state='changeCanAgreeWithCommentsState'
			:origin="'poll'"
			 :comment='comment' 
			 :replies='replies' 
			 :can_agree_to_comments='canAgreeToComments'></comment>


		</div>
	
	</div>

</template>

<script>
    import AuthenticationModal from './home-components/AuthenticationModal.vue';
    import Comment from './home-components/Comment.vue';
	import axios from 'axios';
	
	var siteUrl = ""; 
	const activityPOSTURL = "";


    export default {
        name: 'ViewPoll',
        components: {
            'authentication-modal': AuthenticationModal, 
            'comment': Comment,
        },

        data(){
			return{
				activity_to_refer: {},
				loading: true,
            	some: 'deji',
            	poll: {}, //it'a list because we want it to be reactive.
				chosenOption: 0,
				user_logged_in: false,
				comments: [], 
				activeTab: '*',
				tabs: [],
				isActiveClass: 'isActive',
				intent: '',
				showAuthenticationModal: false,
				categories:  [],


				canAgreeToComments: false, //this will make us know whether user can press agree on another comment
				commentToAgreeWith: 0, 
			}
             
        },


        methods:{
			_sortCategoryList(list){
				list.sort(function(a, b){
					if (a.categoryName < b.categoryName) return -1;
					if (a.categoryName > b.categoryName) return 1;
				})
				return list;
			},

			openBreakDownWindow(){

				window.open("" + '/opinion/demographic-metrics/' + this.poll.id, '_self');
			
			
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

			closeModal(){
				this.showAuthenticationModal = false;
			},

			isActiveTab(tabName){
				this.activeTab == tabName;
			},


			optionChosen(id){
				this.chosenOption = id;

			},

			vote(){
				var vm = this;
				if (vm.user_logged_in == false){
					this.activity_to_refer = this.poll;
					this.showAuthenticationModal = true;
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
				axios.post("" + '/vote/',{
					poll_id: vm.poll.id, 
					option_id: vm.chosenOption,
				}).then(function(response){
					
				}).catch(function(error){
				
				});

		
			},

			addComment(){
				if (this.user_logged_in == false){
					this.activity_to_refer = this.poll;
					this.showAuthenticationModal = true;
					return 0;
				
				}
				this.intent = 'toComment';
			},

			comment(event){
				event.preventDefault();
				var commentForm = document.getElementById('comment-form');
				var formData = new FormData(commentForm);
				formData.append('poll_id', this.poll.id);
				formData.append('option_id', this.chosenOption);
				var request =  new XMLHttpRequest();
				var vm = this;

				request.open('POST', activityPOSTURL + "/comment/");
				vm.changeButtonContent(event.target, '...');

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
							vm.changeButtonContent(event.target, 'Comment');
							window.location.reload();				
						}

					}
					else{

					}
				}
			}
			request.send(formData);

			

        	},
			seeResults: function(){
				var vm = this;
				var result = true;
				if (this.user_logged_in == false){
					this.activity_to_refer = this.poll;
					this.showAuthenticationModal = true;
					return 0;
				}

					axios.post("" + '/viewresults',{
						poll_id: this.poll.id,
					}).then(function(response){
						vm.seenPollResults = true;
					}).catch(function(error){
						vm.seenPollResults = false;

				});

				
				
			},

		},
		watch: {
			intent: function(value) {
				if (value == "toComment"){
					var addCommentBox = document.getElementsByClassName("addCommentBox")[0];
					addCommentBox.classList.remove('start');
					addCommentBox.classList.add('end');
				}
			}
		},
		computed:{

			sortedCategoriesList(){
				var sortedCategories = this._sortCategoryList(this.categories);
				return sortedCategories;
			},
		
			chosenOptionName(){
				for (var i =0; i < this.poll.options.length; i++){
					if (this.poll.options[i].id == this.chosenOption){
						return this.poll.options[i].option;
					}
				}

			},

			
			totalVotes(){
				return this.poll.totalVotes;
			},


			calculatedScores(){
				if(this.poll.totalVotes ==0){
					return this.poll.options.map(a=>{
						a.percent = '0%'
						return a
					})
				}

				
				return this.poll.options.filter(a=>{
                    if (!isNaN(a.score) && a.score > 0){
                        a.percent = ( Math.round( (parseInt(a.score)/this.poll.totalVotes ) * 100) ) + '%'
					}
					else{
                        a.percent =  '0%'
					}
                    return a
                })
			},

			sortedComments(){
				if (this.activeTab != '*'){
					return this.comments.filter(a=> a.optionId == this.activeTab);
				
				}

				//when active tab is "All"
				return this.comments;

			},

			userHasVoted(){
				return this.poll.userHasVoted;
			},

			contextImageHeight(){
				var contextImage =	document.getElementById('opinionContextImage');
				var width = contextImage.style.width;
				
				contextImage.style.height = width;
			},


			totalVotes(){
				return this.poll.totalVotes;
			},

			activityIsAlreadyLiked(){
				
				return this.poll.userHasLiked;
			},

			numOfLikes(){
				return this.poll.numOfLikes;
			},
			openUserProfile() {
     	 		window.open("" + "/profile/" + this.poll.userId + "/" + this.poll.userSlug, "_self");
			},

		},

        created(){
            var vm = this;
			this.loading =true;
			
			var idOfPollToBeViewed = document.getElementById('idOfPollToBeViewed').innerHTML;
			idOfPollToBeViewed = parseInt(idOfPollToBeViewed);
            axios.get("" + '/poll/' + idOfPollToBeViewed)
			
            .then(function(response){
				vm.user_logged_in = response.data.userLoggedIn;
                vm.changePollData('id', response.data.id);
				vm.changePollData('question', response.data.question);
                vm.changePollData('userName', response.data.userName);
				vm.changePollData('userId',response.data.userId);
				vm.changePollData('type', response.data.type);
                vm.changePollData('userPic', response.data.userPic);
                vm.changePollData('info', response.data.info);
				vm.changePollData('imageInfo', response.data.imageInfo);
				vm.changePollData('totalVotes', response.data.totalVotes);
				vm.changePollData('slug', response.data.slug);
				vm.changePollData('isPicturePoll', response.data.isPicturePoll);
				vm.changePollData('hasUrlInfo', response.data.hasUrlInfo);
				vm.changePollData('infoPageThumb', response.data.infoPageThumb);
				vm.changePollData('infoPageTitle', response.data.infoPageTitle);
				vm.changePollData('infoPageDescription', response.data.infoPageDescription);
				vm.changePollData('numOfLikes', response.data.numOfLikes);
				vm.changePollData('options', response.data.options);
				vm.changePollData('userHasLiked', response.data.userHasLiked);
                vm.changePollData('userHasVoted', response.data.userHasVoted);
                vm.changePollData('hasEnded', response.data.hasEnded);
				vm.changePollData('imageInfo', response.data.imageInfo);
				vm.changePollData('timeAdded', response.data.timeAdded);
				vm.changePollData('timeRemaining', response.data.timeRemaining);
				vm.changePollData('seenPollResults', response.data.userHasSeenResults);


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


			axios.get('/comments/' + idOfPollToBeViewed,{

			}).then(function(response){
				vm.comments = response.data.comments;
			});

			axios.get("" + '/categories').then(response => {
				this.categories = response.data.categories;
			});
        },
    }

</script>

<style scoped>

.addCommentBox {
	animation-name: slide-down;
	animation-duration: 2s;
	animation-timing-function: ease-out;
}



@keyframes slide-down {
	0% {  -webkit-transform: translateY(-1%); }   
    100% {  -webkit-transform: translateY(0); }
}
@-webkit-keyframes slide-down {
      0% { -webkit-transform: translateY(-1%); }   
    100% { -webkit-transform: translateY(0); }
}
@-moz-keyframes slide-down {
      0% {  -webkit-transform: translateY(-1%); }   
    100% {  -webkit-transform: translateY(0); }
}
</style>


