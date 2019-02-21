	<template id='comment-template'>
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

      <div class="action-buttons">
        <button v-if="can_agree_to_comments" @click="agree">
          Agree
          <span>{{numOfAgrees}}</span>
        </button>
        <button v-else style="background-color:transparent;">
          <span style="color:black; font-weight:bold;">{{comment.numOfAgrees}} Agrees</span>
        </button>
        
        <button @click="share" v-bind:class="sharedOrNotClass">
          Share
          <span v-if="hasSharedComment">{{numOfShares}}</span>
        </button>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
var siteUrl = "";
const activityPOSTURL = "";

export default {
  name: "Comment",
  props: ["comment", "can_agree_to_comments"],

  data() {
    return {
      canAgreeToComments: this.can_agree_to_comments,
      replies: this.comment.replies,
      numOfAgrees: this.comment.numOfAgrees
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
    shareComment() {
      var vm = this;
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

				if (this.activity.type == 'comment'){
					axios.post(activityPOSTURL + '/reply-comment', {
						comment_id: this.activity.id, 
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
        }
    },

    share() {
      if (this.hasSharedComment) {
        this.unshareComment();
      } else {
        this.shareComment();
      }
    },
    /**
    share() {
      var vm = this;
      axios
        .post("" + "/share/", {
          comment_id: vm.comment.id
        })
        .then(response => {
          vm.hasSharedComment = true;
          vm.numOfShares += 1;
        })
        .catch(error => {
          vm.hasSharedComment = false;
        });
    },
	**/
    agree() {
      var vm = this;
      axios
        .post("" + "/agree", {
          comment_id: this.comment.id,
          option_id: this.comment.optionId,
          poll_id: this.comment.poll_id
        })
        .then(function(response) {
          vm.numOfAgrees += 1;
          vm.setCannotAgree();
        })
        .catch(function(response) {});
    },

    setCannotAgree() {
        var option_voted_for = this.comment_optionId;
        vm.$emit("change_can_agree_state", option_voted_for);
    }
  }
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
</style>

