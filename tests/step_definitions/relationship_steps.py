# steps for how todos relate to categories and projects
from pytest_bdd import given, parsers, then, when

from tests.step_definitions.todo_steps import TITLE
from todo_api import constants


@given(parsers.re(rf"the default todo {TITLE} is in the category with id (?P<category_id>\d+)"))
def default_todo_is_in_category(context, title, category_id):
    todo_id = context.todo_id_of(title)
    if category_id not in category_ids_of(context, todo_id):
        put_in_category(context, todo_id, category_id)


@when(parsers.re(rf"I put the todo {TITLE} in the category with id (?P<category_id>\d+)"))
def put_todo_in_category(context, title, category_id):
    context.last_response = put_in_category(context, context.todo_id_of(title), category_id)


@when(parsers.re(rf"I take the todo {TITLE} out of the category with id (?P<category_id>\d+)"))
def take_todo_out_of_category(context, title, category_id):
    todo_id = context.todo_id_of(title)
    context.last_response = context.client.delete(f"{context.client.todo_path(todo_id)}/categories/{category_id}")


@when(parsers.re(r"I delete the category with id (?P<category_id>\d+)"))
def delete_category(context, category_id):
    path = constants.CATEGORY_PATH_TEMPLATE.format(category_id=category_id)
    context.last_response = context.client.delete(path)


@when(parsers.re(r"I view the todos of the category with id (?P<category_id>\d+)"))
def view_todos_of_category(context, category_id):
    path = constants.CATEGORY_PATH_TEMPLATE.format(category_id=category_id)
    context.last_response = context.client.get(f"{path}/todos")


@then(parsers.re(rf"the todo {TITLE} (?P<membership>belongs to|does not belong to) the category with id (?P<category_id>\d+)"))
def todo_membership_of_category(context, title, membership, category_id):
    member = category_id in category_ids_of(context, context.todo_id_of(title))
    assert member == (membership == "belongs to"), f"{title!r} {membership} category {category_id} failed"


@then(parsers.re(r"the category with id (?P<category_id>\d+) still exists"))
def category_still_exists(context, category_id):
    path = constants.CATEGORY_PATH_TEMPLATE.format(category_id=category_id)
    assert context.client.get(path).status_code == constants.OK


@then(parsers.re(r"the project with id (?P<project_id>\d+) still exists"))
def project_still_exists(context, project_id):
    assert context.client.get(project_path(project_id)).status_code == constants.OK


@then(parsers.re(rf"the project with id (?P<project_id>\d+) no longer lists the todo {TITLE}"))
def project_no_longer_lists_todo(context, project_id, title):
    project = context.client.get(project_path(project_id)).json()["projects"][0]
    assert {"id": context.todo_id_of(title)} not in project["tasks"]


# helpers

def put_in_category(context, todo_id, category_id):
    return context.client.post_json(f"{context.client.todo_path(todo_id)}/categories", {"id": category_id})


def category_ids_of(context, todo_id):
    response = context.client.get(f"{context.client.todo_path(todo_id)}/categories")
    assert response.status_code == constants.OK, response.text
    return {category["id"] for category in response.json()["categories"]}


def project_path(project_id):
    return constants.PROJECT_PATH_TEMPLATE.format(project_id=project_id)
