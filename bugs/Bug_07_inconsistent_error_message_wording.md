# Bug 07: the "todo not found" error is worded differently on every method

**Executive summary:** unknown todo id gives a different error message on GET, PUT, DELETE and POST

**Related story:** Story 3, "Mark a todo as done" (scenario "the error message for an unknown todo uses the same wording as GET")

**Description:** Asking for a todo that does not exist returns `404` with an error message on
every method, but each method words the message differently:
- `GET /todos/9999`: "Could not find an instance with todos/9999"
- `PUT /todos/9999`: "Invalid GUID for 9999 entity todo"
- `DELETE /todos/9999`: "Could not find any instances with todos/9999"
- `POST /todos/9999` (the call that marks a todo as done): "No such todo entity instance with GUID or ID 9999 found"

**Potential impact:** Low. A client that wants to recognise "this todo does not exist" has to
match four different sentences, and the PUT message does not even say the todo is missing.

**Steps to reproduce:**
1. Start a fresh app.
2. Send GET, PUT, DELETE and POST to `/todos/9999` (the PUT and POST need a JSON body).
3. All four return 404, and the four messages are all different.

**Test:** scenario "Error flow - the error message for an unknown todo uses the same wording as GET"
in `features/complete_todo.feature`, tagged `@xfail`. It is expected to fail, so it is
reported as xfail.
