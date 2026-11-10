import random

import discord
from discord import app_commands
from discord.ext import commands

from config import load_questions
from utils import database
from utils.views import VoteView, build_embed


class Rather(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="rather",
        description="Post a random would you rather question",
    )
    async def rather(self, interaction: discord.Interaction):
        questions = load_questions()
        if not questions:
            await interaction.response.send_message(
                "There are no questions yet. Add some to data/questions.json.",
                ephemeral=True,
            )
            return

        question = random.choice(questions)
        embed = build_embed(question["a"], question["b"])

        await interaction.response.send_message(embed=embed, view=VoteView())
        message = await interaction.original_response()

        database.create_poll(
            message_id=message.id,
            channel_id=interaction.channel_id,
            option_a=question["a"],
            option_b=question["b"],
            daily=False,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Rather(bot))