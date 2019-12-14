from github import Github

from statbus.ext import cache
from statbus.config import config

gh = Github(login_or_token=config.GITHUB_TOKEN)
repo = gh.get_repo(config.GITHUB_REPO)


DEFAULT_LABELS = config.GITHUB_LABELS.split(",")


@cache.memoize()
def get_balance_labels(text=["Needs Balance Review", "Balance/Rebalance"]):
    labels = repo.get_labels()
    return [label for label in labels if label.name in text]


@cache.memoize()
def get_balance_prs(balance_labels=None):
    if balance_labels is None:
        balance_labels = get_balance_labels()
    all_issues = []
    for label in balance_labels:
        all_issues += repo.get_issues(state="open", labels=[label])

    # for issue in all_issues:
    #     print(issue)

    return all_issues
