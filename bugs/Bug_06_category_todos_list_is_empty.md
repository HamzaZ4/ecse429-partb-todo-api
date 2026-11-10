# Bug 06: GET /categories/:id/todos returns nothing for a category that has todos

**Executive summary:** GET /categories/:id/todos is empty even when todos are in the category

**Related story:** Story 4, "Put a todo in a category" (scenario "see which todos are in a category")

**Description:** A todo can be put in a category, and the todo then lists the category
(`GET /todos/1/categories` returns category 1). The path `/categories/:id/todos` is in the
swagger docs, so a user expects it to list the todos of that category. It always answers
`200` with `{"todos": []}`. The other direction works: `GET /projects/1/tasks` lists the
project's todos.

**Potential impact:** A user cannot find out which todos belong to a category. The only way
is to read every todo and look at its `categories`. A client that trusts the empty answer
shows an empty category and may offer to delete it.

**Steps to reproduce:**
1. Start a fresh app. Todo 1 ("scan paperwork") is in category 1 ("Office").
2. `GET /todos/1/categories` returns category 1.
3. `GET /categories/1/todos` returns `200 {"todos":[]}`. It should list todo 1.

**Test:** scenario "Alternate flow - see which todos are in a category" in
`features/categorize_todo.feature`, tagged `@xfail`. It is expected to fail, so it is
reported as xfail.
