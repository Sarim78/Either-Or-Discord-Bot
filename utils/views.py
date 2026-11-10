import discord

from utils import database


def make_bar(percent: int, length: int = 10) -> str:
    filled = round(percent / 100 * length)
    return "█" * filled + "░" * (length - filled)


def build_embed(
    option_a: str,
    option_b: str,
    votes_a: int = 0,
    votes_b: int = 0,
    daily: bool = False,
) -> discord.Embed:
    total = votes_a + votes_b
    percent_a = round(votes_a / total * 100) if total else 0
    percent_b = round(votes_b / total * 100) if total else 0

    embed = discord.Embed(
        title="Daily Dilemma" if daily else "Would You Rather...",
        color=discord.Color.blurple(),
    )
    embed.add_field(
        name="Option A",
        value=f"{option_a}\n{make_bar(percent_a)} **{percent_a}%** ({votes_a})",
        inline=False,
    )
    embed.add_field(
        name="Option B",
        value=f"{option_b}\n{make_bar(percent_b)} **{percent_b}%** ({votes_b})",
        inline=False,
    )
    embed.set_footer(text=f"{total} vote{'s' if total != 1 else ''}")
    return embed


class VoteView(discord.ui.View):
    """Two buttons that work on any poll message, even after a restart."""

    def __init__(self):
        super().__init__(timeout=None)

    async def handle_vote(self, interaction: discord.Interaction, choice: str):
        message_id = interaction.message.id
        poll = database.get_poll(message_id)

        if poll is None:
            await interaction.response.send_message(
                "This poll is no longer active.", ephemeral=True
            )
            return

        recorded = database.add_vote(message_id, interaction.user.id, choice)
        if not recorded:
            previous = database.get_user_vote(message_id, interaction.user.id)
            await interaction.response.send_message(
                f"You already voted for Option {previous.upper()}.",
                ephemeral=True,
            )
            return

        votes_a, votes_b = database.get_counts(message_id)
        embed = build_embed(
            poll["option_a"],
            poll["option_b"],
            votes_a,
            votes_b,
            daily=bool(poll["daily"]),
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        label="Option A",
        style=discord.ButtonStyle.primary,
        custom_id="rather:a",
    )
    async def option_a(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.handle_vote(interaction, "a")

    @discord.ui.button(
        label="Option B",
        style=discord.ButtonStyle.danger,
        custom_id="rather:b",
    )
    async def option_b(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.handle_vote(interaction, "b")