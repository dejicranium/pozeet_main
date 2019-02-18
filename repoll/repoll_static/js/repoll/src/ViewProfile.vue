


<script>
    import axios from 'axios';
    var siteUrl = "http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com:6543";
	const activityPOSTURL = "http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com:6543";

	var pollTabContent = document.getElementById('poll');
	pollTabContent.style.display = 'block';
	pollTabContent.style.visibility = 'visible';
	pollTabContent.style.opacity = 1;

    var tabs = document.getElementsByClassName('tab');
    tabs[0].style.borderBottom = 'solid 2px teal';
    tabs[0].style.fontWeight = 'bold';
        

    function showTabContent(tb, name){
        var tab = tb; 
        var tabs = document.getElementsByClassName('tab');
        for (var i = 0; i < tabs.length; i++){
            tabs[i].style.borderBottom = 'none';
            tabs[i].style.fontWeight = 'normal';
        }
        tab.style.borderBottom = 'solid 2px teal';
        tab.style.fontWeight = 'bold';
        
        var tabContents = document.getElementsByClassName('t-content');
        for (var i = 0; i < tabs.length; i++){
            tabContents[i].style.display = 'none';
            tabContents[i].style.visibility = 'hidden';
            tabContents[i].style.opacity = 0;
        }

        var tabContent = null;

        if (name=='polls'){
            tabContent = document.getElementById('poll');
        }
        else if(name=='opinions'){
            tabContent = document.getElementById('opinions');
        }
        else if (name=='c_and_s'){
            tabContent = document.getElementById('c_and_s');
        }
        else if (name=="l_amd_s"){
            tabContent = document.getElementById('l_and_s');
        }


        tabContent.style.display = 'block';

        tabContent.style.visibility = 'visible';
            
        tabContent.style.opacity = 1;
    }


    
    export default {
        name: 'ViewProfile',
           data(){
                return {
                    activities: [],
                    likesAndShares: [],
                    commentsAndReplies: [],
					num_of_followers: {{user.num_of_followers}},
					
					

                }

                
            },

		
            methods:{

				

                changePollData(id, value){
                	this.$set(this.activities, id, value);
            	
				},

				followUser(){
					var vm = this;
					axios.post(activityPOSTURL + "/follow/" + userId, {
					}).then(response =>{
						this.num_of_followers = this.num_of_followers  + 1;
					});

				},

				unfollowUser(){
					this.num_of_followers = this.num_of_followers - 1;
				},

                getCommentsAndReplies(){
					if (this.activities.c_and_s == null){
                    	axios.get("" + '/comments_and_replies/user_id=' + userId).then(response=> {
						this.changePollData('c_and_s', response.data.c_and_s);
                    	});
					}
                },

                getLikesAndShares(){
                    axios.get(setInterval + '/likes_and_shares/user_id=' + userId).then(response => {
                        this.changePollData('l_and_s', response.data.l_and_s);
                    });
                },
                getPosts(){
                    //if there are no opinions already
                    if (this.activities.opinions == null){
                        axios.get("" +'/posts/user_id=' + userId).then(response => {
                            this.changePollData('opinions', response.data.opinions);
							//this.activities.opinions = [],
                            //this.activities.opinions = response.data.opinions;
                        });
                    }
                },
            },

            created(){
                var vm = this;
                axios.get("" + '/polls/user_id=' + userId).then(response =>{
                    this.activities = response.data.activities;
                });
            },
    }

</script>