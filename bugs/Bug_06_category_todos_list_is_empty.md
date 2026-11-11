# Bug 06: GET /categories/:id/todos is always empty

**Executive summary:** GET /categories/:id/todos is empty even when todos are in the category

**Related story:** Story 4, put a todo in a category (scenario "see which todos are in a category")

**Description:** A todo can be put in a category and the todo then shows the category
(`GET /todos/1/categories` returns category 1). The docs say `GET /categories/:id/todos`
returns the todos of a category, but it always answers `200` with `{"todos": []}`. The other
direction works for projects: `GET /projects/1/tasks` lists the todos of the project.

**Potential impact:** A user cannot see which todos are in a category. The only way is to
read every todo and look at its categories. A client that trusts the empty answer would
show an empty category and might let the user delete it.

**Steps to reproduce:**
1. Start a fresh app. Todo 1 ("scan paperwork") is in category 1 ("Office").
2. `GET /todos/1/categories` returns category 1.
3. `GET /categories/1/todos` returns `200 {"todos":[]}`. It should list todo 1.

**Test:** scenario "Alternate flow - see which todos are in a category" in
`features/categorize_todo.feature`, tagged `@xfail` (shows as xfailed).
