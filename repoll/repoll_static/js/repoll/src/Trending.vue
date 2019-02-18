<template>
	<div class="body-container">
		<div class="tab-container">
			<div class="tab polls">
				<p>Poll</p>
			</div>
			<div class="tab opinions">
				<p>Opinions</p> 
			</div>
			<div class="tab comments">
				<p>Comments</p>
			</div> 
		</div>
		<div class="content-container">
			<div class=""></div>
		</div>

		<h1>thjis is soo good</h1>
	</div>
    
</template>


<script>
import axios from 'axios';
import AddComment from './home-components/AddComment.vue'; 
import AuthenticationModal from './home-components/AuthenticationModal.vue';
import Comments from './home-components/Comments.vue';
import FeedItem from './home-components/FeedItem.vue';
import NewOpinion from './home-components/NewOpinion.vue';
import NewPoll from './home-components/NewPoll.vue'; 
import Reply from './home-components/Reply.vue';
import Sidebar from './home-components/Sidebar.vue'; 

	var changeButtonContent = function(button, text){
		button.innerHTML = text;
	}
	var siteUrl = 'http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com:6543';
	

export default {
    name: "Trending",
   
	delimiters: ['((','))'],
	components: { 
      'sidebar': Sidebar, 
      'reply': Reply, 
      'feed-item': FeedItem, 
      'new-opinion-modal': NewOpinion, 
      'add-new-comment-modal': AddComment, 
       'comments': Comments, 
    },

		data(){
			return{
				loading: true,
				loadingMoreContent: false,
				locations: true,
				sidebarContentSelectedClass: 'sidebar-content-selected',

				activities: [],
				categories: [],
				subscriptions: [],

				userLoggedIn: false,
				userName: '',
				userPic: '',

				optionToCommentOn: 0,
				activityToReplyTo: {},
				activityToCommentOn: {},

				showRespondentsModal: false,
				showNewSelectionModal: false,
				showAuthenticationModal: false,
				showReplyModal: false,
				showCommentModal: false,
				showSidebar: false,
				showCategories: false,
				showViewCommentsModal: false,
				showCreateNewPollModal: false,
				showSubscriptions:false,
				showCreateNewOpinionModal: false,
				activityToGetRespondents: {},
				activityToVoteOn: {},
				

			}
		},

		computed:{
			sortedSubscriptionsList(){
				var sortedSubscriptions = this._sortCategoryList(this.subscriptions);
				return sortedSubscriptions;
			},

			sortedCategoriesList(){
				var sortedCategories = this._sortCategoryList(this.categories);
				return sortedCategories;
			},
		},

		methods:{
			openPollsVotedIn: function(){
				window.open("" + '/polls_voted_in/', '_self');

			},

			openProfile: function(){
				window.open("" + '/profile/{{user.id}}/{{user.slug}}', '_self');
			},
			_sortCategoryList(list){
				list.sort(function(a, b){
					if (a.categoryName < b.categoryName) return -1;
					if (a.categoryName > b.categoryName) return 1;
				})
				return list;
			},

			mShowNewSelectionModal(){
				this.showNewSelectionModal = true; 
			},

		

			showNewPollModal(){
				this.showCreateNewPollModal = true;
			},
			showNewOpinionModal(){
				this.showCreateNewOpinionModal = true;
			},
			showViewComments(value){
				this.showViewCommentsModal = true;
			},
			
			toggleSubscriptions(){
			},

			toggleShowCategories(){
				this.showCategories = !this.showCategories;
			},
			toggleAuthModal(){
				this.showAuthenticationModal = !this.show_auth_modal;
			},

			closeAddCommentModal(newData){
				this.showCommentModal = newData;
			},


			closeModal(newData){
					this.showCommentModal = false;
				
				
					this.showAuthenticationModal = false;
								this.showSidebar = false;
				

				this.showCommentModal == false;
				
				this.showCreateNewOpinionModal = false;
				this.showCreateNewPollModal = false;
				this.showReplyModal = false;
				
			},

			setActivityCommentDetails(activity){
				this.activityToCommentOn = activity;
			},

			setReplyActivityDetails(activity){
				this.activityToReplyTo = activity;
				this.showReplyModal = true;
			},

			setActivityRespondentDetails(activity){
				this.activityToGetRespondents = activity;
				this.showRespModal();
			},

			setOptionCommentDetails(optionId){
				this.optionToCommentOn = optionId;
			},

			showCommModal(newData){
				this.showCommentModal = true;
			},

			showAuthModal(newData){
				this.showAuthenticationModal = newData;
			},
			
			showRespModal(){
				this.showRespondentsModal = true;
			},

			subscribeToCategory(categoryId){
				var category = this.categories.filter(c=> c.categoryId==categoryId);
				var category = category[0]; //because the above returns a list of one object;
				var categoryIndex = this.categories.indexOf(category); //we need the index of the category so we can remove it from list of categories

				this.subscriptions.push(category);
				this.categories.splice(categoryIndex, 1);
			},

			unsubscribeFromCategory(categoryId){
				var category = this.subscriptions.filter(c=> c.categoryId==categoryId);
				var category = category[0]; //because the above returns a list of one object;
				var categoryIndex = this.subscriptions.indexOf(category); //we need the index of the category so we can remove it from list of categories

				this.subscriptions.splice(categoryIndex, 1);
				this.categories.push(category);
			},

			goToCategoryPage(categoryId){
				window.open("" + '/polls/category_id=' + categoryId);
			},

			addToActivitiesList(activityObject){
				this.activities.unshift(activityObject);
			},

			changeActivityData(activity, key, value){
				this.$set(activity, key, value);
			},

			changeActivityJustVoted(activityDetailsList){
				var activityId = activityDetailsList[0];
				var optionId = activityDetailsList[1];
				var type = activityDetailsList[2];

				var vm = this;
				var activityInstances = this.activities.filter(a=>a.id==activityId &&a.type==type);
				activityInstances.forEach(function(activity){
					activity.totalVotes += 1;
					vm.$set(activity, 'userHasVoted', true);

					activity.options.forEach(function(option){
						if (option.id == optionId){
							option.score += 1;
						}
					});
				});
                
			},

			 getDocHeight() {
    var D = document;
    return Math.max(
        D.body.scrollHeight, D.documentElement.scrollHeight,
        D.body.offsetHeight, D.documentElement.offsetHeight,
        D.body.clientHeight, D.documentElement.clientHeight
    );
},

		},
		

	


		//this is what happens when you load the page.
		//automaticall
		created(){
			var vm = this;

			axios.get("" + '/get_trending').then(response => {
			//this will give a list of polls
			var response_list = response.data.activities;
			this.activities = response_list;
			this.userName = response.data.userName;
			this.userPic = response.data.userPic;
			this.userLoggedIn = response.data.user_logged_in; 
			this.loading =false;
			

			
			});

			//get categories data
			axios.get("" + '/categories').then(response => {
				this.categories = response.data.categories;
			});

			axios.get("" + '/show_subscriptions').then(response => {
				this.subscriptions = response.data.subscriptions;
			});
	

			window.onscroll = () => {
				/**
				var loader = document.getElementById('loadingMoreContent');
				var scrollTop = window.pageYOffset || (document.documentElement || document.body.parentNode || document.body).scrollTop;
				var winheight = window.innerHeight || (document.documentElement || document.body).clientHeight;
				var docHeight = this.getDocHeight();
				var trackLength = docHeight - winheight;
				var pctScrolled = Math.floor(scrollTop/trackLength * 100); // gets percentage scrolled (ie: 80 or NaN if tracklength == 0)
				this.loadingMoreContent = true;

				if (pctScrolled == 98){
					axios.get(siteUrl + '/get/latest').then(response=>{
						response.data.activities.forEach(activity=>{
							this.activities.push(activity);
						});
					});
					console.log(pctScrolled);
				}
				**/
			}
		}
}
</script>

<style scoped>
	.container {
		background-color: white; 
	}
	.tab-container {
		display: flex; 
		justify-content: space-between;
		align-items: center;
	}
	.tab {
		color: teal;
		padding: 10px;
	}

</style>
