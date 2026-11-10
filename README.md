# Dilemma-Drop-Discord-Bot

A Discord bot that posts "Would You Rather" dilemmas with voting buttons, shows the live vote split, and drops a fresh question every day at a time you choose.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

Dilemma Drop turns a simple game into a daily ritual for your server. Members vote with a single button click, each person gets one vote per question, and the results update as votes come in. No outside APIs or paid services are needed.

## Features

- Slash command `/rather` that posts a random dilemma with two buttons
- Live vote split shown as percentages after each vote
- One vote per person per question, stored in SQLite
- Daily automatic question at a time you set
- Votes survive restarts
- Easy to expand: add your own questions in a single JSON file

## Screenshots

Add a screenshot or GIF of the bot in action here.

## Getting Started

### Prerequisites

- Python 3.10 or newer
- A Discord account and a server where you can add bots

### 1. Create the Discord application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and click **New Application**.
2. Open the **Bot** tab and click **Reset Token**. Copy the token and keep it private.
3. Open **OAuth2 > URL Generator**, select the `bot` and `applications.commands` scopes, and give the bot permission to **Send Messages** and **Embed Links**.
4. Open the generated URL to invite the bot to your server.

### 2. Install the project

```bash
git clone https://github.com/Sarim78/Dilemma-Drop-Discord-Bot.git
cd Dilemma-Drop-Discord-Bot
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure your settings

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description |
| --- | --- |
| `DISCORD_TOKEN` | Your bot token from the Developer Portal |
| `DAILY_CHANNEL_ID` | ID of the channel for the daily question |
| `DAILY_POST_TIME` | Time of the daily post in 24-hour format, for example `18:00` |

To get a channel ID, turn on Developer Mode in Discord settings, then right-click the channel and choose **Copy Channel ID**.

### 4. Run the bot

```bash
python bot.py
```

When you see the "Logged in" message in the terminal, the bot is online.

## Usage

| Command | What it does |
| --- | --- |
| `/rather` | Posts a random would you rather question with two voting buttons |

The daily question posts automatically in the channel you set in `DAILY_CHANNEL_ID`.

## Adding Your Own Questions

Open `data/questions.json` and add a new entry:

```json
{
  "a": "Be able to fly",
  "b": "Be able to turn invisible"
}
```

Restart the bot and your new question will join the random pool.

## Project Structure

```
Dilemma-Drop-Discord-Bot/
├── bot.py              # Entry point: logs in, loads cogs, syncs commands
├── config.py           # Reads settings from environment variables
├── requirements.txt    # Python dependencies
├── .env.example        # Template for your environment variables
├── cogs/
│   ├── rather.py       # The /rather command
│   └── daily.py        # Scheduled daily question
├── utils/
│   ├── views.py        # Button layout and click handling
│   └── database.py     # SQLite vote storage
└── data/
    └── questions.json  # Your list of dilemmas
```

## Hosting

The bot is only online while the script is running. For testing, running it on your own computer is fine. For a server that needs it available all day, run it on a small VPS, a Raspberry Pi, or any machine that stays on.

## Security Notes

- Never commit your `.env` file or share your bot token. If a token leaks, reset it right away in the Developer Portal.
- The `.gitignore` already excludes `.env`, `data/votes.db`, and `__pycache__/`.

## Contributing

Contributions are welcome. Fork the repo, create a branch for your change, and open a pull request with a short description of what you changed.

## License

Released under the MIT License. See the `LICENSE` file for details.
