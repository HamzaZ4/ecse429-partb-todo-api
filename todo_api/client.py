import json

import requests

from todo_api import constants


class TodoApiClient:
    def send(self, method, path, headers=None, body=None):
        return requests.request(
            method,
            constants.BASE_URL + path,
            headers=headers,
            data=body,
            timeout=constants.REQUEST_TIMEOUT_SECONDS,
        )

    def get(self, path):
        return self.send("GET", path)

    def delete(self, path):
        return self.send("DELETE", path)

    def post_json(self, path, payload):
        return self.send("POST", path, headers=constants.JSON_HEADERS, body=json.dumps(payload))

    def send_xml(self, method, path, xml_text):
        return self.send(method, path, headers=constants.XML_HEADERS, body=xml_text)

    def post_raw(self, path, content_type, body):
        return self.send("POST", path, headers={"Content-Type": content_type}, body=body)

    def create_todo(self, title):
        # many scenarios just need a todo to exist first, so the check is done here
        response = self.post_json(constants.TODOS_PATH, {"title": title})
        assert response.status_code == constants.CREATED, response.text
        return response.json()

    def get_todo(self, todo_id):
        return self.get(self.todo_path(todo_id))

    def todo_path(self, todo_id):
        return f"{constants.TODOS_PATH}/{todo_id}"
