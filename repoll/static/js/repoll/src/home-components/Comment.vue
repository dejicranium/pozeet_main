	<template id='comment-template'>
  <div>
  <div class="comment-card">
    <div class="avatar">
      <img v-if="comment.userPic == null" src="https://www.w3schools.com/howto/img_avatar.png">
      <img v-else :src="comment.userPic">
    </div>

    <div class="beside-avatar-box">
      <div class="author-details">
        <h3 class="name" style="font-weight:bold">{{comment.userName}}</h3>
        <p class="name" style="color:lightgray">{{comment.timeAdded}}</p>
      </div>

      <div class="chosen-option">
        <h4 class="option">{{comment.option}}</h4>
      </div>

      <div class="reason" id>
        <p class="comment">{{comment.comment}}</p>
      </div>

      <button v-if="!showCommentReplies && comment.numOfReplies > 0" style="font-size:13px; color:teal; background-color:transparent;border:0;" @click="getCommentReplies">Show Replies</button>
      <button v-if="showCommentReplies" style="font-size:13px; color:teal; background-color:transparent;border:0;" @click="getCommentReplies">Hide Replies</button>

      <div class="action-buttons">
	<!-- you can only agree if you've not carried out an action on the opinion or poll-->
        <button v-if="can_agree_to_comments" @click="agree">Agree</button>

	<!-- shows the number of agrees on a comment -->
        <button v-else style="background-color:transparent;">
          <span style="color:black; font-weight:bold;">{{comment.numOfAgrees}} agrees</span>
        </button>
	
	<!---
        <button @click="share" v-bind:class="sharedOrNotClass">
          Share
          <span v-if="hasSharedComment">{{numOfShares}}</span>
        </button>
	-->

        <!-- reply button for opinion comments -->
        <button v-if="origin == 'opinion'" @click="addReply"> Reply</button>
      </div>
    </div>
  </div>
      <div class="addReplyReplyBox" v-show="intent=='toReplyComment'">
      <form id="comment-form">
        <textarea
          type="text"
          v-model="replyText"
          placeholder="Reply"
          @click="autoResize"
          name="reply"
          id="comment-form"
        ></textarea>
        <button type="button" @click="reply">Reply</button>
      </form>
    </div>

    <div style="padding-left: 20px;">
        <convo-comment v-show="showCommentReplies"  v-for="reply in commentReplies" :key="reply.id" :reply="reply"></convo-comment>
      </div>

</div>
</template>


<script>
import axios from "axios";
var siteUrl = "";
const activityPOSTURL = "";
import ConvoComment from '../view-converstation-components/ConvoComment.vue';

