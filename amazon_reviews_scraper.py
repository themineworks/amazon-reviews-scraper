#!/usr/bin/env python3
"""Star rating, verified badge, full text and review images by ASIN, across 8 marketplaces. Python, Node.js and cURL clients for the Amazon Reviews Scraper on Apify, pay per result.

Command-line client for the themineworks/amazon-reviews actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/amazon-reviews/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/amazon-reviews"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--asins", help="Comma-separated. Amazon ASINs or full product URLs")
    ap.add_argument("--marketplace", help="Amazon marketplace domain")
    ap.add_argument("--max-reviews", type=int, help="Upper limit on reviews returned per ASIN")
    ap.add_argument("--sort-by", help="Order of the returned reviews")
    ap.add_argument("--filter-by-star", help="Keep only reviews with this star rating")
    ap.add_argument("--include-international", action=argparse.BooleanOptionalAction, help="Amazon shows a 'reviews from other countries' block on most listings, typically 5 of the…")
    ap.add_argument("--residential-fallback", action=argparse.BooleanOptionalAction, help="Retry on a residential IP when the standard proxy is blocked, or when Amazon returns a…")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.asins: run_input["asins"] = [s.strip() for s in a.asins.split(",") if s.strip()]
    if a.marketplace is not None: run_input["marketplace"] = a.marketplace
    if a.max_reviews is not None: run_input["maxReviews"] = a.max_reviews
    if a.sort_by is not None: run_input["sortBy"] = a.sort_by
    if a.filter_by_star is not None: run_input["filterByStar"] = a.filter_by_star
    if a.include_international is not None: run_input["includeInternational"] = a.include_international
    if a.residential_fallback is not None: run_input["residentialFallback"] = a.residential_fallback

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
