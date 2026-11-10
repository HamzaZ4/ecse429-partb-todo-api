BASE_URL = "http://localhost:4567"
REQUEST_TIMEOUT_SECONDS = 5
SERVER_START_TIMEOUT_SECONDS = 15
SERVER_STOP_TIMEOUT_SECONDS = 5

JAR_ENVIRONMENT_VARIABLE = "TODO_JAR"
JAR_FILE_NAME = "runTodoManagerRestAPI-1.5.5.jar"

TODOS_PATH = "/todos"
PROJECT_PATH_TEMPLATE = "/projects/{project_id}"
CATEGORY_PATH_TEMPLATE = "/categories/{category_id}"

JSON_CONTENT_TYPE = "application/json"
XML_CONTENT_TYPE = "application/xml"

JSON_HEADERS = {"Content-Type": JSON_CONTENT_TYPE, "Accept": JSON_CONTENT_TYPE}
XML_HEADERS = {"Content-Type": XML_CONTENT_TYPE, "Accept": XML_CONTENT_TYPE}

OK = 200
CREATED = 201
NOT_FOUND = 404

DEFAULT_TODO_TITLES = ("scan paperwork", "file paperwork")
