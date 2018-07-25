# -- FILE: features/example.feature
Feature: Integration
  As a visitor
  I want to see all four links on index
  So that I can click on each one and click back to index
  Scenario: Visit each page
    Given I start on index
    When I click the link to "about"
    Then I see "About Me" as the title of page
    Then I click the link "Amy Jording"
    And I return to index
    When I click the link to "work"
    Then I see "My Work" as the title of page
    Then I click the link "Amy Jording"
    And I return to index
    When I click the link to "demo"
    Then I see "Try It" as the title of page
    Then I click the link "Amy Jording"
    And I return to index
    When I click the link to "contact"
    Then I see "Contact Me" as the title of page
    Then I click the link "Amy Jording"
    And I return to index