$(document).ready(function() { 
        $("#loginHelp").submit(function(event) {
        event.preventDefault();
            $.ajax({
                type: "POST",
                url: '/demo/identify',
                data: $(this).serialize(),
                dataType: 'json',
                success : function(data) {
                    if (data['result_ok'] == true){
                        $( "#loginRecoveryStatus" ).addClass( "alert-success collapse in" ).html(data['success_msg']);
                        console.log(data['success_msg']);
                    } 
                    else {
                        $( "#loginRecoveryStatus" ).addClass( "alert-danger collapse in" ).html(data['error_msg']);
                        console.log(data['error_msg']);
                    } 
                }
            });
        });
    });

$(document).ready(function() { 
        $("#signup-tab-content").submit(function(event) {
        event.preventDefault();
            $.ajax({
                type: "POST",
                url: '/demo/signup',
                data: $(this).serialize(),
                dataType: 'json',
                success : function(data) {
                    if (data['result_ok'] == true){
                        $( "#signup_msg" ).addClass( "alert-success collapse in" ).html(data['success_msg']);
                        console.log(data['success_msg']);
                    } 
                    else {
                        $( "#signup_msg" ).addClass( "alert-danger collapse in" ).html(data['error_msg']);
                        console.log(data['error_msg']);
                    } 
                }
            });
        });
    });