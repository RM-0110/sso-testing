import json
import os
from datetime import datetime


def write_result(
    browser,
    status,
    error=None,
):
    os.makedirs(
        "results",
        exist_ok=True,
    )

    result = {
        "browser": browser,
        "status": status,
        "error": error,
        "timestamp": datetime.utcnow().isoformat(),
        "workflow": os.getenv("GITHUB_WORKFLOW"),
        "run_id": os.getenv("GITHUB_RUN_ID")
    }

    with open(
        f"results/{browser}.json",
        "w",
    ) as f:
        json.dump(
            result,
            f,
            indent=2,
        )

    print(
        f"[RESULT] {browser}: {status}"
    )
