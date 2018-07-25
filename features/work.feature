# -- FILE: features/example.feature
Feature: Integration
  As a reviewer
  I want to review portfolio cards
  So that I can click each reference link and have a new window open to the url
  Scenario: Visit work page
    Given I start on work
    When I click the link to "feedbackcommons.org"
    Then I see a new tab or window "Feedback Commons Home | Feedback Commons" as the title of page
