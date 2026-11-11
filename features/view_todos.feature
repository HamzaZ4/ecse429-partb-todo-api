# Story 2: view my todos

Feature: View my todos
  As a user
  I want to look at my todos
  so that I know what is on my list

  Background:
    Given the todo manager is running
    And the list starts with the 2 default todos

  Scenario Outline: Normal flow - view the whole list
    Given I have added a todo titled "<title>"
    When I view all todos
    Then the response status is 200
    And the list contains 3 todos
    And the list includes the todo "<title>"

    Examples:
      | title                    |
      | finish the Part B report |
      | email the prof           |

  Scenario Outline: Alternate flow - view one todo by its id
    Given I have added a todo titled "<title>"
    When I view the todo "<title>"
    Then the response status is 200
    And the response contains exactly 1 todo titled "<title>"

    Examples:
      | title                    |
      | print the lecture notes  |
      | return the library books |

  Scenario Outline: Error flow - view a todo that does not exist
    When I view the todo with the id <id>
    Then the response status is 404
    And the error message contains "Could not find an instance"
    And the default todos are unchanged

    Examples:
      | id   |
      | 9999 |
      | abc  |
