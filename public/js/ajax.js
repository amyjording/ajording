
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
                    } else if (data['result_ok'] == false && data['type'] == 'email' || data['entry'] == 'email') {
                        $('#signin-email').toggleClass('has-error').next('span').toggleClass('is-visible').text(data['error_msg']);
                        console.log(data['error_msg']);
                    } else if (data['result_ok'] == false && data['type'] == 'password') {
                        $("#signin-password").toggleClass('has-error').next('span').toggleClass('is-visible').text(data['error_msg']);
                        console.log(data['error_msg']);
                    } else {
                        $('#loginMessage').addClass('alert-danger centered').text(data['error_msg'])
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
                data: $(this).serialize(),
                url: '/demo/signup',
                dataType: 'json',
                success : function(data) {
                    if (data['result_ok'] == true){
                        window.location.href = '/dash';
                    } else if (data['result_ok'] == false && data['entry'] == 'username') {
                        $('#signup-username').toggleClass('has-error').next('span').toggleClass('is-visible').text(data['error_msg']);
                        console.log(data['error_msg']);
                    } else if (data['result_ok'] == false && data['entry'] == 'email') {
                        $form_signup.find('input[type="email"]').toggleClass('has-error').next('span').toggleClass('is-visible').text(data['error_msg']);
                        console.log(data['error_msg']);
                    } else if (data['result_ok'] == false && data['entry'] == 'password') {
                        $('.toggle-pass').toggleClass('has-error').next('span').toggleClass('is-visible');
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
        $("#loginHelp").submit(function(event) {
            event.preventDefault();
            $.ajax({
                type: "POST",
                url: '/demo/identify',
                data: $(this).serialize(),
                dataType: 'json',
                success : function(response) {
                    if (response['result_ok'] == true){
                        $('#loginResetStatus').addClass('alert alert-success').html(response['success_msg']);
                    } else if (response['result_ok'] == false) {
                        $('#loginResetStatus').addClass('alert alert-danger').html(response['error_msg']);
                        console.log(response['error_msg']);
                    } else {
                        console.log(response['error_msg']);
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
        $("#updateUser").submit(function(event) {
        event.preventDefault();
        console.log("This is working");
            $.ajax({
                type: "POST",
                url: '/demo/settings',
                data: $(this).serialize(),
                dataType: 'json',
                success : function(data) {
                    if (data['result_ok'] == true){
                        $('#userSettingsStatus').addClass('alert alert-success').html(data['success_msg']);
                    } else if (data['result_ok'] == false) {
                        $('#userSettingsStatus').addClass('alert alert-danger').html(data['error_msg']);
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


    // change this to fire off when reCaptcha succeeds
    function recaptchaCallback(){
            $.ajax({
                type: "GET",
                url: '/contact',
                data: {'email':'true'},
                success : function(response) {
                    console.log(response);
                    $('#emailMe').attr("href", "mailto:"+response).text(response);                          
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
        };