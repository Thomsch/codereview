import pytest

from app.github_api import get_pr_diff


def test_get_pr():
    diff = get_pr_diff("https://github.com/PyGithub/PyGithub/pull/664")
    assert diff is not None


def test_nonexistent_pr():
    with pytest.raises(ValueError) as e:
        diff = get_pr_diff("https://github.com/PyGithub/PyGithub/pull/999999")
        assert e.value == "Could not retrieve diff from Github: Not Found (404)"
