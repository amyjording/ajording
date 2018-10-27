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
        $("#userSignUp").submit(function(event) {
        event.preventDefault();
            $.ajax({
                type: "POST",
                url: '/demo/signup',
                data: $(this).serialize(),
                dataType: 'json',
                success : function(data) {
                    if (data['result_ok'] == true){
                        window.location.href = '/work';
                    } 
                    else {
                        $( "#signupMessage" ).addClass( "alert-danger collapse in" ).html(data['error_msg']);
                        console.log(data['error_msg']);
                    }
                },
                error : function(xhr, status) {
                    // check if xhr.status is defined in $.ajax.statusCode
                    // if true, return false to stop this function
                    if (typeof this.statusCode[xhr.status] != 'undefined') {
                        return false;
                    }
                    // else continue
                    console.log('ajax.error');
                },
                statusCode: {
                    404: function(response) {
                        console.log('ajax.statusCode: 404');
                    },
                    500: function(response) {
                        console.log('ajax.statusCode: 500');
                    }
                }
            });
        });
    });