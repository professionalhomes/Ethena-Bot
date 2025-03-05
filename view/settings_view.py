from discord import ButtonStyle, Interaction
from discord.ui import Button, View, button


class SettingsView(View):
    def __init__(self):
        super().__init__()
    
    @button(label='Enter Address', style=ButtonStyle.blurple)
    async def callback(self, button: Button, interaction: Interaction):
        await interaction.respond('hi')
