#!/usr/bin/env python3
"""Track a delivery app price at a fixed interval (default: 10 minutes)."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone


def fetch_price(url: str, timeout: float) -> float:
    """Fetch the current price from a JSON endpoint containing a 'price' field."""
    with urllib.request.urlopen(url, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))

    if "price" not in payload:
        raise ValueError("Response JSON must include a 'price' field")

    return float(payload["price"])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Track delivery app prices every 10 minutes by default."
    )
    parser.add_argument("url", help="JSON endpoint returning a 'price' field")
    parser.add_argument(
        "--interval-minutes",
        type=float,
        default=10,
        help="Polling interval in minutes (default: 10)",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=10,
        help="Request timeout in seconds (default: 10)",
    )
    args = parser.parse_args()

    if args.interval_minutes <= 0:
        raise ValueError("--interval-minutes must be greater than 0")

    interval_seconds = args.interval_minutes * 60
    previous_price: float | None = None

    while True:
        timestamp = datetime.now(timezone.utc).isoformat()
        try:
            current_price = fetch_price(args.url, timeout=args.timeout_seconds)
            if previous_price is None:
                change_message = "(initial reading)"
            else:
                delta = current_price - previous_price
                sign = "+" if delta >= 0 else ""
                change_message = f"(change: {sign}{delta:.2f})"

            print(f"[{timestamp}] price={current_price:.2f} {change_message}")
            previous_price = current_price
        except (urllib.error.URLError, ValueError, json.JSONDecodeError) as error:
            print(f"[{timestamp}] failed to fetch price: {error}")

        time.sleep(interval_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
