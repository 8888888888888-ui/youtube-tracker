# YouTube Tracker - Auto Description Updater

Automatically update your YouTube channel description with your current subscriber ranking and track your channel name changes.

**Tracking:** ActuallyDreamz

## Features
- 🤖 Automatically fetches your YouTube subscriber count
- 📊 Calculates your ranking among top YouTubers
- 📝 Updates your channel description automatically
- ⏰ Runs on a schedule (hourly via GitHub Actions)
- 📈 Tracks subscriber ranking history
- 📌 **Tracks all channel name changes** - even if you change your name, your channel will still be recorded!

## How It Works

Every hour (via GitHub Actions), the bot:
1. Fetches your current subscriber count from YouTube
2. Records your current channel name (tracks if it changes)
3. Calculates your ranking
4. Updates your YouTube description with all past channel names and current ranking

**Example Description:**
```
🎥 I'm the #1,234 most subscribed YouTuber!
📊 1,234,567 subscribers
🚀 Channel: ActuallyDreamz → NewChannelName → AnotherName
⏰ Last updated automatically
```

## Setup

### 1. Get YouTube API Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create OAuth 2.0 credentials (Desktop app)
5. Download the credentials JSON

### 2. Store Credentials
- Place `credentials.json` in the root directory
- Add to `.gitignore` (never commit credentials!)

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Locally
```bash
python update_description.py
```

### 5. Set Up GitHub Actions
Configure secrets in Settings → Secrets and Variables → Actions:
- `YOUTUBE_CREDENTIALS_JSON` - Your credentials.json content (base64 encoded)

## File Structure
```
youtube-tracker/
├── update_description.py      # Main script
├── youtube_api.py             # YouTube API functions
├── ranking_service.py         # Ranking calculation & history tracking
├── channel_history.json       # Stores all channel names and ranking history
├── requirements.txt           # Dependencies
├── .github/workflows/
│   └── auto-update.yml        # GitHub Actions workflow
└── .gitignore
```

## Channel History
The `channel_history.json` file automatically tracks:
- All channel name changes with timestamps
- Original channel name
- Channel ID
- Daily ranking and subscriber count history (keeps 1 year of data)

Example:
```json
{
  "channel_names": [
    {
      "name": "ActuallyDreamz",
      "changed_at": "2026-06-18T21:30:00"
    },
    {
      "name": "NewChannelName",
      "changed_at": "2026-07-15T10:15:00"
    }
  ],
  "original_name": "ActuallyDreamz",
  "channel_id": "UCxxxxx",
  "ranking_history": [...]
}
```

## Usage
The bot will automatically:
1. Check your current subscriber count
2. Track any channel name changes
3. Calculate your ranking
4. Update your YouTube description hourly

Track your progress and see your channel history grow! 🚀
