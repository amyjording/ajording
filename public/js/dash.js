$(document).ready(function() { 
        var $form_modal = $('.user-modal'),
        $form_login = $form_modal.find('#login'),
        $form_signup = $form_modal.find('#signup');
        $("#loginHelp").submit(function(event) {
        event.preventDefault();
            $.ajax({
                type: "PUT",
                url: '/dash/PUT',
                data: $(this).serialize(),
                dataType: 'json',
                success : function(data) {
                    if (data['result_ok'] == false){
                        $( "#pinStatus" ).addClass( "alert-danger collapse in" ).html(data['error_msg']);
                        console.log(data['error_msg']);
                    } 
                    else {
                        $( "#dynamicIDhere" ).addClass( "pinned" );
                    } 
                }
            });
        });
    });