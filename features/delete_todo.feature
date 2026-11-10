# Story 5 of 5 (ECSE 429 Part B, working alone, todos only)
# Normal flow (delete a todo), alternate flow (delete a todo that belongs to a
# project and a category) and error flow (delete the same todo twice).

Feature: Delete a todo
  As a user
  I want to delete a todo
  so that my list only holds the tasks I still care about

  Background:
    Given the todo manager is running
    And the list starts with the 2 default todos

  Scenario Outline: Normal flow - delete a todo I added
    Given I have added a todo titled "<title>"
    When I delete the todo "<title>"
    Then the response status is 200
    And the todo "<title>" no longer exists
    And the list contains 2 todos
    And the default todos are unchanged

    Examples:
      | title                    |
      | finish the Part B report |
      | return the library books |

  Scenario Outline: Alternate flow - delete a todo that belongs to a project and a category
    When I delete the todo "<title>"
    Then the response status is 200
    And the todo "<title>" no longer exists
    And the project with id <project> no longer lists the todo "<title>"
    And the project with id <project> still exists
    And the category with id <category> still exists

    Examples:
      | title          | project | category |
      | scan paperwork | 1       | 1        |

  Scenario Outline: Error flow - delete a todo twice
    Given I have added a todo titled "<title>"
    And I have deleted the todo "<title>"
    When I delete the todo "<title>" again
    Then the response status is 404
    And the error message contains "Could not find"
    And the list contains 2 todos

    Examples:
      | title         |
      | go to the gym |
