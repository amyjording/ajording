from selenium import webdriver
from selenium.webdriver.support.ui import Select

def before_all(context):
    context.browser = webdriver.Firefox()
    context.browser.implicitly_wait(4)

def after_all(context):
    context.browser.quit()