	<template id='respondents-template'>
		<transition name='modal'>
			<div class="modal-mask" v-show='show_users_modal' @click='closeModal'>
				<div class="m-container" @click.stop>
                    <div class="header">
                        <div class="close-box">
                            <p class="close-mark" @click="closeModal">x</p>
                        </div>
                    </div>
					<div class="container" v-for="user in users">
                        <user-card :user='user'></user-card>
                        <!--<div>
                            <img src="/static/rename.svg" v-show="listLoading"/>
                        </div>
                        <div class="image">
                			<img src="https://pbs.twimg.com/profile_images/1081905771028320256/yajLUZzZ_400x400.jpg"/>
            			</div>
            			<div class="detail">
                			<div class="name">{{user.userName}}</div>
                			<div class="username">{{user.username}}</div>
            			</div>
            			<div class="follow">
                			<button class="button" @click="followUser">Follow</button>
            			</div>
                        -->
        			</div>
				</div>
			</div>
		</transition>
	</template>


<script>
var siteUrl = "";
	const activityPOSTURL = "";

    import axios from 'axios';
    import UserCard from './UserCard.vue';

	export default {
		name: 'UsersModal', 
        props: ['show_users_modal', 'url_to_load'],
        components: {'user-card': UserCard},

		data(){
			return{	
                users: [],
                listLoading: false,
			}
        },
        methods: {
            followUser(event){
                var vm = this;
                event.target.disabled = true;
                axios.post(activityPOSTURL + "/follow/" + userId, {
                }).then(response =>{
                    vm.user.num_of_followers +=1;
                    event.target.disabled = false;
                }).catch(error=>{
                    event.target.disabled = false;
                });

		    },
            closeModal(){
                this.$emit('act_close_users_modal', false);
            }
        },
		watch:{
			show_users_modal: function(val){
				if (val == true){
                    var vm = this;
                    vm.listLoading = true;
					axios.get("" + vm.url_to_load, {
					}).then(response=>{
                        vm.users = response.data;
                        vm.listLoading = false;
					});
                }
                else {
                    //clear the users' list
                    this.users = [];
                }
            },
            
		},

		
	}
</script>
<style scoped>
        .modal-mask {
            display: flex;
            justify-content: center;
            align-items: center;

        }
        .m-container {
            width: 250px;
            box-sizing: border-box;
            padding: 0;
            background-color: white; 
            flex-direction: column;
            -ms-flex-direction: column;
            justify-content: stretch;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            max-height: calc(100% - 40px);
            overflow-y: scroll;
            margin: auto;
        }
        .header {
            border-bottom: 1px solid lightgrey;
            padding: 10px 5px; 
            display: flex; 
            justify-content: flex-end;

        }
        .close-box {
            display: flex;
            justify-content: center;
            box-sizing: border-box;
            padding-right: 5px;
        }
        .close-mark {
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            color: darkgrey;
        }
        .container {
            display: flex;
            flex-direction: row;
            box-sizing: border-box;
            -ms-flex-direction: row;
            align-items: stretch;
            padding: 5px 5px;
            justify-content: center;
        }
        .image {
            align-items: center;
            justify-content: center;
            padding: 5px 5px;
        }
        .image img {
            max-width: 44px;
            max-height: 44px;
            border-radius: 50%;
        }

        .detail {
            display: flex; 
            flex-direction: column;
            justify-content: center;
            padding: 5px 5px;
            font-size: 14px;
            width: 100px;
        }
        .detail :first-child {
            font-weight: bold;
        }
        .detail div {
            overflow-x: hidden;
            overflow-y: hidden;
            text-overflow: ellipsis;
            -ms-text-overflow: ellipsis;
            -o-text-overflow: ellipsis;
        }
        .detail .name {
            text-overflow: ellipsis;
            -ms-text-overflow: ellipsis;
            -o-text-overflow: ellipsis;
            overflow: hidden;
        }
        .detail .username {
            color: darkgrey;
        }
        .follow {
            padding: 5px 5px;
            display: flex;
            align-items: center;
        }
        .follow button {
            border: 0; 
            border-radius: 3px; 
            padding: 8px 8px;
            background-color: teal;
            color: white;
        }
        
</style>