export default {
  name: "Comment",
  props: ["comment", "can_agree_to_comments", "origin", 'user_logged_in'],
  components: {
    'convo-comment': ConvoComment,
  },
  
  data() {
    return {
      canAgreeToComments: this.can_agree_to_comments,
      replies: this.comment.replies,
      numOfAgrees: this.comment.numOfAgrees,
      replyText: '',
      intent: '',
      showCommentReplies: false, 
      commentReplies: [],

    };
  },

  computed: {
    sharedOrNotClass() {
      if (this.hasSharedComment) {
        return "hasShared";
      }
      return "";
    },
    hasSharedComment: {
      get: function() {
        return this.comment.hasSharedComment;
      },
      set: function(newValue) {
        this.comment.hasSharedComment = newValue;
      }
    },
    numOfShares: {
        get: function() {
          return this.comment.numOfShares;
        },

          set: function(newValue) {
            this.comment.numOfShares = newValue;
          }
      }
  },

  methods: {
		changeShareStateTo(boolean) {
			this.comment.hasSharedComment = boolean;
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
		flattenReplyReplies(reply) {
			this.commentReplies.push(reply);
		},

		getCommentReplies(){
			var vm = this;
			var button = event.target;
			button.disabled = true;
			if (this.commentReplies.length == 0) {
				axios.get("" + "/replies/comment_id=" + this.comment.comment_id).then(response => {
					var replies = response.data.replies;

					replies.forEach(reply => {
					this.flattenReplyReplies(reply);
					button.disabled = false;

					}).catch(error => {
						button.disabled = false;
					});
				});
			} 
			else {
			
			}     
		},
		showAuthenticationModal(){
			this.$emit('act_show_auth_modal', true);
		},

		shareComment() {
			var vm = this;
			if (this.user_logged_in == false){
				this.showAuthenticationModal();
				return 0;
			}
			if (this.hasSharedComment == false) {
				vm.changeShareStateTo(true);
				axios
				.post(activityPOSTURL + "/share", {
					comment_id: vm.comment.id
				})
				.then(response => {
					vm.numOfShares += 1;
				})
				.catch(error => {
					vm.changeShareStateTo(false);
				});
			}
		},
		addReply(){
			if (this.user_logged_in == false){
				this.showAuthenticationModal();
				return 0;
			}
			this.intent = "toReplyComment";
		},
		unshareComment() {
			var vm = this;
			if (this.hasSharedComment == true) {
				vm.changeShareStateTo(false);
				vm.numOfShares += 1;
				axios
				.post(activityPOSTURL + "/delete_share", {
					comment_id: vm.comment.id
				})
				.then(response => {
					vm.numOfShares -= 1;
				})
				.catch(error => {
					vm.numOfShares -= 1;
					vm.changeShareStateTo(true);
				});
			}
		},

    	reply(event){
        	var vm = this;
			var replyButton = event.target;
			replyButton.disabled = true;
			var vm = this;

			replyButton.innerText = "...";
			axios.post(activityPOSTURL + '/reply-comment', {
				comment_id: this.comment.comment_id, 
				reply: this.replyText,
					
			}).then(response=>{
				vm.changeButtonContent(replyButton, "Reply");	
				replyButton.disabled = false;
				vm.closeModal();
				vm.replyText = '';
				vm.showSnackbar('Reply Added!');
			
			}).catch(error=>{
				vm.changeButtonContent(replyButton, "Reply");
				replyButton.disabled = false;
				vm.showSnackbar('Error Adding Reply');


			});
		},
		
		share() {
			if (this.user_logged_in == false){
				this.showAuthenticationModal();
				return 0;
			}			
			if (this.hasSharedComment) {
				this.unshareComment();
			} else {
				this.shareComment();
			}
    	},
 
		agree() {
			var vm = this;
			if (this.user_logged_in == false){
				this.showAuthenticationModal();
				return 0;
			}			
			//if origin of comment is a poll
			if (this.origin == "poll") {
				axios.post("" + "/agree", {
					comment_id: this.comment.id,
					option_id: this.comment.optionId,
					poll_id: this.comment.poll_id,
				}).then(function(response) {
					vm.numOfAgrees += 1;
					vm.setCannotAgree();
				}).catch(function(response) {

				});
			}
			else {	// if it is an opinion
				axios.post("" + "/agree", {
					comment_id: this.comment.id,
					option_id: this.comment.optionId,
					opinion_id: this.comment.opinion.id,
				}).then(function(response) {
					vm.numOfAgrees += 1;
					vm.setCannotAgree();
				}).catch(function(response) {

				});        
			}
		
		},

		setCannotAgree() {
			var option_voted_for = this.comment.optionId;

			// you can check change_can_agree_state in either ViewPoll.vue or ViewOpinion.vue
			vm.$emit("change_can_agree_state", option_voted_for);
    	}
		
    },




  };

</script>

<style scoped>
.comment {
  box-sizing: border-box;
  word-wrap: break-word;
  padding-bottom: 2px;
  width: 100%;
  border-radius: 0;
  white-space: pre-wrap;
  text-overflow: ellipsis;
  overflow: hidden;
  max-height: 120px;
}

.chosen-option .option {
  font-size: 12px;
}

.author-details .name {
  font-size: 12px;
}
#hasShared {
  color: teal;
  background-color: white;
}
#innerReply {
  margin-top: 5px;
}

#comment-form {
  display: flex;
  flex-direction: column; 
  -ms-flex-direction: column;
}

#comment-form button {
  align-self: flex-end;
}
.comment {
  box-sizing: border-box;
  word-wrap: break-word;
  padding-bottom: 2px;
  width: 100%;
  border-radius: 0;
  white-space: pre-wrap;
  text-overflow: ellipsis;
  overflow: hidden;
  max-height: 120px;
}
</style>

