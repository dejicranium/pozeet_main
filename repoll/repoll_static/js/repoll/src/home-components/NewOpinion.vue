<template id='new-opinion-template' type='x/template'>
	<transition name='modal'>
		<div class='modal-mask' v-show='show_opinion_modal' @click='closeModal'>
			<div class='modal-container' @click.stop >
				<div class='modal-header' style='color:black'>
					<p>New opinion</p>
				</div>

			<div class='modal-body'>
				<form id='opinion-form' enctype='multipart/form-data' method='post'>
					<textarea style='width: 100%; border-radius:0px; font-size:13px; margin-bottom:5px;; ' v-model='opinion' id='comment-input' @click='autoResize' class='form-control final-input' name='comment' form='comment-form' placeholder='Have your say'></textarea>
					
					<div> 
          			<label @click='addOpinionImage' id='opinion-image-label' style='background-color:lightgrey; display:inline-block; padding:5px; border-radius:5px; margin-left:10px;'>
				
					<input type="file" style='display:none'
               		id="opinion-image" name="opinion-image" accept="image/png, image/jpeg"/>
					<span><i class="far fa-image button-icon" ></i>Add image</span>
					<img id='opinion-image-display'>					

					</label><br>
					</div>
				</form>

			</div>
			<div class="modal-footer">
				<button type='button' id='createOpinionButton' style='margin-bottom: 10px; border-radius:10px; margin-left:10px;margin-right:10px;' @click='createOpinion'>  <i class="fa fa-circle-o-notch fa-spin" ></i>Share</button>
				</div> 
			</div>

		</div>
	</transition>
</template>


<script>
var siteUrl = "http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com:6543";
	const activityPOSTURL = "";


	import axios from 'axios';
	export default {
		name: 'NewOpinion',
		props: ['show_opinion_modal'],

		data(){
			return{
				opinion: '',
				newOpinionObject: {},
 			}
		},

		mounted(){
		
		},

		methods:{

			addOpinionImage(){
				var opinionImageInput = document.getElementById('opinion-image');
				var opinionImageDisplay = document.getElementById('opinion-image-display');
				var opinionImageInputLabel = document.getElementById('opinion-image-label');
				var opinionImageInputHeight = opinionImageInputLabel.clientHeight;

				opinionImageInput.addEventListener('input', function(){
					var imageFiles = opinionImageInput.files;
					var neededFile = imageFiles[0];
					opinionImageDisplay.style.height = '20px';
					opinionImageDisplay.style.width = '20px';
					opinionImageDisplay.src = window.URL.createObjectURL(neededFile);
				});
		},


			createOpinion(event){
				var vm = this;
				/**var target = event.target;
				event.target.innerHTML = '...';
				target.disabled = true;
				axios.post("" + '/new/opinion',{
					opinion: vm.opinion,
			
			
				}).then(function(response){
					vm.opinion = '';
					target.innerHTML = 'Share';
					target.disabled = false;

			**/

					var form = document.getElementById('opinion-form');
					event.target.disabled = true;
					var formData = new FormData(form);
					formData.append('opinion', vm.opinion);
					var request = new XMLHttpRequest();
					vm.changeButtonContent(event.target, '...');
					request.open("POST", activityPOSTURL + '/new/opinion');
					request.onreadystatechange = function(){
						if (request.readyState == XMLHttpRequest.DONE){
							if(request.status == 200){
								vm.closeModal();
								vm.showSnackbar('Opinion published!');
								vm.changeButtonContent(event.target, 'Share');
								event.target.disabled = false;
								vm.newOpinionObject = JSON.parse(request.response.data);
								vm.addToActivities();

							}
							else {
								vm.showSnackbar('There was an error sharing your opinion. Please Retry');
								vm.changeButtonContent(event.target, 'Share');
								event.target.disabled = false;

							}	
					
						}
					}
					request.send(formData);
				},

			closeModal(){
				this.$emit('close_new_opinion_modal', true);

			},
			packageNewOpinion(jsonObject){

			},

			alterObject(key, value){
				this.$set(this.newOpinionObject, key, value);
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

			addToActivities(){
				this.$emit('act_add_to_activities', this.newOpinionObject);
			},


		},		
	}
</script>

<style scoped>
	.modal-container { 
		height:90%;
		display: flex;
		align-items: stretch;
		flex-direction: column;
		padding-bottom: 10px;
	}
	.modal-container .modal-header{
		height: 5%;
	}

	.modal-header p {
		font-size: 12px;
		font-weight: bold; 
	}
	.modal-container .modal-body{
		display: flex; 
		flex-direction: column;
		width:100%;
		height: 90%;
		box-sizing:border-box;  
		padding-right:0px; 
		padding-left:0px; 
		padding-top:0px;
	}
	.modal-body form {
		height:100%;
		display: flex;
		flex-direction: column;
		border: 0;
	}
	.modal-body form textarea{
		height: 90%;
	}
	.modal-body label {
		display: flex;
		align-items: center;
		background-color:whitesmoke;
		padding: 5px; 
		border-radius: 5px;

	}
	.modal-footer {
		height: 5%;		
		display: flex; 
		justify-content: flex-end;
		align-items: center;
		padding: 2px;

	}
	.modal-footer button {
		padding: 5px; 
		border-radius: 5px;
		background-color: teal;
		color: white;
		border: 0; 
		text-align: center;
	}

</style>
