import importlib_resources
from pytest_notebook.nb_regression import NBRegressionFixture

import notebooks

fixture = NBRegressionFixture(exec_timeout=300)
fixture.diff_color_words = False
fixture.diff_replace = (("/cells/*/outputs", "\\r", ""),)
# ignoring some output cells,
# because pd.DataFrame.value_counts' return value is inconsistent
fixture.diff_ignore = (
    "/cells/*/execution_count",
    "/metadata/language_info/version",
    "/cells/68/outputs/0/text",
    "/cells/69/outputs/0/text",
    "/cells/78/outputs/0/text",
    "/cells/134/outputs/0/text",
    "/cells/135/outputs/0/text",
    "/cells/136/outputs/0/text",
)


def cli_notebook_output():
    with importlib_resources.path(notebooks, "CLI.ipynb") as path:
        fixture.check(str(path))
