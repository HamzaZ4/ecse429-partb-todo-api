# Story 4: put a todo in a category
# the last two scenarios are @xfail, they fail because of Bug 06 and Bug 08

Feature: Put a todo in a category
  As a user
  I want to put a todo in a category
  so that I can group related tasks together

  Background:
    Given the todo manager is running
    And the list starts with the 2 default todos

  Scenario Outline: Normal flow - put a todo in a category
    Given I have added a todo titled "<title>"
    When I put the todo "<title>" in the category with id <category>
    Then the response status is 201
    And the todo "<title>" belongs to the category with id <category>
    And the default todos are unchanged

    Examples:
      | title                    | category |
      | finish the Part B report | 1        |
      | do laundry               | 2        |

  Scenario Outline: Alternate flow - take a todo out of a category
    Given the default todo "<title>" is in the category with id <category>
    When I take the todo "<title>" out of the category with id <category>
    Then the response status is 200
    And the todo "<title>" does not belong to the category with id <category>
    And the category with id <category> still exists

    Examples:
      | title          | category |
      | scan paperwork | 1        |

  Scenario Outline: Error flow - put a todo in a category that does not exist
    Given I have added a todo titled "<title>"
    When I put the todo "<title>" in the category with id <category>
    Then the response status is 404
    And the todo "<title>" does not belong to the category with id <category>
    And the default todos are unchanged

    Examples:
      | title         | category |
      | buy groceries | 99       |

  @xfail
  Scenario Outline: Alternate flow - see which todos are in a category
    Given the default todo "<title>" is in the category with id <category>
    When I view the todos of the category with id <category>
    Then the response status is 200
    And the response includes the todo "<title>"

    Examples:
      | title          | category |
      | scan paperwork | 1        |

  @xfail
  Scenario Outline: Alternate flow - delete a category that has a todo in it
    Given the default todo "<title>" is in the category with id <category>
    When I delete the category with id <category>
    Then the response status is 200
    And the todo "<title>" does not belong to the category with id <category>

    Examples:
      | title          | category |
      | scan paperwork | 1        |
