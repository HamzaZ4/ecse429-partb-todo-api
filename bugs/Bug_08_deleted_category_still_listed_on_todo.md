# Bug 08: a deleted category is still listed on the todos that were in it

**Executive summary:** after DELETE /categories/:id the todos still list the deleted category

**Related story:** Story 4, "Put a todo in a category" (scenario "delete a category that has a todo in it")

**Description:** Deleting a category answers `200` and the category is gone (`GET /categories/1`
returns `404` and it is missing from `GET /categories`). But the todos that were in it keep the
link: `GET /todos/1/categories` still returns category 1 and `GET /todos/1` still has
`"categories":[{"id":"1"}]`. Deleting a project behaves correctly: after `DELETE /projects/1`
the todo no longer lists the project in `tasksof`.

**Potential impact:** A todo claims to belong to a category that does not exist, and the client
cannot open, rename or remove that category. Any screen that groups todos by category shows a
category that is not in the category list. The data stays inconsistent until the todo is deleted.

**Steps to reproduce:**
1. Start a fresh app. Todo 1 ("scan paperwork") is in category 1 ("Office").
2. `DELETE /categories/1` returns `200`. `GET /categories/1` now returns `404`.
3. `GET /todos/1/categories` still returns category 1. Expected: an empty list.

**Test:** scenario "Alternate flow - delete a category that has a todo in it" in
`features/categorize_todo.feature`, tagged `@xfail`. It is expected to fail, so it is
reported as xfail.
