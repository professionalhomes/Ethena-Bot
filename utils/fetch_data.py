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
            embed = Embed(
                title='sUSDe Daily Profit',
                color=0xFFA46E,
            )
            for address in records[user]:
                susde_balance = getSusdeBalance(address)
                usde_balance = convertToUsde(susde_balance)
                susde_balance = susde_balance / (10 ** 18)
                print(f'{susde_balance} {usde_balance}')
                RecordManager.updateBalance(
                    user,
                    address,
                    timestamp,
                    susde_balance,
                    usde_balance
                )

            try:
                await dm_user.send(embed=embed)

            except discord.Forbidden:
                print('DM closed')
        else:
            print('User not found')