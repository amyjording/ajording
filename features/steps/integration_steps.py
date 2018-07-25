# -- FILE: features/steps/example_steps.py
from behave import given, when, then, step, use_fixture

@given('I start on index')
def step_impl(context):
	context.browser.get('http://localhost:8080')

@when('I click the link to "{link_text}"')
def step_impl(context, link_text):
	go_to_page = context.browser.find_element_by_xpath("//*[@id='{0}-link']".format(link_text)) #*[name()='use' and @*='#{0}']//html/body/svg[1]/symbol/a
	go_to_page.click()

@then('I see "{title_text}" as the title of page')  # String literal is currently not passing through here correctly, so repeating
def step_impl(context, title_text):
	element = context.browser.find_element_by_tag_name('h1')
	assert element.text == "{0}".format(title_text)
"""
@then('I see "My Work" as the title of page')  # String literal is currently not passing through here correctly, so repeating
def step_impl(context):
	element = context.browser.find_element_by_tag_name('h1')
	assert element.text == "My Work"

@then('I see "Try It" as the title of page')  # String literal is currently not passing through here correctly, so repeating
def step_impl(context):
	element = context.browser.find_element_by_tag_name('h1')
	assert element.text == "Try It"

@then('I see "Contact Me" as the title of page')  # String literal is currently not passing through here correctly, so repeating
def step_impl(context):
	element = context.browser.find_element_by_tag_name('h1')
	assert element.text == "Contact Me"
"""

@then('I click the link "Amy Jording"')
def step_impl(context):
	context.browser.find_element_by_xpath("//*[@id='home']").click()

@then('I return to index')
def step_impl(context):
	home = context.browser.find_element_by_xpath("//h1[contains(text(), 'Amy Jording')]")
	assert home


