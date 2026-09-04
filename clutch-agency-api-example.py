"""
Clutch.co Agency API: A Quick Start Example
See more at: https://apify.com/johnvc/clutch-agency-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/clutch-agency-api/input-schema?fpr=9n7kx3

This script shows how to call the Clutch.co Agency API on Apify from Python and
read its structured JSON output. It is a company data API for Clutch.co, the B2B
directory of agencies and service providers: pull directory listings, full
company profiles, and every verified client review, as JSON plus LLM-ready
markdown.

The default run stays cheap on purpose (one directory page, a small row cap).
The three helpers below map to the Actor's three modes so you can see its range.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3

Examples:
  uv run python clutch-agency-api-example.py
  uv run python clutch-agency-api-example.py --example directory
  uv run python clutch-agency-api-example.py --example profiles
  uv run python clutch-agency-api-example.py --example search
"""

from __future__ import annotations

import argparse
import os
from typing import Any

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR_ID = "johnvc/clutch-agency-api"


def _print_items(items: list[dict[str, Any]]) -> None:
    """Print a short, readable summary of the dataset rows.

    Every row carries a `result_type` of listing, profile, review, or error.
    """
    print(f"Returned {len(items)} row(s).\n")
    for item in items:
        rt = item.get("result_type")
        if rt == "listing":
            print(f"[listing] {item.get('name')} | {item.get('rating')} "
                  f"({item.get('review_count')} reviews) | {item.get('location')} "
                  f"| {item.get('min_project_size')} | {item.get('hourly_rate')}")
        elif rt == "profile":
            print(f"[profile] {item.get('name')} | {item.get('rating')} stars "
                  f"| {item.get('employees')} staff | founded {item.get('founded_year')} "
                  f"| {item.get('website')}")
        elif rt == "review":
            print(f"[review]  {item.get('company_name')}: \"{item.get('title')}\" "
                  f"| {item.get('rating')} | {item.get('project_size')}")
        else:
            print(f"[{rt}] {item}")


def run_default(client: ApifyClient) -> None:
    """Cheap general quick-start: one directory page, a small row cap.

    Inputs are kept small so this first run is inexpensive. Raise `maxItems` and
    `maxPagesPerDirectory` once you have your own API key and know your budget.
    """
    run_input: dict[str, Any] = {
        "mode": "directory",
        "directoryUrls": ["https://clutch.co/web-developers"],
        "maxPagesPerDirectory": 1,
        "maxItems": 10,
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_directory(client: ApifyClient) -> None:
    """Directory mode: walk a Clutch category page into one row per company.

    This is how you build a marketing agency database or a list of digital
    marketing agencies for a category or location. Swap in any Clutch directory
    URL, for example https://clutch.co/us/agencies/digital-marketing/chicago .
    """
    run_input: dict[str, Any] = {
        "mode": "directory",
        "directoryUrls": ["https://clutch.co/agencies/digital-marketing"],
        "maxPagesPerDirectory": 1,   # one page is ~70-90 companies; raise to go deeper
        "maxItems": 20,
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_profiles(client: ApifyClient) -> None:
    """Profiles mode: full company records plus verified client reviews.

    Each profile carries ratings, pricing, service mix, industries, locations,
    and Clutch's own LLM-ready markdown. Reviews come back as their own rows.
    A bare slug works in place of a full profile URL.
    """
    run_input: dict[str, Any] = {
        "mode": "profiles",
        "profileUrls": ["ignite-visibility"],
        "includeReviews": True,
        "maxReviewsPerProfile": 5,   # small on purpose to keep the run cheap
        "outputFormats": ["json", "markdown"],
        "maxItems": 10,
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_search(client: ApifyClient) -> None:
    """Search mode: a keyword query, then the matching company profiles.

    Good for shortlisting B2B service providers by what they do rather than by a
    directory URL.
    """
    run_input: dict[str, Any] = {
        "mode": "search",
        "searchQueries": ["shopify development"],
        "includeReviews": False,
        "maxItems": 5,
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


EXAMPLES = {
    "default": run_default,
    "directory": run_directory,
    "profiles": run_profiles,
    "search": run_search,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Clutch.co Agency API example client.")
    parser.add_argument(
        "--example",
        choices=sorted(EXAMPLES),
        default="default",
        help="Which example to run (default: default).",
    )
    args = parser.parse_args()

    token = os.getenv("APIFY_API_TOKEN")
    if not token or token == "your_apify_api_token_here":
        raise SystemExit(
            "Set APIFY_API_TOKEN in your environment or a .env file. "
            "Get a free token at https://apify.com?fpr=9n7kx3"
        )

    client = ApifyClient(token)
    EXAMPLES[args.example](client)


if __name__ == "__main__":
    main()
