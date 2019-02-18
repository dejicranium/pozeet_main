<template id="show-new-poll-modal-template">
	<transition name="modal">

		<div class="modal-mask" v-show='show_new_poll_modal' @click='closeModal'>


			<div class="modal-container new-poll-modal" @click.stop>

				<!--there should be an if condition here
					to decide what to show to the user in the header.
					Basically, we'll need to check the leadingIntent-->
			
			
				<div class="modal-header" style='display:flex; flex-direction:row; color:grey; font-size: 15px;padding:0px;  height:50px;'>					
					<div :id='[pollType=="normal" ? "selected-tab" : "t"]' @click='pollType="normal"'>Normal</div>
					<div :id='[pollType=="picture" ? "selected-tab" : "t"]' @click='pollType="picture"'>Picture</div>
				</div>


				<div class="modal-body" >
					<div class='normal-poll-div' v-if='pollType == "normal"'>
						<form method="post" accept-charset="utf-8" enctype="multipart/form-data" id='new-poll-form'>
							
							<div style='padding: 10px 16px'>
								<div style='width:94%'>
									<input type='text' 
										class='form-control' 
										name='question' 
										id='poll-question' 
										placeholder='Question'
									 
									/>
								</div>


								<div class='add-context'>
									<textarea style='margin-bottom:5px;' @click='autoResize' placeholder= "Provide context: info, explanation, link or image."  name='info' class='form-control'></textarea>
								
								
									<label for="context-image" id='add-context-image' style='color:teal;height:20px;' @click='addContextImage'> Add Context Image </label>
									<img id='contextImageDisplay'/>
									<input type="file"
								 	id="context-image" 
								 	name="context-image"
								 	value="Add Image"
								 	accept=".jpg, .jpeg, .png" >
							
								</div>
						

								<div style='margin-bottom: 5px;'>
									<div v-for='option in options' :option='option' class='options-box'>							
										<input type='text' 
											class='form-control ' 
											:placeholder='option.placeholder' 
										v-model='option.text'/>								
									</div>
									<span class="selectBtn" @click="addNewOption">New Option</span>
								</div>
							</div>						
						
							<div style='width:100%; box-sizing:border-box;'>
								<div style='width:100%;padding-left:16px; margin-bottom:10px;'>
									<div>
									<label for='duration' class='form-label' style='font-size:12px;'> Duration: <span class='required'>*</span> </label>
										<select id="duration" name='timeDue'>
											<option value="1"> 24 hours</option>
											<option value="2"> 2 days</option>
											<option value="3"> 3 days</option>
											<option value="4"> 4 days</option>
											<option value="5"> 5 days</option>
											<option value="6"> 6 days</option>
											<option value="7"> 1 week</option>
										</select>
									</div>
								</div>

								<div style='padding:5px 16px;'>	
									<label for='category' class='form-label' style='font-size:12px;'> Publish to (max: 2): <span class='required'>*</span> <span class='expand' v-show="!expandCategories" @click="showCategories">Select Categories</span> </label>

									<div class='categories-selection' v-if='expandCategories'>
										<label v-for='category in categories' :category='category' @click='chooseCategory(category.categoryId, $event)'>
											<input disabled type='checkbox' :id="'checkbox_category_' + category.categoryId" :value='category.categoryId' @click.stop /> {{category.categoryName}}
											<span class='checkmark' @click.stop></span>
										</label>
									</div>
								
							
									<button type='button' @click='createPoll'> Share</button>

								</div>
						
							</div>

						</form>
					</div>



					<div v-else style='padding: 10px 16px;'>								
						<form enctype='multipart/form-data' id='image-poll-form'>
							<input type='text' 
									class='form-control' 
									name='question' 
									id='poll-question' 
									placeholder='Question'
									 style=''
								/>
							
							<div style='dislay:flex; flex-direction:row; flex-wrap:wrap; width:100%;'>
							<div v-for='option in imageOptions' :option='option' style='flex-basis:20%; display:flex; margin-bottom:20px; flex-direction:row; flex-wrap:wrap'>
								<div style='margin:auto; text-align:center; flex-wrap:wrap; box-sizing:box-sizing;'>	
									<div style=' margin-bottom:5px;'>

										<img height="120" width='120' :id="'image-display-' + option.classKey" style='border:0.5px solid darkgrey; border-radius:5px; background-color:whitesmoke;'/>
									</div>
									<label style='color:teal; font-weight:bold;'>
									<input type='file' 
										style='width:100%; height:30px; display:none;' 
										@click='triggerListener(option.classKey)'
										:id="'image-button-' + option.classKey"
										name='optionImage'
										accept=".jpg, .jpeg, .png" >
									+Add image</label>
																
									<input type='text'
										name='option' 
										class='form-control' 
										placeholder='Option title'
										style='width: 100%; height:40px; margin:auto; margin-bottom:5px;'/><br>
								
						
								</div>
							</div>
								<div>
									<div @click='addNewOption' style='background-color:darkgrey; margin-bottom: 10px; color: white; font-size: 15px; padding: px; border-radius: 20px; display:block; margin: 1px auto 10px auto; width:60px; text-align: center;'>+</div>
								</div>
							</div>



							<div style='width:100%; box-sizing:border-box;'>
								<div style='width:100%;padding-left:16px; margin-bottom:10px;'>
									<div>
										<label for='duration' class='form-label' style='font-size:12px;'> Duration: <span class='required'>*</span> </label>
											<select id="duration" name='timeDue'>
											<option value="1"> 24 hours</option>
											<option value="2"> 2 days</option>
											<option value="3"> 3 days</option>
											<option value="4"> 4 days</option>
											<option value="5"> 5 days</option>
											<option value="6"> 6 days</option>
											<option value="7"> 1 week</option>
											</select>
									</div>
								</div>
							

								<div style='padding:5px 16px;'>	
									<label for='category' class='form-label' style='font-size:12px;'> Publish to (max: 2): <span class='required'>*</span> <span class='expand' v-show="!expandCategories" @click="showCategories">Select Categories</span> </label>

									<div class='categories-selection' v-if='expandCategories'>
										<label v-for='category in categories' :category='category' @click='chooseCategory(category.categoryId, $event)'>
										<input disabled type='checkbox' :id="'checkbox_category_' + category.categoryId" :value='category.categoryId' @click.stop/> {{category.categoryName}}
										<span class='checkmark' @click.stop></span>

										</label>
									</div>
								
							
								</div>
								<button type='button' @click='createImagePoll'> Share </button>
                            </div>
                        </form>
					</div>
					
				</div>

            </div>
		</div>
	</transition>
