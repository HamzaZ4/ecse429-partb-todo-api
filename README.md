# ECSE 429 Part B: story tests for the todo list manager

Hamza Khalfi, 261169045, hamza.khalfi@mail.mcgill.ca

Story tests for the REST API Todo List Manager (`runTodoManagerRestAPI-1.5.5.jar`).
I work alone, so I wrote 5 user stories about todos. Each story has a normal, an
alternate and an error flow, written as Gherkin scenario outlines in `features/` and run
with pytest-bdd. Part A is in a separate repository. I built this with help from Claude,
see the "Generative AI usage" section of my report.

## The stories

| # | Story | Feature file |
|---|-------|--------------|
| 1 | As a user I want to add a todo so that I can keep track of the tasks I still have to do | `add_todo.feature` |
| 2 | As a user I want to look at my todos so that I know what is on my list | `view_todos.feature` |
| 3 | As a user I want to mark a todo as done, or reopen it, so that I can see which tasks are finished | `complete_todo.feature` |
| 4 | As a user I want to put a todo in a category so that I can group related tasks together | `categorize_todo.feature` |
| 5 | As a user I want to delete a todo so that my list only holds the tasks I still care about | `delete_todo.feature` |

`service_availability.feature` is one extra scenario: a request has to fail when the todo
manager is not running.

## How to run

You need Python 3.11+, Java, and port 4567 free. The jar is not in the repo.

    pip install -r requirements.txt
    export TODO_JAR=/path/to/runTodoManagerRestAPI-1.5.5.jar
    pytest -v

* The tests run in a random order (pytest-randomly) and the seed is printed at the top.
  `pytest -v -p randomly --randomly-seed=1234` runs the same order again and
  `pytest -v -p no:randomly` runs them in file order.
* One story: `pytest tests/test_add_todo.py -v`
* Expected result: 35 tests, 32 passed and 3 xfailed (the 3 bugs below).

## How the tests work

* Every feature starts with the same Background: the todo manager is running (the test
  fails if nothing answers on port 4567) and the list has the 2 default todos.
* Every scenario starts its own copy of the app and shuts it down at the end, so it always
  starts from the default data. That is why the scenarios can run in any order.
* The scenarios check the status code, the response and what happened to the data. The
  step "the default todos are unchanged" compares the 2 default todos with the copy taken
  in the Background, to catch an action that changes another todo by mistake.
* A scenario tagged `@xfail` says what the API should do, but it fails today because of a
  bug (see `bugs/`), so pytest reports it as an expected failure.

## Files

    features/                the Gherkin scenario outlines, one file per story
    tests/step_definitions/  the step definitions, shared by all features
        common_steps.py          background, status code, error message, default todos
        todo_steps.py            add, view, mark done, delete
        relationship_steps.py    categories and projects
        scenario_context.py      what the steps of one scenario share
    tests/test_*.py          one line each, links a feature file to the steps
    todo_api/                helper code (client, server) from Part A
    bugs/                    bug reports
    conftest.py              starts and stops the app for each scenario

## Bugs

| Bug | Story | Summary |
|-----|-------|---------|
| `bugs/Bug_06_category_todos_list_is_empty.md` | 4 | GET /categories/:id/todos is empty even when todos are in the category |
| `bugs/Bug_07_inconsistent_error_message_wording.md` | 3 | the "todo not found" error is worded differently on GET, PUT, DELETE and POST |
| `bugs/Bug_08_deleted_category_still_listed_on_todo.md` | 4 | after DELETE /categories/:id the todos still list the deleted category |

The five bugs from Part A (Bug_01 to Bug_05) are in the Part A repository.
