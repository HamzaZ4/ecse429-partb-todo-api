# Bug 07: the "todo not found" message is different on every method

**Executive summary:** unknown todo id gives a different error message on GET, PUT, DELETE and POST

**Related story:** Story 3, mark a todo as done (scenario "the error message for an unknown todo uses the same wording as GET")

**Description:** For a todo id that does not exist (like 9999) all four methods return `404`
with a message, but the message is different each time:
- `GET /todos/9999`: "Could not find an instance with todos/9999"
- `PUT /todos/9999`: "Invalid GUID for 9999 entity todo"
- `DELETE /todos/9999`: "Could not find any instances with todos/9999"
- `POST /todos/9999` (used to mark a todo as done): "No such todo entity instance with GUID or ID 9999 found"

**Potential impact:** Low. A client that wants to know that the todo does not exist has to
check four different sentences. The PUT message does not even say the todo is missing.

**Steps to reproduce:**
1. Start a fresh app.
2. Send GET, PUT, DELETE and POST to `/todos/9999` (PUT and POST need a JSON body).
3. All four return 404 and the four messages are different.

**Test:** scenario "Error flow - the error message for an unknown todo uses the same wording as GET"
in `features/complete_todo.feature`, tagged `@xfail` (shows as xfailed).
