from discord import ButtonStyle, Interaction, PartialEmoji
from discord.ui import Button, View, button


class SettingsView(View):
    def __init__(self):
        super().__init__()
    
    @button(
        label='Enter Ethereum Address',
        style=ButtonStyle.blurple,
        emoji=PartialEmoji(
            name='ethena_logo',
            id=1346781126781308999
        )
    )
    async def callback(self, button: Button, interaction: Interaction):
        await interaction.respond('hi')
