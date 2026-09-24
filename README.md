# Clutch.co Agency API: B2B Company Data, Directory & Reviews

A company data API for [Clutch.co](https://clutch.co), the B2B directory of
agencies and service providers. Walk any category directory, pull full company
profiles, and paginate every verified client review, returned as JSON and as
LLM-ready markdown. This repo shows two ways to use it: a Python quick start, and
Model Context Protocol (MCP) install steps for Claude, Cursor, and ChatGPT.

Actor on Apify Store: [Clutch.co Agency API](https://apify.com/johnvc/clutch-agency-api?fpr=9n7kx3)

Get a free Apify API key: https://apify.com?fpr=9n7kx3

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/hqdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

## Text walkthrough

This is a **company data API** for Clutch.co. Pick a `mode`, give it a URL or a
keyword, and it returns clean rows. In `directory` mode you pass a Clutch
category page such as `https://clutch.co/web-developers` and get one row per
company: name, rating, review count, minimum project size, hourly rate, team
size, location, and the profile link, which is how you build a marketing agency
database or a list of digital marketing agencies for a location. In `profiles`
mode you pass company profile URLs (or bare slugs) and get the full record:
description, founding year, service mix with percentages, industries, client
sizes, pricing bands, and every verified client review as its own row. Every
profile can also carry Clutch's own LLM-ready markdown at no extra cost, which
makes this a good source for shortlisting B2B service providers or feeding a RAG
pipeline. In `search` mode you pass a keyword and it collects the matching
company profiles for you.

## What you get

- **Directory listings** (`listing` rows): name, rating, review count,
  verification badges, minimum project size, hourly rate, employees, location,
  profile URL.
- **Company profiles** (`profile` rows): everything above plus description,
  founding year, all office locations, languages, service lines, focus areas,
  industries, client-size split, cost rating, pricing by service, and packages.
- **Client reviews** (`review` rows): title, rating, the quality, schedule,
  cost, and willing-to-refer breakdown, project services, budget, duration,
  reviewer role and industry, and Clutch's own summaries.
- **Markdown** on any profile row (default), and raw **HTML** on request.

## Quick start (Python)

This example uses Python with [uv](https://docs.astral.sh/uv/). It never uses
pip.

1. Install uv (if you do not have it):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone this repo and enter it:

```bash
git clone https://github.com/johnisanerd/Apify-Clutch-Agency-API.git
cd Apify-Clutch-Agency-API
```

3. Add your Apify API token. Copy `.env.example` to `.env` and paste your token
   (get one free at https://apify.com?fpr=9n7kx3):

```bash
cp .env.example .env
```

4. Run it. The default run stays cheap (one directory page, 10 rows):

```bash
uv run python clutch-agency-api-example.py
```

5. Try the other modes:

```bash
uv run python clutch-agency-api-example.py --example directory
uv run python clutch-agency-api-example.py --example profiles
uv run python clutch-agency-api-example.py --example search
```

## Input parameters

| Field | Type | Notes |
|---|---|---|
| `mode` | string | `directory` (default), `profiles`, or `search`. |
| `directoryUrls` | array | Clutch category or location pages, e.g. `https://clutch.co/web-developers`. |
| `maxPagesPerDirectory` | integer | Result pages per directory URL. Each page is about 70-90 companies. |
| `profileUrls` | array | Company profile URLs, e.g. `https://clutch.co/profile/ignite-visibility`. A bare slug works. |
| `searchQueries` | array | Free-text queries, e.g. `shopify development`. |
| `includeReviews` | boolean | Return every verified review as its own row. Default `true`. |
| `maxReviewsPerProfile` | integer | Cap on reviews per company. |
| `outputFormats` | array | `json`, `markdown` (default), and optionally `html`. |
| `maxItems` | integer | Hard ceiling on rows for the run. Use it as a spend cap. |

## Example output

```json
{
  "result_type": "profile",
  "name": "Ignite Visibility",
  "profile_url": "https://clutch.co/profile/ignite-visibility",
  "website": "https://ignitevisibility.com",
  "rating": 4.8,
  "review_count": 175,
  "min_project_size": "$1,000+",
  "hourly_rate": "$100 - $149",
  "employees": "250 - 999",
  "founded_year": 2013,
  "headquarters": "San Diego, CA",
  "service_lines": [{ "name": "Search Engine Optimization", "percent": 30 }],
  "markdown": "# Ignite Visibility\n## Company Information\n..."
}
```

## Install as an MCP tool

The sections below add the Clutch.co Agency API to Claude, Cursor, and ChatGPT
as a Model Context Protocol tool, so an assistant can call it directly. The MCP
server URL is the same everywhere:

```
https://mcp.apify.com/?tools=actors,docs,johnvc/clutch-agency-api
```

Get a free Apify account at https://apify.com?fpr=9n7kx3 and a token at
https://console.apify.com/settings/integrations .

### Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Clutch.co Agency API
as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or
   **Settings → Developer → Edit Config** to edit `claude_desktop_config.json`
   directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/clutch-agency-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt
   in your browser, or add your Apify API token in the connector settings to
   skip OAuth.
4. In a Cowork chat, ask it to run the Clutch.co Agency API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

### Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one
command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/clutch-agency-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/clutch-agency-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude
Code to call the Clutch.co Agency API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

### Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for
   **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool
   `johnvc/clutch-agency-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL
   `https://mcp.apify.com/?tools=actors,docs,johnvc/clutch-agency-api`, using
   OAuth when prompted.
5. Ask Claude to run the Clutch.co Agency API.

Open Claude on the web: https://claude.ai

### Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/clutch-agency-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/clutch-agency-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is
   connected (green dot).
4. In Composer or Chat, ask Cursor to call the Clutch.co Agency API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

### Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on
ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a
   **Create app** button, open **Advanced settings** and enable
   **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/clutch-agency-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose
   **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

<!-- ask-ai:start -->
## 🤖 Ask an AI assistant about this Actor

Open a ready-to-send prompt about the Clutch.co Agency API in the AI of your choice:

- 💬 [ChatGPT](https://chatgpt.com/?q=Using%20the%20Clutch.co%20Agency%20API%20on%20Apify%20%28https://apify.com/johnvc/clutch-agency-api?fpr=9n7kx3%29%2C%20walk%20me%20through%20this%20use%20case:%20%22Clutch%20Company%20Data%20API%20as%20JSON%20for%20Your%20CRM%22.%20Show%20me%20the%20input%20JSON%2C%20the%20output%20fields%2C%20and%20how%20to%20automate%20it%20with%20the%20API%20or%20MCP.)
- 🧠 [Claude](https://claude.ai/new?q=Using%20the%20Clutch.co%20Agency%20API%20on%20Apify%20%28https://apify.com/johnvc/clutch-agency-api?fpr=9n7kx3%29%2C%20walk%20me%20through%20this%20use%20case:%20%22Clutch%20Company%20Data%20API%20as%20JSON%20for%20Your%20CRM%22.%20Show%20me%20the%20input%20JSON%2C%20the%20output%20fields%2C%20and%20how%20to%20automate%20it%20with%20the%20API%20or%20MCP.)
- 🔍 [Perplexity](https://www.perplexity.ai/search?q=Using%20the%20Clutch.co%20Agency%20API%20on%20Apify%20%28https://apify.com/johnvc/clutch-agency-api?fpr=9n7kx3%29%2C%20walk%20me%20through%20this%20use%20case:%20%22Clutch%20Company%20Data%20API%20as%20JSON%20for%20Your%20CRM%22.%20Show%20me%20the%20input%20JSON%2C%20the%20output%20fields%2C%20and%20how%20to%20automate%20it%20with%20the%20API%20or%20MCP.)
- 🅒 [Copilot](https://copilot.microsoft.com/?q=Using%20the%20Clutch.co%20Agency%20API%20on%20Apify%20%28https://apify.com/johnvc/clutch-agency-api?fpr=9n7kx3%29%2C%20walk%20me%20through%20this%20use%20case:%20%22Clutch%20Company%20Data%20API%20as%20JSON%20for%20Your%20CRM%22.%20Show%20me%20the%20input%20JSON%2C%20the%20output%20fields%2C%20and%20how%20to%20automate%20it%20with%20the%20API%20or%20MCP.)
<!-- ask-ai:end -->

## People also search for

**Is this a company data API?**
Yes. It returns structured company records from Clutch.co: firmographics, service
mix, pricing bands, ratings, and verified reviews, as JSON you can drop into a
CRM or a vector store.

**Can I use it as a B2B directory?**
Yes. Directory mode reads any Clutch category or location page and returns one
row per listed company, which is a ready-made B2B directory export.

**Can I build a marketing agency database?**
Yes. Point directory mode at a marketing category, page through the results, and
you get a marketing agency database with ratings, rates, and locations.

**Does it get client reviews?**
Yes. In profiles and search modes, every verified client review comes back as
its own row, paginated until the company's declared total is reached.

**Do I need a Clutch.co account or API key?**
No. There is nothing to configure on Clutch's side. You only need an Apify API
token to run the Actor. Get one free at https://apify.com?fpr=9n7kx3 .

## Links

- Actor on Apify Store: https://apify.com/johnvc/clutch-agency-api?fpr=9n7kx3
- Apify Python client docs: https://docs.apify.com/api/client/python/
- Apify MCP docs: https://docs.apify.com/platform/integrations/mcp

Last Updated: 2026.09.22
