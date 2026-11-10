# steps every story uses: setup, status code, error message, list size, default todos
import requests
from pytest_bdd import given, parsers, then, when

from todo_api import constants
from todo_api.server import is_service_up, require_service_running


@given("the todo manager is running")
def todo_manager_is_running():
    require_service_running()


@given("the todo manager is not running")
def todo_manager_is_not_running():
    assert not is_service_up()


@given(parsers.re(r"the list starts with the (?P<count>\d+) default todos"))
def list_starts_with_default_todos(context, count):
    todos = read_all_todos(context)
    # the order of the todos changes between runs, so I sort the titles
    assert sorted(todo["title"] for todo in todos) == sorted(constants.DEFAULT_TODO_TITLES)
    assert len(todos) == int(count)
    for todo in todos:
        context.remember_todo(todo["title"], todo["id"])
    # keep them to compare with at the end of the scenario
    context.default_todos = todos


@when(parsers.re(r"I try to view the todos at (?P<path>\S+)"))
def try_to_view_todos(context, path):
    try:
        context.client.get(path)
        context.request_failed = False
    except requests.RequestException:
        context.request_failed = True


@then(parsers.re(r"the response status is (?P<status>\d+)"))
def response_status_is(context, status):
    actual = context.last_response.status_code
    assert actual == int(status), f"expected {status} but got {actual}: {context.last_response.text}"


@then(parsers.re(r'the error message contains "(?P<fragment>.*)"'))
def error_message_contains(context, fragment):
    messages = error_messages_of(context.last_response)
    assert any(fragment in message for message in messages), f"no message contains {fragment!r}: {messages}"


@then(parsers.re(r"the list contains (?P<count>\d+) todos"))
def list_contains_count(context, count):
    assert len(read_all_todos(context)) == int(count)


@then("the default todos are unchanged")
def default_todos_are_unchanged(context):
    todos_now = {todo["id"]: todo for todo in read_all_todos(context)}
    for before in context.default_todos:
        now = todos_now.get(before["id"])
        assert now == before, f"default todo {before['id']} was {before} but is now {now}"


@then("the request fails because nothing is answering")
def request_fails_because_nothing_answers(context):
    assert context.request_failed, "the request got an answer although nothing should be running"


def error_messages_of(response):
    try:
        return response.json().get("errorMessages", [])
    except ValueError:
        return []  # error status with no body at all


def read_all_todos(context):
    response = context.client.get(constants.TODOS_PATH)
    assert response.status_code == constants.OK, response.text
    return response.json()["todos"]
