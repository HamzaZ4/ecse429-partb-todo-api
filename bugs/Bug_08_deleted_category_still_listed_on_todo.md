# Bug 08: a deleted category is still listed on its todos

**Executive summary:** after DELETE /categories/:id the todos still list the deleted category

**Related story:** Story 4, put a todo in a category (scenario "delete a category that has a todo in it")

**Description:** `DELETE /categories/1` answers `200` and the category is gone (`GET /categories/1`
returns `404` and it is not in `GET /categories`). But the todo that was in it still has the
link: `GET /todos/1/categories` returns category 1 and `GET /todos/1` still has
`"categories":[{"id":"1"}]`. Deleting a project works correctly: after `DELETE /projects/1`
the todo no longer lists the project.

**Potential impact:** A todo says it is in a category that does not exist, and the user can't
open or remove that category. A screen that groups todos by category would show a category
that is not in the category list.

**Steps to reproduce:**
1. Start a fresh app. Todo 1 ("scan paperwork") is in category 1 ("Office").
2. `DELETE /categories/1` returns `200`. `GET /categories/1` now returns `404`.
3. `GET /todos/1/categories` still returns category 1. It should be empty.

**Test:** scenario "Alternate flow - delete a category that has a todo in it" in
`features/categorize_todo.feature`, tagged `@xfail` (shows as xfailed).
