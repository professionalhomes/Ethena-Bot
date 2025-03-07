from discord import (ButtonStyle, Embed, InputTextStyle, Interaction,
                     PartialEmoji)
from discord.ui import Button, InputText, Modal, View, button

from utils.record_manager import RecordManager


class AddressModal(Modal):
    def __init__(self, uid):
        super().__init__(title='Enter Ethereum addresses.')
        records = RecordManager.readRecord(uid)
        address_ct = 0
        if records: address_ct = len(records)
        
        for i in range(5):
            if i < address_ct:
                address = list(records.keys())[i]
            else:
                address = '0x...'

            inp = InputText(
                label=f'Enter Ethereum address.',
                placeholder=address,
                style=InputTextStyle.short,
                min_length=42,
                max_length=42,
                required=False
            )

            self.add_item(inp)

    async def callback(self, interaction):
        uid = str(interaction.user.id)
        inputs = [child.value for child in self.children if isinstance(child, InputText)]
        new_records = {}
        old_records = RecordManager.readRecord(uid)
        if old_records:
            for index, new_address in enumerate(inputs):
                if new_address in new_records or new_address == '0x0000000000000000000000000000000000000000':
                    continue

                elif new_address == '': # keep old address and data
                    if index < len(old_records):
                        old_address = list(old_records.keys())[index]
                        new_records[old_address] = old_records[old_address]

                elif new_address in old_records: # keep old data
                    new_records[new_address] = old_records[new_address]

                else: # add new address, empty data
                    new_records[new_address] = {}
        
        RecordManager.updateRecord(uid, new_records)
        
        new_addresses_text = ''
        for na in new_records.keys():
            new_addresses_text += na
            if na != list[-1]:
                new_addresses_text += '\n'
        embed = Embed(
            title='Success',
            color=0xFFA46E,
            description=f'The bot is now monitoring the following addresses:\n{new_addresses_text}'
        )
        await interaction.respond(embed=embed, ephemeral=True)


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
