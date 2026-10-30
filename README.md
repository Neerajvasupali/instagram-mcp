<div align="center">

# 📸 Instagram MCP Server

### *Turn your AI Agent into an Autonomous Instagram Growth & Operations Engine*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-v2.3.0-blueviolet?style=for-the-badge&logo=anthropic&logoColor=white)](https://modelcontextprotocol.io/)
[![Meta Graph API](https://img.shields.io/badge/Meta%20Graph%20API-v22.0-0081FB?style=for-the-badge&logo=meta&logoColor=white)](https://developers.facebook.com/docs/instagram-platform)
[![RAM Footprint](https://img.shields.io/badge/Memory-~35MB%20RAM-success?style=for-the-badge&logo=speedtest&logoColor=white)](#-ultra-lightweight--hardware-friendly)
[![Tools Built-in](https://img.shields.io/badge/Tools-31%20Production%20Tools-orange?style=for-the-badge&logo=wakatime&logoColor=white)](#-complete-31-tools-catalog)
[![License](https://img.shields.io/badge/License-MIT-gray?style=for-the-badge)](#)

<p align="center">
  <b>A lightweight, production-grade Model Context Protocol (MCP) server that empowers AI agents (Claude Desktop, Cursor, Antigravity, Continue) with end-to-end control over Instagram Professional (Creator & Business) accounts.</b>
</p>

[Key Features](#-superpowers--capabilities) • 
[Architecture](#-architecture) • 
[Tools Catalog](#-complete-31-tools-catalog) • 
[3-Minute Setup](#-3-minute-quick-start) • 
[Connect Your AI](#-connect-to-your-ai-clients) • 
[Security & Hardening](#-production-grade-engineering)

---

</div>

## ⚡ Superpowers & Capabilities

| Capability | What It Unlocks for Your AI Agent | Key Tools |
| :--- | :--- | :--- |
| 🚀 **Autonomous Publishing** | Auto-publishes Photos, Reels, 24h Stories, and 20-slide Carousels with intelligent video transcoding readiness polling. | `instagram_publish_reel`, `instagram_publish_photo`, `instagram_publish_carousel` |
| 💬 **Community Moderation** | Inspects top-level comments and sub-replies, posts automated responses, and hides spam or deletes offensive comments. | `instagram_get_post_comments`, `instagram_reply_to_comment`, `instagram_hide_comment` |
| 📊 **v22.0 Performance Analytics** | Deep intelligence using Meta’s post-April 2025 unified `views` metric, watch time, follower demographics, and hourly active times. | `instagram_get_media_insights`, `instagram_get_audience_demographics`, `instagram_get_online_followers` |
| 🕵️‍♂️ **Competitor & Market Intel** | Reverse-engineers competitors' public post frequency, engagement metrics, and follower counts without leaving your chat. | `instagram_discover_business` |
| #️⃣ **Hashtag Discovery** | Searches trending tags and monitors recent and top public media to capitalize on viral topics in your niche. | `instagram_search_hashtag`, `instagram_get_hashtag_top_media` |
| 🏷️ **Mentions & Tagging Ops** | Tracks photos/videos where your brand is tagged and replies directly to comments where your account was @mentioned. | `instagram_reply_to_mention`, `instagram_get_mentioned_comment`, `instagram_get_tagged_media` |

---

## 🏛️ Architecture

```mermaid
flowchart LR
    subgraph AI Client ["🤖 Your AI Assistant"]
        Claude["Claude Desktop"]
        Cursor["Cursor IDE"]
        Anti["Antigravity / Gemini"]
    end

    subgraph MCP Engine ["⚡ Instagram MCP Server (Local Process)"]
        Stdio["Standard I/O Transport (stdio)"]
        Server["MCPServer (31 Tools)"]
        Client["Async HTTP Client (httpx)"]
        Auth["Bearer Auth & Auto-Reload"]
    end

    subgraph Meta API ["🌐 Meta Graph API v22.0"]
        Cloud["graph.facebook.com/v22.0"]
        IG["Instagram Professional Account"]
    end

    AI Client <== "JSON-RPC / stdio" ==> Stdio
    Stdio --> Server
    Server --> Client
    Client --> Auth
    Auth <== "HTTPS (Bearer Token)" ==> Cloud
    Cloud <==> IG
```

---

## 🛠️ Complete 31-Tools Catalog

<details open>
<summary><b>1. 🔐 Authentication & Account Management (4 Tools)</b></summary>

| Tool Name | Parameters | Purpose |
| :--- | :--- | :--- |
| `instagram_validate_token` | *(none)* | Ping Meta to verify that your access token is alive and unexpired. |
| `instagram_list_connected_accounts` | *(none)* | Discover Facebook Pages and your exact numeric `INSTAGRAM_ACCOUNT_ID`. |
| `instagram_get_profile` | `account_id` *(optional)* | Fetch bio, username, follower count, media count, website, and avatar. |
| `instagram_get_publishing_quota` | *(none)* | Inspect your rolling 24-hour publishing quota usage and ceiling. |

</details>

<details>
<summary><b>2. 🚀 Content Publishing Engine (5 Tools)</b></summary>

| Tool Name | Parameters | Purpose |
| :--- | :--- | :--- |
| `instagram_publish_photo` | `image_url`, `caption`, `location_id`, `timeout_seconds` | Publish single feed photo with race-condition prevention. |
| `instagram_publish_reel` | `video_url`, `caption`, `cover_url`, `share_to_feed`, `audio_name` | Publish video Reel with automated transcoding status polling. |
| `instagram_publish_story` | `media_url`, `media_type` *(IMAGE/VIDEO)* | Publish 24h ephemeral Story content. |
| `instagram_publish_carousel` | `media_urls` *(2-20 items)*, `media_types`, `caption` | Create multi-asset photo & video carousel albums. |
| `instagram_check_container_status` | `container_id` | Manually check upload processing status (`IN_PROGRESS`, `FINISHED`, `ERROR`). |

</details>

<details>
<summary><b>3. 🖼️ Media & Post Inspection (3 Tools)</b></summary>

| Tool Name | Parameters | Purpose |
| :--- | :--- | :--- |
| `instagram_get_recent_media` | `limit`, `after_cursor` | Paginated feed of recently published posts, Reels, and videos. |
| `instagram_get_media_details` | `media_id` | Deep post inspection: captions, permanent links, timestamps, and comments status. |
| `instagram_get_carousel_children` | `media_id` | Inspect individual child photos/videos inside a carousel album. |

</details>

<details>
<summary><b>4. 💬 Comment Moderation & Engagement (7 Tools)</b></summary>

| Tool Name | Parameters | Purpose |
| :--- | :--- | :--- |
| `instagram_get_post_comments` | `media_id`, `limit`, `after_cursor` | Fetch top-level comments with usernames and like counts. |
| `instagram_get_comment_replies` | `comment_id`, `limit`, `after_cursor` | Retrieve threaded sub-replies under any comment. |
| `instagram_post_comment` | `media_id`, `message` | Post a new top-level comment on any owned post. |
| `instagram_reply_to_comment` | `comment_id`, `message` | Reply directly to an existing comment. |
| `instagram_hide_comment` | `comment_id`, `hide` *(true/false)* | Hide spam/trolls from public view without deleting. |
| `instagram_delete_comment` | `comment_id` | Permanently delete abusive comments. |
| `instagram_toggle_comments` | `media_id`, `enabled` *(true/false)* | Turn comments ON or OFF on a post. |

</details>

<details>
<summary><b>5. 📈 Analytics & Audience Demographics (4 Tools)</b></summary>

| Tool Name | Parameters | Purpose |
| :--- | :--- | :--- |
| `instagram_get_account_insights` | `metric`, `period`, `metric_type`, `breakdown` | Account-level reach, views (`total_value`), and engagement. |
| `instagram_get_media_insights` | `media_id`, `media_type` | Post/Reel metrics with v22.0 watch-time and views. |
| `instagram_get_audience_demographics` | `breakdown` *(country/city/age/gender)* | Follower demographics using v18+ `follower_demographics`. |
| `instagram_get_online_followers` | *(none)* | Follower hourly activity distribution for optimal posting time. |

</details>

<details>
<summary><b>6. 🕵️‍♂️ Competitor Intelligence & Research (1 Tool)</b></summary>

| Tool Name | Parameters | Purpose |
| :--- | :--- | :--- |
| `instagram_discover_business` | `target_username`, `media_limit` | Extract competitor bios, follower counts, and recent post engagement. |

</details>

<details>
<summary><b>7. #️⃣ Hashtag Search & Trends (3 Tools)</b></summary>

| Tool Name | Parameters | Purpose |
| :--- | :--- | :--- |
| `instagram_search_hashtag` | `hashtag` | Lookup Meta's unique hashtag ID for any topic. |
| `instagram_get_hashtag_top_media` | `hashtag_id`, `limit`, `after_cursor` | Query trending/top-performing public media for a hashtag. |
| `instagram_get_hashtag_recent_media` | `hashtag_id`, `limit`, `after_cursor` | Query real-time, recently published public media for a hashtag. |

</details>

<details>
<summary><b>8. 🏷️ Mentions & Tagged Media (4 Tools)</b></summary>

| Tool Name | Parameters | Purpose |
| :--- | :--- | :--- |
| `instagram_get_tagged_media` | `limit`, `after_cursor` | Retrieve photos/videos where other users visually tagged your account. |
| `instagram_get_mentioned_comment` | `comment_id` | Read comment content and find parent `media_id` when @mentioned. |
| `instagram_get_mentioned_media` | `media_id` | Retrieve media where your account was @mentioned inside the caption. |
| `instagram_reply_to_mention` | `media_id`, `comment_id`, `message` | Post a verified reply when @mentioned in a comment. |

</details>

---

## 🚀 3-Minute Quick Start

### 1. Prerequisites
* Python 3.10+ installed
* A free Instagram Professional (Creator or Business) Account linked to a Facebook Page

---

### 2. Clone & Install Dependencies
Everything runs 100% project-scoped inside your virtual environment — zero global package pollution:

```bash
git clone https://github.com/Neerajvasupali/instagram-mcp.git
cd instagram-mcp
```

#### On Windows (PowerShell / Command Prompt):
```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
Copy-Item .env.example .env
```

#### On macOS & Linux (Bash / Zsh):
```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
cp .env.example .env
```

---

### 3. Get Your Free Meta Credentials (No Credit Card Needed)

> [!NOTE]
> All Instagram Graph API access is **100% free** for Creator and Business accounts.

1. **Switch Instagram Account:** Open the Instagram mobile app $\rightarrow$ *Settings* $\rightarrow$ *Switch to Professional Account* (choose **Creator** or **Business**).
2. **Link a Facebook Page:** In the Instagram app $\rightarrow$ *Edit Profile* $\rightarrow$ *Page* $\rightarrow$ Connect any free Facebook Page.
3. **Create a Free Developer App:**
   * Go to [developers.facebook.com](https://developers.facebook.com/) $\rightarrow$ **My Apps** $\rightarrow$ **Create App**.
   * Select **Other** $\rightarrow$ **Business** $\rightarrow$ Name it (e.g. `Instagram Agent`).
4. **Generate Token in Explorer:**
   * Open the [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/).
   * Select your App $\rightarrow$ Click **Get User Access Token**.
   * Add permissions:
     * `instagram_basic`
     * `instagram_content_publish`
     * `instagram_manage_comments`
     * `instagram_manage_insights`
     * `pages_show_list`
     * `pages_read_engagement`
   * Click **Generate Access Token**.
5. **Extend to a 60-Day Token:** Click the **ℹ️ (Info)** button next to the token in Explorer $\rightarrow$ **Open in Access Token Tool** $\rightarrow$ Click **Extend Access Token**.

---

### 4. Configure Your `.env`

Open `.env` and paste your access token:

```env
INSTAGRAM_ACCESS_TOKEN=your_60_day_token_here
INSTAGRAM_ACCOUNT_ID=
GRAPH_API_VERSION=v22.0
```

> [!TIP]
> **Don't know your numeric `INSTAGRAM_ACCOUNT_ID`?**  
> Just leave it blank! The server has built-in auto-discovery. Run the discovery tool:
> 
> **Windows:**
> ```powershell
> .\.venv\Scripts\python.exe -c "import asyncio; from src.tools.profile import *; from src.server import server; print(asyncio.run(server.call_tool('instagram_list_connected_accounts', {})))"
> ```
> 
> **macOS / Linux:**
> ```bash
> ./.venv/bin/python -c "import asyncio; from src.tools.profile import *; from src.server import server; print(asyncio.run(server.call_tool('instagram_list_connected_accounts', {})))"
> ```
> It will query Meta and print your exact `INSTAGRAM_ACCOUNT_ID`! Then paste it into `.env`.

---

## 🔌 Connect to Your AI Clients

Replace `<PATH_TO_INSTAGRAM_MCP>` with your actual absolute project path:
* **Windows Example:** `C:\\Users\\username\\Projects\\instagram-mcp` (or `D:\\Instagram`)
* **macOS / Linux Example:** `/Users/username/Projects/instagram-mcp`

### 🤖 Claude Desktop
Add to your Claude Desktop config file:
* **Windows Location:** `%APPDATA%\Claude\claude_desktop_config.json`
* **macOS Location:** `~/Library/Application Support/Claude/claude_desktop_config.json`

#### Windows Config:
```json
{
  "mcpServers": {
    "instagram": {
      "command": "<PATH_TO_INSTAGRAM_MCP>\\.venv\\Scripts\\python.exe",
      "args": ["<PATH_TO_INSTAGRAM_MCP>\\run.py"],
      "cwd": "<PATH_TO_INSTAGRAM_MCP>"
    }
  }
}
```

#### macOS / Linux Config:
```json
{
  "mcpServers": {
    "instagram": {
      "command": "<PATH_TO_INSTAGRAM_MCP>/.venv/bin/python",
      "args": ["<PATH_TO_INSTAGRAM_MCP>/run.py"],
      "cwd": "<PATH_TO_INSTAGRAM_MCP>"
    }
  }
}
```

---

### ⚡ Cursor IDE
Go to **Settings** $\rightarrow$ **Features** $\rightarrow$ **MCP Servers** $\rightarrow$ **Add New MCP Server**:
* **Name:** `instagram`
* **Type:** `command`
* **Command (Windows):** `<PATH_TO_INSTAGRAM_MCP>\.venv\Scripts\python.exe <PATH_TO_INSTAGRAM_MCP>\run.py`
* **Command (macOS/Linux):** `<PATH_TO_INSTAGRAM_MCP>/.venv/bin/python <PATH_TO_INSTAGRAM_MCP>/run.py`

---

### 🪐 Antigravity / Gemini CLI
Add to your project config (`mcp_config.json` or `.gemini/antigravity-cli/mcp.json`):

```json
{
  "mcpServers": {
    "instagram": {
      "command": "<PATH_TO_INSTAGRAM_MCP>/.venv/bin/python",
      "args": ["<PATH_TO_INSTAGRAM_MCP>/run.py"],
      "cwd": "<PATH_TO_INSTAGRAM_MCP>"
    }
  }
}
```

---

## 🛡️ Production-Grade Engineering

* 🔒 **Zero Token Leakage:** Authentication strictly uses HTTP `Authorization: Bearer <token>` headers instead of exposing keys in URL query strings.
* 📦 **Strict POST Body Transmission:** Payloads are transmitted directly through HTTP request bodies, adhering to Meta Graph API specifications.
* 🔄 **Dynamic Environment Reloading:** Tokens are re-read dynamically on each invocation (`load_dotenv(override=True)`), so updating credentials never requires restarting the server.
* ⏱️ **Race Condition Elimination:** Automated container polling loop waits for Meta's transcoding queue to report `FINISHED` before attempting to publish media.
* 🪶 **Ultra-Lightweight & Hardware-Friendly:** Pure Python async I/O with an idle memory footprint of **~35 MB RAM** (vs 150–300 MB for Node/Electron servers).

---

<div align="center">
  <b>Built with ❤️ for Autonomous Social Media Automation</b><br>
  <sub>Meta Graph API v22.0 Aligned • Model Context Protocol Compliant</sub>
</div>
