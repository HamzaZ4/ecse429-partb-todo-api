# ECSE 429 Part B: story tests for the todo list manager

Author: Hamza Khalfi, 261169045, hamza.khalfi@mail.mcgill.ca

Story tests for the REST API Todo List Manager (`runTodoManagerRestAPI-1.5.5.jar`).
I work alone, so I wrote 5 user stories about todos (and the categories and projects a
todo belongs to). Each story has a normal, an alternate and an error flow, written as
Gherkin scenario outlines in `features/` and run with pytest-bdd (Cucumber's Gherkin for
Python). Part A, the exploratory notes and unit tests, is in a separate repository.

## The stories

| # | Story | Feature file |
|---|-------|--------------|
| 1 | As a user I want to add a todo so that I can keep track of the tasks I still have to do | `add_todo.feature` |
| 2 | As a user I want to look at my todos so that I know what is on my list and what is still open | `view_todos.feature` |
| 3 | As a user I want to mark a todo as done, or reopen it, so that I can see which tasks are finished | `complete_todo.feature` |
| 4 | As a user I want to put a todo in a category so that I can group related tasks together | `categorize_todo.feature` |
| 5 | As a user I want to delete a todo so that my list only holds the tasks I still care about | `delete_todo.feature` |

`service_availability.feature` adds one more scenario outline: a request must fail when
the todo manager is not running.

## Running

Needs Python 3.11+, Java, and port 4567 free. The application jar is not in the repository.

    pip install -r requirements.txt
    export TODO_JAR=/path/to/runTodoManagerRestAPI-1.5.5.jar
    pytest -v

* The tests run in a **random order** (pytest-randomly). The seed is printed at the top of
  each run. `pytest -v -p randomly --randomly-seed=1234` replays an order, and
  `pytest -v -p no:randomly` runs them in file order.
* A story: `pytest tests/test_add_todo.py -v`.
* Expected result: 35 tests, 32 passed and 3 xfailed (the bugs below).

## How a scenario runs

* **Background.** Every feature starts with the same two steps: the todo manager is running
  (the scenario fails if nothing answers on port 4567), and the list holds the 2 default
  todos. The second step also keeps a copy of those 2 todos.
* **Clean start and clean finish.** Each scenario starts its own copy of the jar and shuts
  it down afterwards, so it always starts from the default data and leaves nothing behind.
  This is what lets the scenarios run in any order.
* **Correctness and side effects.** Scenarios check status codes, response bodies and what
  happened to the data. The step "the default todos are unchanged" compares the 2 default
  todos with the copy kept in the Background, so an action that also changes another todo
  is caught.
* **Expected failures.** A scenario tagged `@xfail` describes what the API should do. It
  fails today because of a bug (see `bugs/`), so pytest reports it as an expected failure.
  Once the bug is fixed the scenario passes, pytest reports it as xpassed and the tag
  can be removed.

## Layout

    features/              the Gherkin scenario outlines, one file per story
    tests/step_definitions/  the step definition library, shared by all features
        common_steps.py        background, status codes, error messages, default todos
        todo_steps.py          adding, viewing, completing, deleting todos
        relationship_steps.py  categories and projects of a todo
        scenario_context.py    what the steps of one scenario share
    tests/test_*.py        one line each, binding a feature file to the steps
    todo_api/              the helper package (client, server), as in Part A
    bugs/                  bug reports for bugs found while writing the stories
    conftest.py            starts and stops the application for each scenario

## Bugs found

| Bug | Story | Summary |
|-----|-------|---------|
| `bugs/Bug_06_category_todos_list_is_empty.md` | 4 | GET /categories/:id/todos is empty even when todos are in the category |
| `bugs/Bug_08_deleted_category_still_listed_on_todo.md` | 4 | after DELETE /categories/:id the todos still list the deleted category |
| `bugs/Bug_07_inconsistent_error_message_wording.md` | 3 | the "todo not found" error is worded differently on GET, PUT, DELETE and POST |

The five bugs found in Part A (`Bug_01` to `Bug_05`) are in the Part A repository.
