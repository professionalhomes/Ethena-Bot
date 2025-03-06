import os
import time

import discord
from dotenv import load_dotenv
from web3 import Web3

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
    balance_display = balance / (10 ** 18)
    timestamp = time.time()

    return (timestamp, balance_display)


async def sendDM(bot):
    user = await bot.fetch_user(874806243208871977)
    if user:
        try:
            (timestamp, balance) = getSusdeBalance('0x9f015B246a6bC257B1205c9df1c03db75DB518aA')
            await user.send(f'{timestamp} {balance}')

        except discord.Forbidden:
            print('DM closed')
    else:
        print('User not found')