# Story 3 of 5 (ECSE 429 Part B, working alone, todos only)
# Normal flow (mark a todo as done), alternate flow (reopen it) and error flow
# (a done status that is not true or false).
# The last scenario is tagged @xfail: it describes what the API should do,
# fails today (see bugs/Bug_07) and is reported as an expected failure.

Feature: Mark a todo as done
  As a user
  I want to mark a todo as done, or reopen it
  so that I can see which tasks are finished and which are still open

  Background:
    Given the todo manager is running
    And the list starts with the 2 default todos

  Scenario Outline: Normal flow - mark a todo as done
    Given I have added a todo titled "<title>"
    When I mark the todo "<title>" as done
    Then the response status is 200
    And the todo "<title>" is done
    And the default todos are unchanged

    Examples:
      | title                    |
      | finish the Part B report |
      | email the prof           |

  Scenario Outline: Alternate flow - reopen a todo that was done
    Given I have added a todo titled "<title>"
    And the todo "<title>" is done
    When I reopen the todo "<title>"
    Then the response status is 200
    And the todo "<title>" is not done
    And the default todos are unchanged

    Examples:
      | title      |
      | do laundry |

  Scenario Outline: Error flow - give a todo a done status that is not true or false
    Given I have added a todo titled "<title>"
    When I set the done status of the todo "<title>" to "<value>"
    Then the response status is 400
    And the error message contains "should be BOOLEAN"
    And the todo "<title>" is not done

    Examples:
      | title         | value |
      | buy groceries | maybe |
      | go to the gym | 2     |

  @xfail
  Scenario Outline: Error flow - the error message for an unknown todo uses the same wording as GET
    When I mark the todo with the id <id> as done
    Then the response status is 404
    And the error message contains "Could not find"

    Examples:
      | id   |
      | 9999 |
