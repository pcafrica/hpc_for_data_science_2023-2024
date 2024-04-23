# Unit testing

> A computer program does what you tell it, not what you want.

Tests ensure that your software does what you *want*.
Moreover, tests often *define* what you want, i.e. the set of features provided by a package: since it is only by continuous testing that the developer can ensure all of a growing list of features survive the passage of time (i.e. often chaotic development).

> [!TIP]
> The normalisation "test" → "*unit* test" focuses on each component in your project (usually, each function/method) in an atomistic fashion, suggesting the strategy you should adopt when writing tests.

## [`pytest`](https://docs.pytest.org/): helps you write better programs

Use pytest for all your Python unit-testing needs. Its basic usage is simple:
- You write [test functions](https://docs.pytest.org/en/stable/explanation/goodpractices.html#conventions-for-python-test-discovery): any functions whose name starts with "`test_`" or methods (whose name starts with "`test_`") of classes whose name starts with "`Test`".
- In test functions, you compare the output (return value!) of your code with some usually hard-coded explicit result using [`assert`](https://docs.python.org/3/reference/simple_stmts.html#grammar-token-python-grammar-assert_stmt):
```python
def test_my_function():
    assert your_function(*args, **kwargs) == KNOWN_RESULT
```

### [Parametrisations](https://docs.pytest.org/en/stable/how-to/parametrize.html)

[`mark.parametrize`](https://docs.pytest.org/en/stable/reference/reference.html#pytest.Metafunc.parametrize) is a decorator that executes a given test multiple times with different parameters. Its usage is simple but powerful:
```python
import pytest

@pytest.mark.parametrize('arg1, arg2, answer', (
    (2, math.pi, math.tau),
    (6, 7, 42),
    (6, 9, 42)  # this will fail: see below
))
def test_multiply(arg1, arg2, answer):
    # Test Python's builtin multiply, I guess...
    assert arg1 * arg2 == answer
```
This will be made much more powerful by [Hypothesis](https://en.wikipedia.org/wiki/Hypothesis) (which deserves its own [section](#hypothesis-an-essential-part-of-the-scientific-process)).

### Other [markers](https://docs.pytest.org/en/stable/how-to/mark.html)
#### [Skip](https://docs.pytest.org/en/stable/how-to/skipping.html#skip) ([if](https://docs.pytest.org/en/stable/how-to/skipping.html#id1))
Self-explanatory, no? Follow the links for examples.

#### Expect to fail ([`mark.xfail`](https://docs.pytest.org/en/stable/how-to/skipping.html#xfail))
If you know that a test might fail, you can mark it with `@pytest.mark.xfail`[^xfailparam]. This can be useful if you plan to fix the issue "[later](https://en.wikipedia.org/wiki/Procrastination)" or if the failure occurs only under certain [conditions](https://docs.pytest.org/en/stable/how-to/skipping.html#condition-parameter)[^xfailwhy][^xfailcond]. The test will be run, but if it fails, it will be reported as `XFAIL`, which is usually not bad and will not fail your overall test suite. If it succeeds, though, it will be marked as `XPASS` instead of `PASS`, which is also not bad [by default](https://docs.pytest.org/en/stable/how-to/skipping.html#strict-parameter).

[^xfailparam]: Markers like `xfail` can be applied to single parametrisations as well via [`pytest.param(*args, mark=pytest.mark.xfail)`](https://docs.pytest.org/en/stable/reference/reference.html#pytest-param).

[^xfailwhy]: For example, because some of your tests are only meant to be run locally (use data or packages you don't want to / connot deploy to continuous integration).

[^xfailcond]: You can achieve finer-grained control over expected failures by using [`pytest.xfail`](https://docs.pytest.org/en/stable/reference/reference.html#pytest.xfail) (different from `pytest.mark.xfail`!) from *within* the test-function body.

##### Fail if succeed ([`raises=...`](https://docs.pytest.org/en/stable/how-to/skipping.html#raises-parameter))
A much more useful use-case for `xfail` is to verify that your code fails *in a well-defined graceful way*.[^xfail-no-assert] You can achieve this by passing `raises=EXCEPTION_CLASS` to `mark.xfail`:
```python
@pytest.mark.xfail(raises=h2g2.UnethicalError)
@pytest.mark.parametrize('func', (
    h2g2.demolish_arthurs_house_to_make_way_for_a_new_bypass,
    h2g2.destroy_the_Earth_to_make_way_for_a_new_hyperspace_bypass
))
def test_unethical_funcs(func):
    func()
```
This will `FAIL` your test suite if any of those functions complete without raising an `UnethicalError`. Finer-grained control can be achieved via the [`pytest.raises`](https://docs.pytest.org/en/stable/reference/reference.html#pytest-raises) *context manager*.

[^xfail-no-assert]: This is the only kind of test that doesn't need to use `assert`s.

### [Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Fixtures are supposedly pytest's most powerful feature. Correspondingly, the most complicated.

A [fixture](https://docs.pytest.org/en/stable/explanation/fixtures.html#about-fixtures) is usually a relatively complicated *value* you want to use in (possibly multiple) tests, and as such, it is best defined through a factory function rather than hard coding. A fixture is *requested*[^autouse] simply by [declaring a test-function parameter with the same name](https://docs.pytest.org/en/stable/how-to/fixtures.html#requesting-fixtures).[^fixname] The fixture *value* is then reused (without re-computation) within a predefined [*scope*](https://docs.pytest.org/en/stable/how-to/fixtures.html#fixture-scopes):
- `'function'`: the value is recomputed for every test;
- `'class'`, `'module'`, `'package'`: computed once and reused for tests within a class / module / (sub)package[^package];
- `'session'`: computed once and shared among all tests.

Fixtures can be freely combined with parameters and even [themselves parametrised](https://docs.pytest.org/en/stable/how-to/fixtures.html#parametrizing-fixtures).
Once acquired, they can be used in any context: as inputs/outputs to test functions or even to produce objects to be tested. Here's a complete-ish [example](https://hitchhikers.fandom.com/wiki/Ultimate_Question):

```python
import h2g2  # that's our package!

# this runs for 7.5 million years
# but then can be reused throughout all tests
@pytest.fixture(scope='session')
def answer():
    # BTW, you should separately test that deep_thought.answer()
    # gives results as expected.
    return h2g2.deep_though.answer()


# Here the `answer` parameter receives the fixture value
def test_scrabble(answer):
    assert h2g2.what_do_you_get_if_you_multiply_six_by_nine() == answer

    
class TestMice:
    @pytest.fixture(scope='class')
    def brain(self):
        # Prepare Arthur's brain for examination
        # Executed once for all tests in the class
        return h2g2.Brain('Arthur')

    @pytest.mark.parametrize('question', (
        'How many roads must a man walk down?',
        'Given the answer 42, what are all possible permutations of questions which give rise to this answer?'
    ))
    def test_brain(self, brain, question, answer):
        assert brain.ask(question) == answer
```

[^autouse]: Fixtures can be computed even if not requested—e.g. to set up some directories or other environment—by specifying [`autouse=True`](https://docs.pytest.org/en/stable/how-to/fixtures.html#autouse-fixtures-fixtures-you-don-t-have-to-request).

[^fixname]: This is kind of annoying because the connection between function parameters and the fixture factories is not immediately obvious. However, modern IDEs have learned to recognise patterns and can clarify this for you.

[^package]: Here module/package refers to a module/package *of tests*, i.e. files/folders within your test directory.

## Plugins and extensions

### [`hypothesis`](https://hypothesis.readthedocs.io/): an essential part of the scientific process

COMING SOON

### [Coverage](https://coverage.readthedocs.io/) and [`pytest-cov`](https://pytest-cov.readthedocs.io/)

COMING LATER
