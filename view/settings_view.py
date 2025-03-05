from discord import ButtonStyle, InputTextStyle, Interaction, PartialEmoji
from discord.ui import Button, InputText, Modal, View, button

from utils.record_manager import RecordManager


class AddressModal(Modal):
    def __init__(self, uid):
        super().__init__(title='Ethereum addresses. Enter 0 to remove old one')
        records = RecordManager.readRecord(uid)
        address_ct = len(records)
        
        for i in range(5):
            if i < address_ct:
                address = list(records.keys())[i]
            else:
                address = '0x...'
            print(address)

            inp = InputText(
                label=f'Enter Ethereum address.',
                placeholder=address,
                style=InputTextStyle.short,
                min_length=40,
                max_length=40,
                required=False
            )

            self.add_item(inp)

    async def callback(self, interaction):
        mid = interaction.user.id
        inputs = [child.value for child in self.children if isinstance(child, InputText)]
        print(inputs)


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
        uid = str(interaction.user.id)
        await interaction.response.send_modal(AddressModal(uid))
