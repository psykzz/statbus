from flask import current_app
from github import Github

from statbus.ext import cache
from statbus.config import config


gh, repo = None, None
try:
    gh = Github(login_or_token=config.GITHUB_TOKEN)
    repo = gh.get_repo(config.GITHUB_REPO)
except:
    print("Unable to create github instance")
    pass

DEFAULT_LABELS = config.GITHUB_LABELS.split(",")


@cache.memoize()
def get_balance_labels(text=["Needs Balance Review", "Balance/Rebalance"]):
    if not repo:
        return []
    labels = repo.get_labels()
    return [label for label in labels if label.name in text]


@cache.memoize()
def get_balance_prs(testmerged_prs, balance_labels=None):
    if balance_labels is None:
        balance_labels = get_balance_labels()
    all_issues = []
    for label in balance_labels:
        all_issues += repo.get_issues(state="open", labels=[label])
        all_issues += repo.get_issues(state="closed", labels=[label])

    # Filter down issues based on the current round
    pr_ids = set([int(tm.get("number")) for tm in testmerged_prs])
    full_prs = []
    for issue in all_issues:
        if issue.number in pr_ids:
            full_prs.append(issue)
    return full_prs
