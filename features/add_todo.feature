# Story 1: add a todo

Feature: Add a todo
  As a user
  I want to add a todo to my list
  so that I can keep track of the tasks I still have to do

  Background:
    Given the todo manager is running
    And the list starts with the 2 default todos

  Scenario Outline: Normal flow - add a todo with a title and a description
    When I add a todo titled "<title>" with the description "<description>"
    Then the response status is 201
    And the new todo has the title "<title>" and the description "<description>"
    And the new todo is not done
    And the list contains 3 todos
    And the default todos are unchanged

    Examples:
      | title                    | description                          |
      | finish the Part B report | add the repo link and the video link |
      | email the prof           | ask about the project deadline       |
      | buy groceries            | milk, eggs and rice                  |

  Scenario Outline: Alternate flow - add a todo with only a title
    When I add a todo titled "<title>" with no other fields
    Then the response status is 201
    And the new todo has the title "<title>" and the description ""
    And the new todo is not done
    And the list contains 3 todos
    And the default todos are unchanged

    Examples:
      | title                   |
      | go to the gym           |
      | print the lecture notes |

  Scenario Outline: Alternate flow - add a todo sent as XML
    When I add a todo titled "<title>" using an XML body
    Then the response status is 201
    And the new todo has the title "<title>" and the description ""
    And the list contains 3 todos
    And the default todos are unchanged

    Examples:
      | title                    |
      | renew my student card    |
      | return the library books |

  Scenario Outline: Error flow - add a todo with an invalid body
    When I try to add a todo with the body <body>
    Then the response status is 400
    And the error message contains "<message>"
    And the list contains 2 todos
    And the default todos are unchanged

    Examples:
      | body                                  | message              |
      | {}                                    | field is mandatory   |
      | {"title": ""}                         | can not be empty     |
      | {"title": "x", "doneStatus": "maybe"} | should be BOOLEAN    |
      | {"title": "x", "unknown": "y"}        | Could not find field |
