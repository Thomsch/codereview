import requests


def get_pr_diff(pull_request_url: str) -> str:
    """
    Retrieves the diff of a pull request from Github.
    :param pull_request_url: URL of the pull request in format github.com/owner/repo/pull/number
    :return: Diff of the pull request
    """

    response = requests.get(pull_request_url + ".diff")
    if response.status_code != 200:
        raise ValueError(f"Could not retrieve diff from Github: {response.reason} ({response.status_code})")
    return response.text
