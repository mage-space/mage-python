"""Live smoke test against the Mage API.

Spends gems: runs the cheapest image model once. Needs MAGE_API_KEY (and MAGE_BASE_URL
to aim at another host).
"""

from __future__ import annotations

import httpx

from mage_space import Mage

PROMPT = "A small red cube on a white table, soft studio light"


def main() -> None:
    with Mage() as mage:
        before = mage.account.get()["gems"]["balance"]
        images = [a for a in mage.architectures.list()["architectures"] if a["type"] == "image"]
        cheapest = min(images, key=lambda architecture: architecture["gems"])
        print(f"Balance: {before} gems. Running {cheapest['id']} ({cheapest['gems']} gems).")

        request = mage.run(cheapest["id"], {"prompt": PROMPT}, timeout=600)
        result = request["result"]
        assert result is not None, "A completed request has a result"
        download = httpx.get(result["url"], timeout=60, follow_redirects=True)
        download.raise_for_status()

        after = mage.account.get()["gems"]["balance"]
        print(f"OK: {result['url']} ({len(download.content)} bytes). Spent {before - after} gems.")


if __name__ == "__main__":
    main()
