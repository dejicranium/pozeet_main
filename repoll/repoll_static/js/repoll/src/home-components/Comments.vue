<template type='x/template' id='comments-template'>
	<transition name='modal'>
		<div class="modal-mask" id='view-comments-modal' v-if='show_view_comments_modal' >
			<div class="modal-container">
				<div class='comment-container'> 
					<div class='tabs'>
						<div class='tabs' >
							<input type='radio' 
							name='input-tab' 
							id='all-comments' 
							/>
							<label for='all-comments'>All</label>
						</div>

					<div class='tabs'>
						<input type='radio' name='input-tab'/>
						<label></label>
					</div>
				</div>
		
			<div>
				<comment></comment>
			</div>

			</div>
	
	
		</div>
 	</div>


		</div>
	</div>
	</transition>


</template>

<script>
	export default {
		name: 'Comments', 
		props: ['show_view_comments_modal',],
	}
</script>