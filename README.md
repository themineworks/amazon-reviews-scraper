# Amazon Reviews Scraper: Ratings, Text, Verified Badge

Scrape Amazon customer reviews by ASIN: star rating, title, full review body, verified purchase badge, helpful vote count and review images. Supports 8 Amazon marketplaces. Sort by recency or top-rated. Pay per review. Failed results are never charged.

**Run it on Apify:** [apify.com/themineworks/amazon-reviews](https://apify.com/themineworks/amazon-reviews)
**Docs, FAQ and pricing:** [themineworks.com/actors/amazon-reviews](https://themineworks.com/actors/amazon-reviews/)

**Price:** From $3.42 per 1,000 reviews on Apify's higher plans ($5.70 on the free plan), plus a $0.01 start fee per run. Failed and empty results are never charged.

## What it returns

* Full review text, star rating, title and reviewer name
* Verified purchase badge and helpful vote count
* Review images (when customers include photos)
* Sort by most recent or top-rated
* 8 marketplaces: US, UK, DE, FR, JP, IN, CA, AU
* Filter by star rating (1-5 stars)

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/amazon-reviews").call(run_input={
    "asins": [
        "B08N5KWB9H"
    ],
    "maxReviews": 13
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/amazon-reviews').call({
    "asins": [
        "B08N5KWB9H"
    ],
    "maxReviews": 13
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~amazon-reviews/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"asins": ["B08N5KWB9H"], "maxReviews": 13}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 amazon_reviews_scraper.py --token YOUR_APIFY_TOKEN --asins "B08N5KWB9H" --max-reviews "13"
node amazon_reviews_scraper.mjs --token YOUR_APIFY_TOKEN --asins "B08N5KWB9H" --max-reviews "13"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `asins` | array |  | Amazon ASINs or full product URLs |
| `marketplace` | string | `"amazon.com"` | Amazon marketplace domain |
| `maxReviews` | integer | `50` | Upper limit on reviews returned per ASIN |
| `sortBy` | string | `"recent"` | Order of the returned reviews |
| `filterByStar` | string | `"all"` | Keep only reviews with this star rating |
| `includeInternational` | boolean | `true` | Amazon shows a "reviews from other countries" block on most listings, typically 5 of the 13 reviews |
| `residentialFallback` | boolean | `true` | Retry on a residential IP when the standard proxy is blocked, or when Amazon returns a product page it cut… |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `reviewId` | string | Amazon review ID |
| `asin` | string | Amazon product ID |
| `marketplace` | string | Marketplace scraped (for example amazon.com) |
| `title` | string | Review headline |
| `body` | string | Full review text |
| `rating` | number | Star rating 1-5 |
| `date` | string | Review date (ISO-8601 best-effort) |
| `dateLocalized` | string | Date as shown on the page |
| `authorName` | string | Reviewer display name |
| `authorUrl` | string | Link to reviewer profile |
| `verifiedPurchase` | boolean | True if marked Verified Purchase |
| `helpfulVotes` | number | Number of helpful votes |
| `images` | array | Review photo URLs |
| `variant` | string | Product variant (for example Color: Black) |
| `productUrl` | string | URL of the product page the review was read from |
| `scraped_at` | string | ISO-8601 timestamp |
| `reviewCountry` | string | Country the review was written in (from the review date line) |
| `reviewSource` | string | local = this marketplace's own reviews; international = Amazon's "reviews from other countries" block |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/amazon-reviews
```

## FAQ

### Do I need an Amazon SP-API account to use this?

No. The actor accesses publicly visible review pages directly. No SP-API account, seller account, or Amazon credentials required.

### Can I filter reviews to verified purchases only?

Yes. Set verifiedPurchaseOnly to true and the actor returns only reviews marked with the verified purchase badge.

### Which Amazon marketplaces are supported?

Eight: amazon.com (US), amazon.co.uk (UK), amazon.de (Germany), amazon.fr (France), amazon.co.jp (Japan), amazon.in (India), amazon.ca (Canada) and amazon.com.au (Australia). Set the marketplace input to the domain you want.

### Can I sort by date or by helpfulness?

Yes. Set sortBy to "recent" for chronological order or "helpful" to surface reviews with the most helpful votes first.

### Are review images captured?

Yes. When a reviewer includes photos with their review, the imageUrls field contains the URLs of those images.

### How much does the Amazon Reviews Scraper cost?

From $3.42 per 1,000 reviews on Apify's higher plans ($5.70 on the free plan), plus a $0.01 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [B2B Leads Finder](https://themineworks.com/actors/b2b-leads-finder/): Business emails and LinkedIn profiles for target companies
* [LinkedIn Company Scraper](https://themineworks.com/actors/linkedin-company-details/): Company size, industry, website, and followers without login
* [Zillow Rental Listings Scraper](https://themineworks.com/actors/zillow-rental-listings/): Scrape Zillow for-rent listings by city or zip. $1 per 1,000 results

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
