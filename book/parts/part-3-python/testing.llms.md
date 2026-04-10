# 17  Testing Basics with pytest

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks), [sec-debugging](#sec-debugging).
>
> **See also:** [sec-tracebacks](#sec-tracebacks), [sec-git-github](#sec-git-github), [sec-automation](#sec-automation).

## Purpose

If you have ever “fixed” a bug and then broken something else, or changed a function and crossed your fingers, or wondered whether your cleaned data really matches the raw data after a refactor — you were doing the work that tests are designed to do for you automatically.

A **test** is a tiny piece of code that calls another piece of code with known inputs and checks that the output is what you expect. Tests do two jobs at once: they tell you whether your code is currently correct, and they warn you when a later change breaks something that used to work (a *regression*). For a data scientist, that second job is often the more valuable one: you do not have the mental bandwidth to re-verify every analysis step every time you change a helper function, and tests do it for you.

This chapter teaches you enough `pytest` to start writing useful tests for data work: what a test looks like, how to run them, how to test the pandas operations that make up most of your real code, and how to use tests to lock in a bug fix so it cannot come back. It is not a comprehensive software testing course — that can fill a whole book — but it covers the practices a novice data scientist will actually use in a first programming course.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain what a test is, what a test suite is, and why tests matter for data work.
2.  Write a pytest test function, run it from the command line, and read the pass/fail output.
3.  Use `assert` to check values, with a clear message when the assertion fails.
4.  Write assertions specific to pandas DataFrames: shape, column names, dtypes, and value ranges.
5.  Use a pytest fixture to share setup code across multiple tests.
6.  Use parametrization to run the same test against many inputs without duplication.
7.  Use “bug-reproducing tests” to turn a debugging session into permanent regression protection.
8.  Know when testing matters a lot, when it matters a little, and when it does not matter.

## Running theme: a test is just a question your code answers every time you run it

Every test is a small, precise question: “given this input, does this function return this output?” Writing a test forces you to state the question; running the test asks it; the answer is the pass/fail line in the terminal.

## 17.1 1. What a test actually is

A test is a function that:

1.  Arranges some input.
2.  Calls the code under test.
3.  Asserts something about the result.

That is it. In Python with pytest, a test looks like:

``` python
# test_stats.py
from mymodule.stats import mean

def test_mean_of_empty_list_is_zero():
    assert mean([]) == 0

def test_mean_of_small_list():
    assert mean([1, 2, 3, 4]) == 2.5
```

Notice the conventions:

- The file name starts with `test_`.
- Each test function name starts with `test_`.
- Each test uses the built-in `assert` statement to check a condition. If the condition is true, the test passes; if it is false, the test fails and pytest prints the reason.

Run the whole suite with:

``` bash
pytest
```

You will see output like:

    collected 2 items

    test_stats.py ..                                                  [100%]

    ======================== 2 passed in 0.02s =========================

Each `.` is a passed test. An `F` is a failure; an `E` is a test that errored before it could even make an assertion (a broken test, usually a typo or import error).

## 17.2 2. Installing and running pytest

``` bash
python -m pip install pytest
```

Run all tests from the project root:

``` bash
pytest
```

Run just one file:

``` bash
pytest tests/test_stats.py
```

Run just one test:

``` bash
pytest tests/test_stats.py::test_mean_of_small_list
```

Get more verbose output (useful when you want to see each test name):

``` bash
pytest -v
```

Run tests whose name matches a substring (great during focused debugging):

``` bash
pytest -k "mean and not empty"
```

By default pytest auto-discovers any file matching `test_*.py` or `*_test.py` in the current directory tree, and inside those files, any function starting with `test_`. You do not need a config file to get started.

## 17.3 3. Writing a good assertion

`assert` takes any boolean expression. When it is false, pytest reports the failing expression and the values that went into it.

``` python
def test_addition_works():
    x = 2
    y = 3
    assert x + y == 5
```

If the assertion ever fails, pytest would show:

        def test_addition_works():
            x = 2
            y = 3
    >       assert x + y == 5
    E       assert (2 + 3) == 5

    test_addition.py:4: AssertionError

A few guidelines:

- **One clear thing per test.** A test called `test_mean_of_small_list` should test only the mean of a small list. If you want to also check the empty list case, write a second test.
- **Name the test after the behavior.** `test_mean_handles_empty_list` is more useful than `test_mean_2` because the name alone tells you what broke when the test fails.
- **Prefer simple built-in comparisons** (`==`, `in`, `<`) over complicated constructions. If you can’t compare directly, use `pytest.approx` for floats and the pandas helpers below for DataFrames.

**Float equality** deserves its own bullet. Never write `assert 0.1 + 0.2 == 0.3` — floating-point arithmetic will bite you. Use `pytest.approx`:

``` python
from pytest import approx

def test_sum_of_floats():
    assert 0.1 + 0.2 == approx(0.3)
```

## 17.4 4. Testing pandas code

Most real data-science bugs live in pandas operations: the column was renamed, the dtype changed, a merge produced duplicates, a filter silently dropped every row. Here are the assertions that catch each.

**Shape:**

``` python
def test_cleaned_df_has_expected_shape():
    df = clean_sales(raw_sales)
    assert df.shape == (1000, 5)
```

**Column names:**

``` python
def test_cleaned_df_has_expected_columns():
    df = clean_sales(raw_sales)
    assert list(df.columns) == ["date", "store", "sku", "quantity", "revenue"]
```

**Dtypes** (catches the “why is my numeric column suddenly strings” class of bug):

``` python
def test_revenue_is_numeric():
    df = clean_sales(raw_sales)
    assert df["revenue"].dtype.kind in "if"   # integer or float
```

**No missing values** where you do not expect them:

``` python
def test_dates_are_not_missing():
    df = clean_sales(raw_sales)
    assert df["date"].notna().all()
```

**Value range sanity checks:**

``` python
def test_quantities_are_positive():
    df = clean_sales(raw_sales)
    assert (df["quantity"] > 0).all()
```

**Exact DataFrame equality** (rare but sometimes you want to pin a whole transformation):

``` python
import pandas as pd
from pandas.testing import assert_frame_equal

def test_small_transform_matches_gold():
    result = clean_sales(pd.DataFrame({"raw": [1, 2, 3]}))
    expected = pd.DataFrame({"cleaned": [1, 2, 3]})
    assert_frame_equal(result, expected)
```

`pandas.testing.assert_frame_equal` handles dtype and index comparison correctly; plain `==` does not.

## 17.5 5. Fixtures: sharing setup between tests

A fixture is a function decorated with `@pytest.fixture` that returns a value. Tests that need that value take it as an argument, and pytest wires everything up.

``` python
import pytest
import pandas as pd

@pytest.fixture
def raw_sales():
    return pd.DataFrame({
        "date": ["2024-01-01", "2024-01-02"],
        "sku": ["A", "B"],
        "revenue": [10.0, 20.0],
    })

def test_cleaned_preserves_row_count(raw_sales):
    cleaned = clean_sales(raw_sales)
    assert len(cleaned) == 2

def test_cleaned_adds_year_column(raw_sales):
    cleaned = clean_sales(raw_sales)
    assert "year" in cleaned.columns
```

Both tests got their own fresh copy of `raw_sales` automatically. No copy-pasting setup code. Fixtures are the single biggest productivity boost in pytest once you have more than three tests.

Put shared fixtures in `tests/conftest.py` — pytest finds them automatically, and they become available to every test file in the same directory tree.

## 17.6 6. Parametrization: one test, many inputs

When you want to test the same logic against a handful of inputs, use `@pytest.mark.parametrize` instead of writing a test function per case.

``` python
import pytest
from mymodule.stats import mean

@pytest.mark.parametrize("xs,expected", [
    ([], 0),
    ([5], 5),
    ([1, 2, 3], 2),
    ([1.0, 2.0, 3.0, 4.0], 2.5),
])
def test_mean(xs, expected):
    assert mean(xs) == expected
```

pytest runs the body four times, once per row. If the third row fails, the output tells you exactly which parameters caused the failure.

## 17.7 7. Bug-reproducing tests: the regression lock

The highest-value tests you write in your first year will almost all come from bugs you just fixed. The workflow is:

1.  A user (or you) hits a bug.
2.  You narrow it down to a minimal reproducible example (see [sec-debugging](#sec-debugging)).
3.  **Before you fix anything, write a test that reproduces the bug.** The test will fail.
4.  Now fix the bug. The test passes.
5.  Commit both the fix and the test together.

From then on, that test is a tripwire. If someone ever reintroduces the same bug — by refactoring, by updating pandas, by “cleaning up” the fix — the test fails immediately and they know exactly what broke.

This is the single most useful habit you can form from this chapter. Every time you fix a bug, write the test that would have caught it. You will end up with a regression suite that maps exactly to the real failure modes of your project.

## 17.8 8. When to test (and when not to)

Not every line of code deserves a test. A good rule of thumb for course work:

**Test:**

- Functions that transform data (cleaning, joining, aggregating).
- Functions that you and your collaborators will call from multiple places.
- Anything where you just fixed a bug (write the regression test).
- Schema invariants: “this CSV always has these columns with these dtypes.”

**Do not bother testing:**

- One-off exploration in a notebook.
- Plots (visual output is hard to assert on usefully).
- Code that only exists for five minutes during a quick analysis.
- Library internals (trust pandas to handle `.merge` correctly; test *your* merge results, not pandas’).

The fastest way to get value out of testing is to pick one or two key functions in a project and cover those well, not to chase 100% coverage on everything. See [sec-project-management](#sec-project-management) for how this fits into a project’s overall quality gates.

## 17.9 9. Worked examples

### Example 1: locking in a data-cleaning bug fix

Your CSV cleaning function was silently dropping rows where the price had a leading dollar sign. You fixed it, but you want to make sure the fix stays fixed.

``` python
# tests/test_clean.py
import pandas as pd
from mymodule.clean import clean_sales

def test_clean_keeps_dollar_sign_prices():
    raw = pd.DataFrame({
        "sku": ["A", "B", "C"],
        "price": ["10.00", "$20.00", "15.00"],
    })
    cleaned = clean_sales(raw)
    assert len(cleaned) == 3           # no rows dropped
    assert cleaned["price"].tolist() == [10.0, 20.0, 15.0]
```

This test fails before the fix and passes after. It stays in the suite forever as a silent guard.

### Example 2: a fixture for schema validation

``` python
# tests/conftest.py
import pytest
import pandas as pd

@pytest.fixture
def sales():
    return pd.read_csv("tests/data/sample_sales.csv")

# tests/test_schema.py
EXPECTED_COLUMNS = ["date", "store", "sku", "quantity", "revenue"]

def test_sales_has_expected_columns(sales):
    assert list(sales.columns) == EXPECTED_COLUMNS

def test_sales_has_no_null_dates(sales):
    assert sales["date"].notna().all()

def test_sales_quantities_are_positive(sales):
    assert (sales["quantity"] > 0).all()
```

Three independent schema checks, each with a clear failure message, all driven by a single fixture.

### Example 3: parametrized unit converter

``` python
import pytest
from mymodule.units import fahrenheit_to_celsius

@pytest.mark.parametrize("f,c", [
    (32, 0),
    (212, 100),
    (-40, -40),
    (98.6, 37),
])
def test_fahrenheit_to_celsius(f, c):
    assert fahrenheit_to_celsius(f) == pytest.approx(c, abs=0.1)
```

Four tests for the price of one function.

## 17.10 10. Templates

**A minimal `tests/` directory next to your source:**

    my-project/
    ├── mymodule/
    │   ├── __init__.py
    │   └── clean.py
    └── tests/
        ├── conftest.py
        ├── data/
        │   └── sample_sales.csv
        └── test_clean.py

**A skeleton test file:**

``` python
# tests/test_<module>.py
import pytest
from mymodule.<module> import <function_under_test>

def test_<behavior_being_verified>():
    # Arrange
    input_data = ...
    expected = ...
    # Act
    result = <function_under_test>(input_data)
    # Assert
    assert result == expected
```

## 17.11 11. Exercises

1.  Write a test for the `mean` function from section 1 that checks that `mean([1, 2, 3])` returns `2`. Run `pytest`. Now change the function to return `2 * sum(xs) / len(xs)` (a bug) and rerun. Read the failure.
2.  Pick a function in one of your own projects that transforms data. Write three tests for it: shape, column names, and one value-level assertion.
3.  Use `pytest.mark.parametrize` to test `fahrenheit_to_celsius` at five different inputs, including a negative temperature.
4.  Create a fixture in `conftest.py` that loads a small sample CSV, and use it in at least two tests in different test files.
5.  Find a bug in your own code that you recently fixed. Write the regression test that would have caught it. Run the test against the old (buggy) version and confirm it fails, then against the fixed version and confirm it passes.
6.  Run `pytest -v` and observe the difference from plain `pytest`. Try `pytest -x` to stop on the first failure. Try `pytest --lf` to re-run only the tests that failed last time.
7.  Add a `pytest` invocation to a CI workflow (see [sec-automation](#sec-automation)). Intentionally break one test and confirm the CI build fails.

## 17.12 12. One-page checklist

- Files named `test_*.py`, functions named `test_*`.
- One behavior per test; name tests after what they check.
- Use plain `assert`; use `pytest.approx` for floats and `assert_frame_equal` for DataFrames.
- Put shared setup in `@pytest.fixture` functions, ideally in `conftest.py`.
- Use `@pytest.mark.parametrize` when the same logic needs multiple inputs.
- Every bug you fix becomes a regression test.
- Run `pytest` before every commit; wire `pytest` into your CI pipeline.
- Do not aim for 100% coverage in course work; cover the functions that matter most.
- If a test is hard to write, your function is probably doing too much — split it.
