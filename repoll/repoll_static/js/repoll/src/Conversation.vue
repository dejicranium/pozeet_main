<template>    
    <div id="body-container">
    	<div class=''>
			<div class='feed-container'>
				<div class="feed-card">
					<div class="avatar-and-details">
						<div class="avatar">
							<img v-if="comment.userPic == null" src="https://www.w3schools.com/howto/img_avatar.png">
							<img v-if="comment.userPic != null" :src="comment.userPic">                    
						</div>

						<div class="details">
							<p class="name">{{comment.userName}}</p>
							<div class="flex">
								<p class="username">{{comment.username}}</p>
								<p class="">&middot;</p>
								<p class="time-added">{{comment.timeAdded}}</p>
							</div>
						</div>
					</div>    			

                    <h2 class="chosen-option">{{comment.optionChosen}}</h2>
                    <p class="comment" style='white-space:;'>{{comment.comment}}</p>


                    <div>
                        <div class="comment-question quote" v-if='comment.poll' tab-index="0" @click="openPoll">
                            <p class='author-name' style='font-weight:normal; color:teal;'>Poll</p>
							<div>
								<p class='author-name' style='font-size:bold; margin-right:5px; display:inline;'>{{comment.poll.userName}}</p>
								<p style="color:lightgray; font-weight:normal; display: inline; margin-right:5px;">({{comment.poll.username}})</p>
								<p style="color:lightgray; font-weight:normal; display: inline; margin-right:5px;">{{comment.poll.timeAdded}}</p>
							</div>							
							<p class='question'>{{comment.poll.question}}</p>


                        </div>
                            
							
						<div class="comment-question quote" v-else-if='comment.opinion' tab-index="0" @click="openOpinion">
                            <p class='author-name' style='font-weight:normal; color:teal;'>Opinion</p>
							<div>
								<p class='author-name' style='font-size:bold; margin-right:5px; display:inline;'>{{comment.opinion.userName}}</p>
								<p style="color:lightgray; font-weight:normal; display: inline; margin-right:5px;">({{comment.opinion.username}})</p>
								<p style="color:lightgray; font-weight:normal; display: inline; margin-right:5px;">{{comment.opinion.timeAdded}}</p>
							</div>
							<p class='question'>{{comment.opinion.opinion}}</p>

                        </div>

                    </div>

					<button @click='reply'> <i class="fas fa-reply button-icon"></i>Reply </button>
					<!-- <button><i class="far fa-thumbs-up button-icon"></i>Like</button> -->
						<!--<button @click="share"><i class="far fa-share-square button-icon"></i>Share</button> -->

				</div>

            </div>

			<div class='addCommentBox' v-show="intent == 'toReply'">
				<form id='comment-form'>
					<textarea type="text" placeholder='Reply' v-model='replyText' @click="autoResize" name='reply' id='comment-form'></textarea>
					<button @click='replyComment'>reply</button>
				</form>
			</div>

			<div class='other-details'>
				<div id='innerReply'>
					<comment v-for='reply in replies' :reply='reply' :key='reply.id'>
					</comment>

				</div>
			</div>
		</div>



	<div id='snackbar'></div>
</div>




</template>

<script>
	import axios from 'axios';
    import ConvoComment from './view-converstation-components/ConvoComment.vue';

	var siteUrl = "";
	const activityPOSTURL = "";
	var conversationId = document.getElementById('conversation-id-signifier').innerHTML; 
	var replyId = document.getElementById('reply-id-signifier').innerHTML;	
	

export default {
    name: 'Conversation',
    components: {'comment': ConvoComment},
        data(){
			return{
				some: 'deji',
				comment: {}, //it'a list because we want it to be reactive.
				chosenOption: 0,
				user_logged_in: false,
				comments: [],
				replies: [], 
				replyText: '',
				activeTab: '*',
				tabs: [],
				isActiveClass: 'isActive',
				intent: '',
				canAgreeToComments: false, //this will make us know whether user can press agree on another comment
				commentToAgreeWith: 0, 
			}
             
        },


        methods:{
			openPoll(){
				window.open('/poll/' + this.comment.poll.id +'/', '_self');
			},
			openOpinion(){
				window.open('/opinion/' + this.comment.opinion.id + '/', '_self');
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

            changeCommentData(id, value){
                this.$set(this.comment, id, value);
            },


			reply(){
				if (this.user_logged_in == false){
					return 0;
					
				}

				if (this.intent == 'toReply'){
					this.intent = '';
				}
				else{
					this.intent = 'toReply';
				}

			},

			replyComment(event){
				event.preventDefault();
				var replyButton = event.target;
				replyButton.disabled = true;
				var vm = this;
				axios.post(activityPOSTURL + '/reply-comment', {
					comment_id: vm.comment.id, 
					reply: vm.replyText,
				}).then(response=>{
					replyButton.disabled = false;
					vm.replyText = '';
					showSnackbar('Reply Added!');
					vm.intent = '';
					window.location.reload();
				}).catch(error=>{
					replyButton.disabled = false;
				});

			},	

			flattenReplyReplies(reply){
				this.replies.unshift(reply);

				if (reply.replies){
					reply.replies.forEach(r=>{
						this.flattenReplyReplies(r);
					});
				}

				else{
					return 0;
				}
			},


		},

        mounted(){
            var vm = this;
            axios.get("" + '/get_conversation/'+conversationId+'/'+replyId+'/')
			.then(response=>{
				vm.user_logged_in = response.data.user_logged_in;
				vm.changeCommentData('optionChosen', response.data.comment.optionChosen);
                vm.changeCommentData('userName', response.data.comment.commenter);
				vm.changeCommentData('comment', response.data.comment.comment);
                vm.changeCommentData('type', response.data.comment.type);
                vm.changeCommentData('id', response.data.comment.id);
                vm.changeCommentData('userPic', response.data.comment.userPic);
				vm.changeCommentData('numOfShares', response.data.comment.numOfShares);
                vm.changeCommentData('numOfAgrees', response.data.comment.numOfAgrees);
                vm.changeCommentData('hasSharedComment', response.data.comment.hasSharedComment);
				vm.changeCommentData('timeAdded', response.data.comment.timeAdded);
				vm.changeCommentData('userIsFollowing', response.data.comment.userIsFollowing);
				vm.changeCommentData('poll', response.data.comment.poll);
				vm.changeCommentData('opinion', response.data.comment.opinion);

				var replies = response.data.replies;

				replies.forEach(reply=>{
					if(reply.id == parseInt(replyId)){
						reply['toView'] = true;
					}

					vm.flattenReplyReplies(reply);
				});
				vm.loading = false;

				//should users be allowed to agree to a comment?
				//it all starts from knowing whether they have voted before.
				
            }).catch(function(error){
				vm.loading = false;
			    }
            
            );


        },
    
}
</script>

<style scoped>
	#body-container {
		padding-top: 50px;
	}

</style>
