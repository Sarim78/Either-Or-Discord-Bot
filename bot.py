import discord
from discord.ext import commands

import config
from utils import database
from utils.views import VoteView

EXTENSIONS = ("cogs.rather", "cogs.daily")


class DilemmaDropBot(commands.Bot):
    def __init__(self):
        # Slash commands and buttons do not need the message content intent.
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=discord.Intents.default(),
        )

    async def setup_hook(self):
        database.init_db()

        # Register the button view so old polls keep working after a restart.
        self.add_view(VoteView())

        for extension in EXTENSIONS:
            await self.load_extension(extension)

        await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")


def main():
    if not config.DISCORD_TOKEN:
        raise SystemExit(
            "DISCORD_TOKEN is missing. Copy .env.example to .env and fill it in."
        )
    DilemmaDropBot().run(config.DISCORD_TOKEN)


if __name__ == "__main__":
    main()