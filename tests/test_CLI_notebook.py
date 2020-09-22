import importlib_resources
import notebooks

from pytest_notebook.nb_regression import NBRegressionFixture

fixture = NBRegressionFixture(exec_timeout=120)
fixture.diff_color_words = False
fixture.diff_replace = (("/cells/*/outputs", "\\r", ""),)
fixture.diff_ignore = ("/cells/*/execution_count",)


def test_notebook_output():
    with importlib_resources.path(notebooks, "CLI.ipynb") as path:
        result = fixture.check(str(path))
        print(result)
