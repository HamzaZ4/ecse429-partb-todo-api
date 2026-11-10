import pytest

from todo_api.client import TodoApiClient
from todo_api.server import TodoServer, resolve_jar_path
from tests.step_definitions.scenario_context import ScenarioContext

pytest_plugins = [
    "tests.step_definitions.common_steps",
    "tests.step_definitions.todo_steps",
    "tests.step_definitions.relationship_steps",
]


# new app before every scenario and shut down after, so each one starts clean
@pytest.fixture(autouse=True)
def running_server(request):
    if request.node.get_closest_marker("service_down"):
        yield  # this scenario needs the app to be off
        return
    server = TodoServer(resolve_jar_path())
    server.start()
    yield
    server.stop()


@pytest.fixture
def client():
    return TodoApiClient()


@pytest.fixture
def context(client):
    return ScenarioContext(client)
