$(document).ready(function($) {
	tab = $('.tabs h3 a');

	tab.on('click', function(event) {
		event.preventDefault();
		tab.removeClass('active');
		$(this).addClass('active');

		tab_content = $(this).attr('href');
		$('div[id$="tab-content"]').removeClass('active');
		$(tab_content).addClass('active');
	});
});


function deleteAccount(){
	console.log("clicked!");
  	var r = confirm("Are you sure you wish to delete your account? Select OK to delete. This is permanent.");
  	if (r == true) {
    	window.location.href = '/demo/delete';
  	} else {
    	return false;
  	}
 }