</template>


<script>
var siteUrl = "http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com:6543";
	const activityPOSTURL = "http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com:6543";


	import axios from 'axios';
	export default { 
		name: 'NewPoll',
		props: ['show_new_poll_modal', 'categories'],
		delimiters: ['((', '))'],
		
		data(){
			return{

				options: [{
					text: '',
					placeholder: 'Option 1',
				},
				{
					text: '',
					placeholder: 'Option 2',
				},

				
				],
				alphabets : ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
				imageOptions: [{
					classKey: 1, 
					placeholder: 'A',
				},
				{
					classKey: 2, 
					placeholder: 'B',
				}
				],
				//determines whether to show the categories that can be selected
				expandCategories: false,
				toChoosePollType: false,
				pollType: 'normal',
				finalChosenCategories: '',
				finalChosenOptions: '',
				chosenCategories: [],
				//show the error while creating a poll
				pollErrorText: '',

			}
		},
		watch: {
			show_new_poll_modal: function(newValue){
				if (newValue == false){
					//close the categories to be expanded
					this.expandCategories = false;
				}
			}
		},

		computed:{
			allowedCategories(){
				if (this.chosenCategories.length == 2){
					var allowed = [];
					for (let i = 0; i < this.chosenCategories.length; i++){
						var categoryId = this.chosenCategories[i];
						var cate = this.categories.filter(c=>c.categoryId==categoryId)[0];
						allowed.push(cate);
					}

					return allowed;
				}

				return this.categories;
			}
		},

		methods: {
			//show categories to choose while creating a new poll
			showCategories(){
				this.expandCategories = true;
			},

			triggerListener(classKey){
				var inputButton = document.getElementById('image-button-' + classKey);
				var inputDisplay = document.getElementById('image-display-' +classKey);
				inputButton.addEventListener('input', function(){
					var imageFiles = inputButton.files;
					inputDisplay.style.width;
					inputDisplay.style.height;
					inputDisplay.src = window.URL.createObjectURL(imageFiles[0]);				
				});			
			},

			addContextImage(){
				var inputButton = document.getElementById('context-image');
				var inputDisplay = document.getElementById('contextImageDisplay');
				inputButton.addEventListener('input', function(){
					var imageFiles = inputButton.files;
					inputDisplay.style.width = "30px";
					inputDisplay.style.height = '30px';
					inputDisplay.src = window.URL.createObjectURL(imageFiles[0]);
				});
			},


			createPoll(event){

				if (this.chosenCategories.length < 2){
					this.pollErrorText = "Select at least 2 categories";
				}

				var categories = this.flattenCategories();
				var options = this.flattenOptions();
				var form = document.getElementById('new-poll-form');
				event.target.disabled = true;
				var formData = new FormData(form);
				formData.append('categories', categories);
				formData.append('options', options);

				var request = new XMLHttpRequest();
				var vm = this;
				
				vm.changeButtonContent(event.target, '...');

				request.open("POST", activityPOSTURL + '/ask');
				request.onreadystatechange = function(){
					if (request.readyState == XMLHttpRequest.DONE){
						if(request.status == 200){
							vm.$emit('close_new_poll_modal', true);
							vm.showSnackbar('Poll published!');
							vm.changeButtonContent(event.target, 'Share');
							event.target.disabled = false;
						}
						else {
							vm.showSnackbar('There was an error creating the poll. Please Retry');
							vm.changeButtonContent(event.target, 'Share');
							event.target.disabled = false;

						}
					
					}
				}
				
				request.send(formData);
			},

			createImagePoll(event){

				if (this.chosenCategories.length > 2){
					alert('You are allowed to choose only two categories');
					return 0;
				}
				var form = document.getElementById('image-poll-form');
				event.target.disabled = true;
				var formData = new FormData(form);
				var request = new XMLHttpRequest();
				var vm = this;
				var categories = this.flattenCategories();
				formData.append('categories', categories);

				this.changeButtonContent(event.target, '...');

				request.open("POST", activityPOSTURL + '/ask');
				request.onreadystatechange = function(){
					if (request.readyState == XMLHttpRequest.DONE){
						if(request.status == 200){
							vm.$emit('close_new_poll_modal', true);
							vm.showSnackbar('Poll published!');
							vm.changeButtonContent(event.target, 'Share');
							event.target.disabled = false;
						}
						else {
							vm.showSnackbar('There was an error creating the poll. Please Retry');
							vm.changeButtonContent(event.target, 'Share');
							event.target.disabled = false;

						}
					
					}
				}
				
				request.send(formData);
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
			addNewOption(){

				if (this.pollType == 'normal'){
					if (this.options.length < 10){
						var options_length = this.options.length + 1;
						var new_option = {text: '', placeholder: 'Option '+ options_length};
						this.options.push(new_option);
					}
				}

				else{
					var numOfImageOptions = this.imageOptions.length;
					var newClassKey =  numOfImageOptions + 1;
					var newLabel = this.alphabets[newClassKey];
					var newImageOption = {classKey: newClassKey, placeholder: newLabel};

					this.imageOptions.push(newImageOption);

				}

			},

			nextNewPollStep(){
				if(this.pollType != ''){
					this.toChoosePollType = false;

				}
			},

			flatten(array){
				var flattened = array.join(",");
				return flattened;
			},

			flattenCategories(){
				this.finalChosenCategories = this.flatten(this.chosenCategories);
				return this.finalChosenCategories;
			},

			flattenOptions(){
				this.finalChosenOptions = this.flatten(this.options.map(option=>option.text));
				return this.finalChosenOptions;
			},


			chooseCategory(categoryId, event){
				/**first of all, check whether the category has already been checked
				if the category has already been checked, remove it from the list **/
				 for (let i = 0; i < this.chosenCategories.length; i++){
				//if the category has already been checked, remove it from the list
					if (this.chosenCategories[i] == categoryId){
						let categoryIndex = this.chosenCategories.indexOf(categoryId);
						this.chosenCategories.splice(categoryIndex);
						document.getElementById('checkbox_category_' + categoryId).checked = false;

						return 0;
					}
				}
				
				//else, if it not there already, then just add it.
				if (this.chosenCategories.length < 2 ){
					this.chosenCategories.push(categoryId);
					document.getElementById('checkbox_category_' + categoryId).checked = true;
				}	

			},

			closeModal(){
				this.$emit('close_new_poll_modal', true);
			},
			addFileNameToElement(){

			},
		},

		mounted(){
			var addContextImage = document.getElementById('add-context-image');

		},	

	}


</script>

<style scoped>
	.modal-container .modal-body{
		position: relative;
		padding: 0px 0px 35px 0px;
	}

	.modal-container .modal-body .final-input{
	}
	.modal-container .modal-body button{
		position: absolute;
		right: 0; 
		bottom: 0;
		margin-right: 20px; 
	}
	.optionLabel {
		text-align: center;
	}
	.expand {
		background-color: lightgray;
		padding: 5px;
	}
	.selectBtn {
		background-color: lightgrey;
		padding: 5px;
		cursor: pointer;
	}
	.categories-selection {
		display: flex; 
		flex-wrap: wrap;
		justify-content: stretch; 
		width: 100%;
	}
	.error-text {
		color: red;
		font-size: 12px;
	}
</style>
