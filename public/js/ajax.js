$(document).ready(function() { 
        var $form_modal = $('.user-modal'),
        $form_login = $form_modal.find('#login'),
        $form_signup = $form_modal.find('#signup');
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
        $("#userLogin").submit(function(event) {
        var $form_modal = $('.user-modal'),
        $form_login = $form_modal.find('#login');
        event.preventDefault();
            $.ajax({
                type: "POST",
                url: '/demo/login',
                data: $(this).serialize(),
                dataType: 'json',
                success : function(data) {
                    if (data['result_ok'] == true){
                        window.location.href = '/dash';
                    } else if (data['result_ok'] == false && data['entry'] == 'email') {
                        $form_login.find('input[type="email"]').toggleClass('has-error').next('span').toggleClass('is-visible').text(data['error_msg']);
                        console.log(data['error_msg']);
                    } else if (data['result_ok'] == false && data['entry'] == 'password') {
                        $form_login.find('input[type="password"]').toggleClass('has-error').next('span').toggleClass('is-visible').text(data['error_msg']);
                        console.log(data['error_msg']);
                    } else {
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


$(document).ready(function() { 
        $("#userSignUp").submit(function(event) {
        var $form_modal = $('.user-modal'),
        $form_login = $form_modal.find('#login'),
        $form_signup = $form_modal.find('#signup');
        event.preventDefault();
            $.ajax({
                type: "POST",
                url: '/demo/signup',
                data: $(this).serialize(),
                dataType: 'json',
                success : function(data) {
                    if (data['result_ok'] == true){
                        window.location.href = '/dash';
                    } else if (data['result_ok'] == false && data['entry'] == 'username') {
                        $form_signup.find('input[type="text"]').toggleClass('has-error').next('span').toggleClass('is-visible').text(data['error_msg']);
                        console.log(data['error_msg']);
                    } else if (data['result_ok'] == false && data['entry'] == 'email') {
                        $form_signup.find('input[type="email"]').toggleClass('has-error').next('span').toggleClass('is-visible').text(data['error_msg']);
                        console.log(data['error_msg']);
                    } else if (data['result_ok'] == false && data['entry'] == 'password') {
                        $form_signup.find('input[name="password"]').toggleClass('has-error').next('span').toggleClass('is-visible');
                        console.log(data['error_msg']);
                    } else {
                        console.log(data['entry']);
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