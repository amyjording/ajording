import os, os.path
import cherrypy


#-- Main User Account Template --#
def user_account(status, content):
    html = f"""<section class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <h1 class="page-header"> {status} </h1>
            {content}
            </section>
            """
    return html

#-- Partials - content --#

def user_login_signup(msg=None):
    status = f"Come on in" # Login or Sign In
    html = f"""
    <div class="logorow">
        <nav class="main-nav">
            <ul>
                <li><a class="signin" href="#0">Sign in</a> </li>
                <li><a class="signup" href="#0">Sign up</a></li>
            </ul>
        </nav>

        <div class="user-modal">
        <div class="user-modal-container">
            <ul class="switcher">
                <li><a href="#0">Sign in</a></li>
                <li><a href="#0">New account</a></li>
            </ul>

            <div id="login">
                <form class="form">
                    <p class="fieldset">
                        <label class="image-replace email" for="signin-email">E-mail</label>
                        <input class="full-width has-padding has-border" id="signin-email" type="email" placeholder="E-mail">
                        <span class="error-message">An account with this email address does not exist!</span>
                    </p>

                    <p class="fieldset">
                        <label class="image-replace password" for="signin-password">Password</label>
                        <input class="full-width has-padding has-border" id="signin-password" type="password"  placeholder="Password">
                        <a href="#0" class="hide-password">Show</a>
                        <span class="error-message">Wrong password! Try again.</span>
                    </p>

                    <p class="fieldset">
                        <input type="checkbox" id="remember-me" checked>
                        <label for="remember-me">Remember me</label>
                    </p>
                    <p class=""><a style="float:right; margin-top: -15px; margin-bottom: 15px;" href="#0">Forgot your password?</a></p>
                    <p class="fieldset">
                        <input class="full-width" type="submit" value="Login">
                    </p>
                </form>
                <div id="signupMessage" class="alert collapse">
                    <p>{msg}</p>
                </div>
                <!-- <a href="#0" class="close-form">Close</a> -->
            </div>

            <div id="signup">
                <form id="userSignUp" class="form" method="POST" action="get-in">
                    <input type="hidden" name="signup" value="1">
                    <p class="fieldset">
                        <label class="image-replace username" for="signup-username">Username</label>
                        <input class="full-width has-padding has-border" id="signup-username" type="text" name="username" placeholder="Username">
                        <span class="error-message">Your username can only contain numeric and alphabetic symbols!</span>
                    </p>

                    <p class="fieldset">
                        <label class="image-replace email" for="signup-email">E-mail</label>
                        <input class="full-width has-padding has-border" id="signup-email" type="email" name="email" placeholder="E-mail">
                        <span class="error-message">Enter a valid email address!</span>
                    </p>

                    <p class="fieldset">
                        <label class="image-replace password" for="signup-password">Password</label>
                        <input class="full-width has-padding has-border" id="signup-password" type="password" name="password" placeholder="Password">
                        <a href="#0" class="hide-password">Show</a>
                        <span class="error-message">Your password has to be at least 6 characters long!</span>
                    </p>

                    <p class="fieldset">
                        <input type="checkbox" id="accept-terms">
                        <label for="accept-terms">I agree to the <a class="accept-terms" href="#0">Terms</a></label>
                    </p>

                    <p class="fieldset">
                        <input class="full-width has-padding" type="submit" value="Create account">
                    </p>
                </form>
                <div id="signupMessage" class="alert collapse">
                    <p>{msg}</p>
                </div>
                <a href="#0" class="cd-close-form">Close</a>
            </div>

            <div id="reset-password">
                <p class="form-message">Lost your password? Please enter your email address.</br> You will receive a link to create a new password.</p>

                <form class="form">
                    <p class="fieldset">
                        <label class="image-replace email" for="reset-email">E-mail</label>
                        <input class="full-width has-padding has-border" id="reset-email" type="email" placeholder="E-mail">
                        <span class="error-message">An account with this email does not exist!</span>
                    </p>

                    <p class="fieldset">
                        <input class="full-width has-padding" type="submit" value="Reset password">
                    </p>
                </form>
                </div>
                </div><a href="#0" class="close-form">Close</a></p>
            </div>       
        </div>
    </div>
"""
    return status, html

def user_logout(msg): #msg is either with session -> You have been logged out. or no session -> #You are not logged in. You may login here:
    status = u"Logged out"
    html = f"""<div class="alert alert-success collapse collapse in">
            {msg} 
            <a href="/demo/get-in" class="btn btn-primary">Login</a>
            </div>"""
    return status, html

def user_login_recover_form(msg=None, alert='', collapse=''):
    status = u"Account Recovery"
    html = f"""                                    
        <h4>Can't remember your login credentials? No problem.</h4>
        <form id="loginHelp" method="POST" action="identify">
            <div class="form-group required">
                <input type="radio" class="form-control" name="resetpass" value="true"><label> Recover Password </label>
                <input type="radio" class="form-control" name="senduser" value="true"><label> Recover Username </label>
                <p>Enter the email address associated with your account.</p><br>
                <label class="control-label" for="email">Email</label>
                <input type="text" class="form-control" name="email" placeholder="Email">
            </div>
            <button type="submit" id="submitregister" class="btn btn-primary btn-block">Continue</button>
            </form>
            </div>
        <br>
        <div id="loginResetStatus" class="alert alert-{alert} collapse collapse {collapse}">
                <p>{msg}</p>"""
    return status, html


def user_reset_password(user_id):
    status = u"Choose a new password"
    html = f"""                  
            <form id="loginHelp" method='POST' action="identify">
            <input type="hidden" name="user_token" value="{user_id}">
            <div class="form-group required">
                <label class="control-label" for="userpassword">Password *</label>
                <input type="password" class="form-control" name="password" placeholder="Password">
            </div>
            <button type="submit" id="submitregister" class="btn btn-primary btn-block">Continue</button> 
        </form>
        <br>
        <div id="loginRecoveryStatus" class="alert collapse"><p> </p></div>     
        </div>"""
    return status, html

def invalid_token():
    status = u"Account Recovery"
    html = u"""
            <div class="alert alert-danger collapse collapse in">
            The Password Reset token is invalid. 
            <a href="/user/identify" class="btn btn-primary">Recover your username or password here.</a>
            </div>
            """
