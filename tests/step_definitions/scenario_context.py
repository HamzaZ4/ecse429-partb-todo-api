# what the steps of one scenario share
class ScenarioContext:

    def __init__(self, client):
        self.client = client
        self.last_response = None
        self.request_failed = None
        self.default_todos = None
        self.todo_ids_by_title = {}

    def remember_todo(self, title, todo_id):
        self.todo_ids_by_title[title] = todo_id

    def todo_id_of(self, title):
        return self.todo_ids_by_title[title]
