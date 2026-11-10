# Extra scenario for the "fail if the service is not running" requirement.
# The app is not started for this scenario (@service_down), so every request
# should fail instead of returning an answer.

Feature: Know when the service is down
  As a user
  I want my requests to fail loudly when the todo manager is not running
  so that I never mistake a missing service for an empty list

  Background:
    Given the todo manager is not running

  @service_down
  Scenario Outline: Error flow - a request fails when the todo manager is not running
    When I try to view the todos at <path>
    Then the request fails because nothing is answering

    Examples:
      | path     |
      | /todos   |
      | /todos/1 |
