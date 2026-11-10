# steps for todos: add, view, mark done, delete
from pytest_bdd import given, parsers, then, when

from tests.step_definitions.common_steps import read_all_todos
from todo_api import constants
from todo_api.payloads import parse_xml, todo_payload, todo_xml

TITLE = r'"(?P<title>.*)"'
INCLUSION = r"(?P<inclusion>includes|does not include)"


# given

@given(parsers.re(rf"I have added a todo titled {TITLE}"))
def have_added_todo(context, title):
    todo = context.client.create_todo(title)
    context.remember_todo(title, todo["id"])


@given(parsers.re(rf"I have deleted the todo {TITLE}"))
def have_deleted_todo(context, title):
    delete_todo(context, title)
    assert context.last_response.status_code == constants.OK


@given(parsers.re(rf"the todo {TITLE} is (?P<state>done|not done)"))
def todo_is_set_to_state(context, title, state):
    response = amend_todo(context, context.todo_id_of(title), {"doneStatus": state == "done"})
    assert response.status_code == constants.OK, response.text


# when: adding

@when(parsers.re(rf'I add a todo titled {TITLE} with the description "(?P<description>.*)"'))
def add_todo_with_description(context, title, description):
    post_new_todo(context, todo_payload(title, description))


@when(parsers.re(rf"I add a todo titled {TITLE} with no other fields"))
def add_todo_with_title_only(context, title):
    post_new_todo(context, {"title": title})


@when(parsers.re(rf"I add a todo titled {TITLE} using an XML body"))
def add_todo_as_xml(context, title):
    context.last_response = context.client.send_xml("POST", constants.TODOS_PATH, todo_xml(title))
    remember_created_todo(context, title)


@when(parsers.re(r"I try to add a todo with the body (?P<body>.*)"))
def add_todo_with_raw_body(context, body):
    context.last_response = context.client.post_raw(constants.TODOS_PATH, constants.JSON_CONTENT_TYPE, body)


# when: viewing

@when(parsers.re(rf"I view the todo {TITLE}"))
def view_todo_by_title(context, title):
    context.last_response = context.client.get_todo(context.todo_id_of(title))


@when(parsers.re(r"I view the todo with the id (?P<todo_id>\S+)"))
def view_todo_by_id(context, todo_id):
    context.last_response = context.client.get_todo(todo_id)


@when("I view all todos")
def view_all_todos(context):
    context.last_response = context.client.get(constants.TODOS_PATH)


# when: completing

@when(parsers.re(rf"I mark the todo {TITLE} as done"))
def mark_todo_done(context, title):
    context.last_response = amend_todo(context, context.todo_id_of(title), {"doneStatus": True})


@when(parsers.re(r"I mark the todo with the id (?P<todo_id>\S+) as done"))
def mark_todo_done_by_id(context, todo_id):
    context.last_response = amend_todo(context, todo_id, {"doneStatus": True})


@when(parsers.re(rf"I reopen the todo {TITLE}"))
def reopen_todo(context, title):
    context.last_response = amend_todo(context, context.todo_id_of(title), {"doneStatus": False})


@when(parsers.re(rf'I set the done status of the todo {TITLE} to "(?P<value>.*)"'))
def set_done_status(context, title, value):
    context.last_response = amend_todo(context, context.todo_id_of(title), {"doneStatus": value})


# when: deleting

@when(parsers.re(rf"I delete the todo {TITLE}(?: again)?"))
def delete_todo_step(context, title):
    delete_todo(context, title)


# then

@then(parsers.re(rf'the new todo has the title {TITLE} and the description "(?P<description>.*)"'))
def new_todo_has_title_and_description(context, title, description):
    created = todo_fields(context.last_response)
    assert created["title"] == title
    assert created["description"] == description


@then("the new todo is not done")
def new_todo_is_not_done(context):
    assert todo_fields(context.last_response)["doneStatus"] == "false"


@then(parsers.re(rf"the todo {TITLE} is (?P<state>done|not done)"))
def todo_has_state(context, title, state):
    todo = read_todo(context, context.todo_id_of(title))
    assert todo["doneStatus"] == ("true" if state == "done" else "false")


@then(parsers.re(rf"the todo {TITLE} no longer exists"))
def todo_no_longer_exists(context, title):
    assert context.client.get_todo(context.todo_id_of(title)).status_code == constants.NOT_FOUND


@then(parsers.re(rf"the response contains exactly 1 todo titled {TITLE}"))
def response_contains_one_todo(context, title):
    assert titles_in(context.last_response) == [title]


@then(parsers.re(rf"the response {INCLUSION} the todo {TITLE}"))
def response_includes_todo(context, inclusion, title):
    assert_inclusion(title, titles_in(context.last_response), inclusion)


@then(parsers.re(rf"the list {INCLUSION} the todo {TITLE}"))
def list_includes_todo(context, inclusion, title):
    assert_inclusion(title, [todo["title"] for todo in read_all_todos(context)], inclusion)


# helpers

def post_new_todo(context, payload):
    context.last_response = context.client.post_json(constants.TODOS_PATH, payload)
    remember_created_todo(context, payload["title"])


def amend_todo(context, todo_id, fields):
    return context.client.post_json(context.client.todo_path(todo_id), fields)


def delete_todo(context, title):
    todo_id = context.todo_id_of(title)
    context.last_response = context.client.delete(context.client.todo_path(todo_id))


def remember_created_todo(context, title):
    if context.last_response.status_code == constants.CREATED:
        context.remember_todo(title, todo_fields(context.last_response)["id"])


def todo_fields(response):
    # the app answers in JSON or in XML depending on what was sent
    if response.headers["Content-Type"].startswith(constants.JSON_CONTENT_TYPE):
        return response.json()
    root = parse_xml(response.text)
    return {field.tag: field.text or "" for field in root}


def read_todo(context, todo_id):
    response = context.client.get_todo(todo_id)
    assert response.status_code == constants.OK, response.text
    return response.json()["todos"][0]


def titles_in(response):
    return [todo["title"] for todo in response.json()["todos"]]


def assert_inclusion(title, titles, inclusion):
    assert (title in titles) == (inclusion == "includes"), f"{title!r} vs {titles}"
