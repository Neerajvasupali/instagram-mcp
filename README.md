# Instagram Model Context Protocol (MCP) Server

A lightweight, production-grade MCP server that gives AI agents (such as Antigravity, Claude Desktop, Cursor, etc.) full control over Instagram Professional (Creator & Business) accounts using the Meta Graph API v22.0.

---

## 🚀 Key Capabilities (31 Tools Built-In)

* **Authentication & Profile:**
  * Validate and ping active access token status (`instagram_validate_token`).
  * Discover Facebook Pages & connected Instagram account IDs (`instagram_list_connected_accounts`).
  * Read bio, follower count, follows count, media count, website, profile picture (`instagram_get_profile`).
  * Check 24h publishing limits and quota usage (`instagram_get_publishing_quota`).
* **Content Publishing:**
  * Single photo feed posts with race-condition prevention (`instagram_publish_photo`).
  * Reels with automated video transcoding status polling (`instagram_publish_reel`).
  * Stories for 24h ephemeral content (`instagram_publish_story`).
  * Multi-item carousel albums up to 20 items with child container synchronization (`instagram_publish_carousel`).
  * Container status inspector (`instagram_check_container_status`).
* **Media Management:**
  * List recent posts with cursor-based pagination (`instagram_get_recent_media`).
  * Inspect deep post details (`instagram_get_media_details`).
  * Inspect carousel child elements (`instagram_get_carousel_children`).
* **Comment Moderation:**
  * Read top-level comments with cursor pagination (`instagram_get_post_comments`).
  * Read threaded replies with cursor pagination (`instagram_get_comment_replies`).
  * Post comments (`instagram_post_comment`).
  * Reply to comments (`instagram_reply_to_comment`).
  * Hide/unhide comments (`instagram_hide_comment`).
  * Delete comments (`instagram_delete_comment`).
  * Enable/disable comments on posts via `comment_enabled` (`instagram_toggle_comments`).
* **Analytics & Insights:**
  * Account-level reach, views, and interactions (`instagram_get_account_insights`).
  * Post/Reel/Story metrics with updated v22 views & watch-time fields (`instagram_get_media_insights`).
  * Follower demographics by country, city, age, and gender using the modern `follower_demographics` API (`instagram_get_audience_demographics`).
  * Active follower hours by day (`instagram_get_online_followers`).
* **Competitive Intelligence:**
  * Research competitor profiles and public posts (`instagram_discover_business`).
* **Hashtag Research:**
  * Search hashtag IDs (`instagram_search_hashtag`).
  * Fetch top/trending posts with pagination (`instagram_get_hashtag_top_media`).
  * Fetch recent posts with pagination (`instagram_get_hashtag_recent_media`).
* **Mentions & Tagging:**
  * View posts where the account is visually tagged (`instagram_get_tagged_media`).
  * Look up details of comments where you were @mentioned (`instagram_get_mentioned_comment`).
  * Look up details of media where you were @mentioned in captions (`instagram_get_mentioned_media`).
  * Reply to comment @mentions with media_id validation (`instagram_reply_to_mention`).

---

## 📁 Project Structure

All dependencies and virtual environments are 100% self-contained in this folder:

```text
D:\Instagram\
├── .venv\                     # Project-isolated Python virtual environment
├── .env                       # Your secret credentials (not tracked in git)
├── .env.example               # Reference template for configuration
├── .gitignore                 # Standard git ignore rules
├── requirements.txt           # Project dependencies (mcp, httpx, python-dotenv)
├── mcp_config_sample.json     # Configuration snippet for AI clients
├── README.md                  # This documentation
├── run.py                     # Direct entrypoint for MCP clients
└── src\
    ├── __init__.py
    ├── client.py              # Async HTTP client for Meta Graph API with error handling
    ├── server.py              # Main MCP Server entry point (stdio transport)
    └── tools\
        ├── __init__.py        # Tool registration bundle
        ├── profile.py         # Profile, auth check & quota tools
        ├── publishing.py      # Photo, Reel, Story, Carousel publishing tools
        ├── media.py           # Recent media & details tools (with pagination)
        ├── comments.py        # Comment moderation & reply tools
        ├── insights.py        # Analytics, follower demographics & metrics tools
        ├── discovery.py       # Competitor intelligence tools
        ├── hashtags.py        # Hashtag search & top media tools
        └── mentions.py        # Tagged media & mention reply tools
```

---

## ⚙️ Quick Start & Setup Instructions

### Prerequisites
* Python 3.10+ (Python 3.11, 3.12, 3.13, or 3.14)
* A free Instagram Professional (Creator or Business) Account linked to a Facebook Page

---

### Step 1: Clone or Open the Repository
```powershell
cd D:\Instagram
```

### Step 2: Set up Virtual Environment & Dependencies
*(If you are setting this up for the first time or on a new machine)*:
```powershell
# Create project-local virtual environment
python -m venv .venv

# Activate environment and install dependencies
.\.venv\Scripts\pip.exe install -r requirements.txt
```

---

### Step 3: Get Your Free Meta Graph API Credentials

You do **NOT** need a paid business account or credit card. Everything is 100% free:

