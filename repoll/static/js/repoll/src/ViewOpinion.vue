<template>
    <div class="body-container">
    	<div>
        	<div class="feed-container">
				<div class="feed-card">

					<div class="avatar-and-details" @click="openUserProfile">
						<div class="avatar">
							<img v-if="poll.userPic == null" src="https://www.w3schools.com/howto/img_avatar.png">
							<img v-if="poll.userPic != null" :src="poll.userPic">                    
						</div>

						<div class="details">
							<p class="name">{{poll.userName}}</p>
							<div class="flex">
								<p class="username">{{poll.username}}</p>
								<p class="">&middot;</p>
								<p class="time-added">{{poll.timeAdded}}</p>
							</div>
						</div>
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
			
			<!--This div will be shown for poll activities --> 
			</div>

		</div>
		<div class='addCommentBox' v-show="intent == 'toComment' && !poll.userHasVoted">
			<form id='comment-form'>
				<p class='chosenOption'>{{chosenOptionName}}</p>
				<textarea type="text" placeholder='Reason' @click="autoResize" name='comment'></textarea>
				<button @click='comment'>Comment</button>
			</form>
		</div>

		<div class="other-details">
            <div class="tab-header">
                <div class="tab all" style="border-bottom: 3px solid teal;"
				id='*'
				@click='makeTabActive("*")'
				:class="[isActiveTab('*') ? isActiveClass : '']">
                    <p>All</p>
                </div>

                <div class="tab" v-for='option in poll.options'
					 :option='option'
					 :id='option.id'
					 :key="option.id"
					 @click='makeTabActive(option.id)'>
                    <p>{{option.option}}</p>
                </div>
            </div>

            <!--COMMENT COMPONENT-->
			<comment v-for='comment in sortedComments'
				:origin="'opinion'"
				:key="comment.id"
				@change_can_agree_state='changeCanAgreeWithCommentsState' 
				:comment='comment' 
				:can_agree_to_comments='canAgreeToComments'
				:user_logged_in="userLoggedIn"
				@act_show_auth_modal="mShowAuthenticationModal"	></comment>
			
		</div>

		<!-- AUTHENTICATION COMPONENT -->
		<!-- eventually, I'll need to make authentication modal to load categories by itself -->
		<authentication-modal
          :activity_to_refer="poll"
          :categories="_sortCategoryList"
          :show_authentication_modal="showAuthenticationModal"
          @close_auth_modal="closeModal"
        ></authentication-modal>
	</div>
	
</template>


<script>
var siteUrl = "";
	const activityPOSTURL = "";

    import axios from 'axios';
	import Comment from './home-components/Comment.vue'
	import AuthenticationModal from './home-components/AuthenticationModal.vue'

    export default {
        name: 'ViewOpinion', 
        components: {
				'comment': Comment,
			'authentication-modal': AuthenticationModal,
        },
		
        data(){
			return{
            	some: 'deji',
				loading: true,
				userLoggedIn: null,
				categories: [],
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
				showAuthenticationModal: false,
			}
             
		},
		
		watch: {
			// if authentication modal is shown
			showAuthenticationModal: function(newValue) {
				if (newValue == true) {
					//load list of categories to subscribe to.
					this.loadCategories();
					
				}
			}
		},

		computed: {
			sortedCategoriesList() {
      			var sortedCategories = this._sortCategoryList(this.categories);
      			return sortedCategories;
			},

		},

        methods:{
			_sortCategoryList(list) {
				list.sort(function(a, b) {
					if (a.categoryName < b.categoryName) return -1;
					if (a.categoryName > b.categoryName) return 1;
				});
				return list;
			},

			//only authentication modal for now
			closeModal(){
				this.showAuthenticationModal = false;
			},

			//shows authentication modal, "m" means method.
			mShowAuthenticationModal(){
				this.showAuthenticationModal = true;
			},

			//opens the User Profile, as name implies
			openUserProfile() {
     	 		window.open("" + "/profile/" + this.poll.userId + "/" + this.poll.userSlug, "_self");
			},

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
			loadCategories(){
				// a recursion to make sure we get categories at all cost

				//base case
				if (this.categories.length == 0){
					axios.get("" + "/categories").then(response => {
						this.categories = response.data.categories;
					}).then(response=> {
						//return
						return 0;
					}).catch(error=>{
						//start recursion
						this.loadCategories();
					});
				}
				else {
					return 0; // return nothing
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
				if (this.userLoggedIn == false){
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
				if (this.userLoggedIn == false){
					this.showAuthenticationModal = true;
					return 0;
				}

				// if user is the creator of the opinion or has already voted
				else if (this.poll.userHasVoted == true){
					alert("You can't vote in this opinion anymore");
				}
				// else, if user has not voted or is not not the creator of the poll
				else {
					this.chosenOptionName = optionName;
					this.intent = 'toComment';

					//look for the id of the option that has the option name;
					var optionWithName = this.poll.options.filter(o=> o.option == optionName);
					//make it the id of the option the chosen option
					this.chosenOption = optionWithName[0].id;
				}
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
				vm.changePollData('username', response.data.username);
				vm.changePollData('timeAdded', response.data.timeAdded);
                vm.changePollData('type', response.data.type);
                vm.changePollData('id', response.data.id);
				vm.changePollData('userPic', response.data.userPic);
				vm.changePollData('userSlug', response.data.userSlug);
				vm.changePollData('userId', response.data.userId);
                vm.changePollData('totalVotes', response.data.numOfVotes);
				vm.changePollData('numOfShares', response.data.numOfShares);
				vm.changePollData('numOfLikes', response.data.numOfLikes);
                vm.changePollData('options', response.data.options);
                vm.changePollData('userHasVoted', response.data.userHasVoted);
				vm.changePollData('imageInfo', response.data.imageInfo);
				vm.changePollData('timeAdded', response.data.timeAdded);
				vm.changePollData('userIsFollowing', response.data.userIsFollowing);
				vm.changePollData('contextImage', response.data.contextImage);

				// is user logged in?
				vm.userLoggedIn = response.data.userLoggedIn;

				// should users be allowed to agree to a comment?
				// it all starts from knowing whether they have voted before.
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


			axios.get('/comments/opinion/' + idOfPollToBeViewed,{

			}).then(function(response){
				vm.comments = response.data.comments;
			})
        },

    }


</script>

<style>
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

	.modal-container .modal-body{
		position: relative;
		padding-bottom: 20px;
	}

	.modal-container .modal-body .final-input{
		margin-bottom: 30px;
	}
	.modal-container .modal-body button{
		position: absolute;
		right: 0; 
		bottom: 0;
		margin-right: 20px; 
	}
	.third-stage {
		display: flex;
		flex-direction: column;
	}

	.final-stage {
		align-items: center;
		justify-content: center;
	}

	.final-stage button{
		position: relative; 
		margin-right: 0;
	}
	.proceed-container {
		display: flex;
		flex-direction: column;
		justify-self: flex-end;
	}
	.proceed-container button {
		align-self: flex-end;
		position: relative;
	}

</style>
