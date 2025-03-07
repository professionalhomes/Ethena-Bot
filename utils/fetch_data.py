import os

import discord
from discord import Embed
from dotenv import load_dotenv
from web3 import Web3

from utils.record_manager import RecordManager

load_dotenv()
WEB3_PROVIDER_URI = os.getenv('WEB3_PROVIDER_URI')
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))
contract_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"}
        ],
        "name": "balanceOf",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "shares", "type": "uint256"}
        ],
        "name": "convertToAssets",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = w3.eth.contract(
    address='0x9D39A5DE30e57443BfF2A8307A4256c8797A3497',
    abi=contract_abi
)

def getSusdeBalance(address):
    balance = contract.functions.balanceOf(address).call()
    return balance

def convertToUsde(balance):
    usde_balance = contract.functions.convertToAssets(balance).call()
    usde_balance_display = usde_balance / (10 ** 18)
    return usde_balance_display


async def sendDM(bot, timestamp):
    records = RecordManager.readRecord()

    for user in records:
        dm_user = await bot.fetch_user(int(user))
        if user:
            for address in records[user]:
                susde_balance = getSusdeBalance(address)
                usde_balance = convertToUsde(susde_balance)
                susde_balance = susde_balance / (10 ** 18)
                print(f'{susde_balance} {usde_balance}')
                new_records = RecordManager.updateBalance(
                    user,
                    address,
                    timestamp,
                    susde_balance,
                    usde_balance
                )
                embed = Embed(
                    title=f'sUSDe Daily Profit',
                    description=f'Address: {address}',
                    color=0xFFA46E,
                )
                if len(new_records) >= 2:
                    (yesterday, today) = (
                        new_records[list(new_records.keys())[-2]],
                        new_records[list(new_records.keys())[-1]]
                    )

                    embed.add_field(
                        name='Yesterday',
                        value=f'{yesterday['susde_balance']:.4f} sUSDe = {yesterday['usde_balance']:.4f} USDe'
                    )
                    embed.add_field(
                        name='Today',
                        value=f'{today['susde_balance']:.4f} sUSDe = {today['usde_balance']:.4f} USDe'
                    )
                    embed.add_field(
                        name='Daily Profit',
                        value=f'{today['usde_balance'] - yesterday['usde_balance']:.4f} USDe',
                        inline=False
                    )
                else:
                    today = new_records[list(new_records.keys())[-1]]
                    embed.add_field(
                        name='Yesterday',
                        value=f'Data not available, come back tomorrow.'
                    )
                    embed.add_field(
                        name='Today',
                        value=f'{today['susde_balance']:.4f} sUSDe = {today['usde_balance']:.4f} USDe'
                    )
                    embed.add_field(
                        name='Daily Profit',
                        value=f'Data not available, come back tomorrow.',
                        inline=False
                    )
                try:
                    await dm_user.send(embed=embed)
                except discord.Forbidden:
                    print('DM closed')
        else:
            print('User not found')