1. **Switch Instagram Account to Professional:**
   * Open the Instagram mobile app $\rightarrow$ *Settings* $\rightarrow$ *Account Type and Tools* $\rightarrow$ *Switch to Professional Account* (choose **Creator** or **Business**).
2. **Link a Facebook Page:**
   * In the Instagram app $\rightarrow$ *Edit Profile* $\rightarrow$ *Page* $\rightarrow$ Create or link any free Facebook Page.
3. **Create a Free Meta Developer App:**
   * Go to the [Meta for Developers Portal](https://developers.facebook.com/).
   * Click **My Apps** $\rightarrow$ **Create App**.
   * Select **Other** as the use case $\rightarrow$ Choose **Business** app type $\rightarrow$ Give it a name (e.g., `My Instagram Assistant`).
4. **Generate Access Token in Graph API Explorer:**
   * Open the [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/).
   * Under **Meta App**, select your app.
   * Under **User or Page**, select **Get User Access Token**.
   * Add the following permissions (scopes):
     * `instagram_basic`
     * `instagram_content_publish`
     * `instagram_manage_comments`
     * `instagram_manage_insights`
     * `pages_show_list`
     * `pages_read_engagement`
   * Click **Generate Access Token** and approve the prompt.
5. **Exchange for a 60-Day Long-Lived Token:**
   * Click the **ℹ️ (Info)** button next to the Access Token field in Graph API Explorer $\rightarrow$ Click **Open in Access Token Tool**.
   * Click **Extend Access Token** at the bottom to get a token valid for 60 days.

---

### Step 4: Configure Your Environment (`.env`)

Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```

Open `.env` and fill in your credentials:
```env
# D:\Instagram\.env
INSTAGRAM_ACCESS_TOKEN=your_long_lived_meta_access_token_here
INSTAGRAM_ACCOUNT_ID=your_numeric_instagram_account_id_here
GRAPH_API_VERSION=v22.0
```

> 💡 **Don't know your `INSTAGRAM_ACCOUNT_ID` yet?**  
> Don't worry! Just fill in `INSTAGRAM_ACCESS_TOKEN` first. Then connect to your AI client or run:
> ```powershell
> .\.venv\Scripts\python.exe -c "import asyncio; from src.tools.profile import *; from src.server import server; print(asyncio.run(server.call_tool('instagram_list_connected_accounts', {})))"
> ```
> This tool will query Meta and print your exact numeric Instagram Business Account ID! Then simply copy it into `.env`.

---

### Step 5: Test the Server Locally

Verify that all **31 tools** are registered cleanly:

```powershell
.\.venv\Scripts\python.exe -c "import asyncio; from src.server import server; tools = asyncio.run(server.list_tools()); print(f'{len(tools)} tools ready!'); [print(f' - {t.name}') for t in tools]"
```

Test your token validation:

```powershell
.\.venv\Scripts\python.exe -c "import asyncio; from src.server import server; print(asyncio.run(server.call_tool('instagram_validate_token', {})))"
```

To run the MCP server directly in standard I/O mode:

```powershell
.\.venv\Scripts\python.exe run.py
```

---

## 🔌 Connecting to Your AI Clients

### 1. Claude Desktop
Add this to your Claude Desktop configuration file:
* **Windows File Location:** `%APPDATA%\Claude\claude_desktop_config.json`
* **macOS File Location:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "instagram": {
      "command": "D:\\Instagram\\.venv\\Scripts\\python.exe",
      "args": ["D:\\Instagram\\run.py"],
      "cwd": "D:\\Instagram"
    }
  }
}
```

### 2. Antigravity / Gemini CLI
Add to your project or user MCP configuration (`mcp_config.json` or `.gemini/antigravity-cli/mcp.json`):

```json
{
  "mcpServers": {
    "instagram": {
      "command": "D:\\Instagram\\.venv\\Scripts\\python.exe",
      "args": ["D:\\Instagram\\run.py"],
      "cwd": "D:\\Instagram"
    }
  }
}
```

### 3. Cursor IDE
Open **Cursor Settings** $\rightarrow$ **Features** $\rightarrow$ **MCP Servers** $\rightarrow$ **Add New MCP Server**:
* **Name:** `instagram`
* **Type:** `command`
* **Command:** `D:\Instagram\.venv\Scripts\python.exe D:\Instagram\run.py`

---

## 🛡️ Architecture & Security Highlights

1. **Security-First Headers:** Uses `Authorization: Bearer <token>` headers instead of leaking tokens into URL query strings.
2. **Proper POST Body Payloads:** Transmits all publishing parameters (`media_type`, `caption`, `video_url`, `children`) via the POST body rather than query parameters, conforming strictly to Meta Graph API specifications.
3. **Dynamic Token Reloading:** Loads credentials dynamically upon tool calls, preventing silent failures when tokens are refreshed in `.env`.
4. **Graph API v22.0 Alignment:** Adheres to current Meta specifications (e.g., `follower_demographics` breakdown model, `comment_enabled` toggle boolean, and `ig_reels_avg_watch_time`/`ig_reels_video_view_total_time` metrics).
5. **Resource-Light:** Pure Python stdio process with low memory footprint (~35MB RAM).
