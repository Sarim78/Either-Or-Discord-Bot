import random
from datetime import time
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands, tasks

import config
from config import load_questions
from utils import database
from utils.views import VoteView, build_embed


def parse_post_time() -> time:
    hour, minute = (int(part) for part in config.DAILY_POST_TIME.split(":"))
    return time(hour=hour, minute=minute, tzinfo=ZoneInfo(config.TIMEZONE))


class Daily(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        if not config.DAILY_CHANNEL_ID:
            print("DAILY_CHANNEL_ID not set, daily question is turned off.")
            return
        self.daily_post.change_interval(time=parse_post_time())
        self.daily_post.start()

    async def cog_unload(self):
        self.daily_post.cancel()

    @tasks.loop(hours=24)
    async def daily_post(self):
        channel = self.bot.get_channel(config.DAILY_CHANNEL_ID)
        if channel is None:
            try:
                channel = await self.bot.fetch_channel(config.DAILY_CHANNEL_ID)
            except discord.HTTPException:
                print("Could not find the daily channel. Check DAILY_CHANNEL_ID.")
                return

        questions = load_questions()
        if not questions:
            print("No questions available for the daily post.")
            return

        question = random.choice(questions)
        embed = build_embed(question["a"], question["b"], daily=True)

        try:
            message = await channel.send(embed=embed, view=VoteView())
        except discord.HTTPException as error:
            print(f"Could not send the daily question: {error}")
            return

        database.create_poll(
            message_id=message.id,
            channel_id=channel.id,
            option_a=question["a"],
            option_b=question["b"],
            daily=True,
        )

    @daily_post.before_loop
    async def before_daily_post(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(Daily(bot))