<template>
    <div id="sub-container">


	<feed-item v-for="activity in activities" 
			:activity='activity'
			:user_logged_in='userLoggedIn'
			:show_comment_modal='showCommentModal'
			@act_close_comment_modal='closeModal'
			@act_show_comment_modal='showCommModal'
			@set_activity_comment_details='setActivityCommentDetails'
			@set_option_comment_details='setOptionCommentDetails'
			@show_auth_modal="showAuthModal"
			@act_show_view_comments_modal='showViewComments'
			@act_show_voters_modal='mShowUsersModal'
			@change_activity_to_refer_to='changeActivityToReferTo'
			:key="'index' + activities.indexOf(activity) + '-' + activity.id"
			@set_activity_respondent_details='setActivityRespondentDetails'
			@set_reply_activity_details='setReplyActivityDetails'>	
		</feed-item>


		<add-new-comment-modal 
		:show_comment_modal='showCommentModal' 
		:activity='activityToCommentOn'
		@close_add_coment_modal='closeModal'
		:option='optionToCommentOn'
		@activity_voted='changeActivityJustVoted'>
		</add-new-comment-modal>
	

	
	</div>
	

</template>


<script>
import axios from 'axios';
import FeedItem from './home-components/FeedItem.vue';
import AddComment from './home-components/AddComment';

    var showSnackbar = function(text){
		var snackbar = document.getElementById('snackbar');
		snackbar.innerHTML = text;

    	snackbar.className = "show";

    // After 3 seconds, remove the show class from DIV
    	setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 4000);

	}
var siteUrl = "";
	


export default {
    name: "OpinionsVotedIn",
   
	delimiters: ['((','))'],
	components: { 
	  'feed-item': FeedItem,
	  'add-new-comment-modal': AddComment, 
    },
		data(){
			return{
				activities: [],
				activity_to_refer: {},
				loading: true,
				loadingMoreContent: false,
				loadingMoreContentFailed: false,
				locations: true,
				sidebarContentSelectedClass: 'sidebar-content-selected',

				notifications: [],
				categories: [],
				noOfNewNotifications: 0,

				userLoggedIn: false,
				userName: '',
				userPic: '',

				optionToCommentOn: 0,
				activityToReplyTo: {},
				activityToCommentOn: {},

				usersModalUrlToLoad: '',
				
				showUsersModal: false, 
				showNotificationModal: false, 
				showRespondentsModal: false,
				showNewSelectionModal: false,
				showAuthenticationModal: false,
				showReplyModal: false,
				showCommentModal: false,
				showSidebar: false,
				showCategories: false,
				showViewCommentsModal: false,
				showCreateNewPollModal: false,
				showCreateNewOpinionModal: false,
				activityToGetRespondents: {},
				activityToVoteOn: {},
				
			}
		},

		computed:{

		},

		methods:{
            changeUserData(id, value){
                this.$set(this.user, id, value);
            },

			openSidebar(){
				this.showSidebar = true;
			},

			changeActivityToReferTo(activity){
				this.activity_to_refer = activity;
			},

			loadMoreContent: function(){
				axios.get("" + '/get/latest').then(response=>{
					response.data.activities.forEach(activity=>{
						this.activities.push(activity);
					});
					}).catch(error=>{
						this.loadingMoreContentFailed = true;
					});
			},

			goToNotificationsPage: function(){
				window.open("" +  '/notifications', '_self');
				return ;
			},

			getNoOfNewNotifications: function(){
				var vm = this;
				axios.get("" + '/notifs/' + userId).then(response=>{
					vm.noOfNewNotifications = response.data.unseen;
				});
			},

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

			getNotifications(){
				var vm = this;
				axios.get("" + '/notifs/' + userId).then(response=>{
					vm.notifications.push(response.data.notifs);
				});
			},

			mShowNewSelectionModal(){
				this.showNewSelectionModal = true; 
			},
		
			mShowUsersModal(urlToLoad){
				this.showUsersModal =  true;
				this.usersModalUrlToLoad = urlToLoad;
			},

			showNewPollModal(){
				if (!this.userLoggedIn){
					this.showAuthenticationModal = true;
					return;
				}
				this.showCreateNewPollModal = true;
			},
			showNewOpinionModal(){
				if (this.userLoggedIn == false){
					this.showAuthenticationModal = true; 
					return ;
				}
				this.showCreateNewOpinionModal = true;
			},
			showViewComments(value){
				this.showViewCommentsModal = true;
			},
			

			toggleShowCategories(){
				this.showCategories = !this.showCategories;
			},
			toggleAuthModal(intent){

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
			axios.get("" + '/get_opinions_voted_in').then(response => {
			//this will give a list of polls
			var response_list = response.data.activities;
			this.activities = response_list;

			

			
			});

			//get categories data



		},

}
</script>
