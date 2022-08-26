from asyncio import tasks
import logging
from solana_nfts import Client
from tf_backend.data.db_access import remove_holder
from tf_backend.data.db_access import update_holder
from tf_backend.discord_bot.bot import AddRole, RemoveRole
from tf_backend.data.db_access import get_all_holders

nft_client = Client()


def NFTCheck(wallet_id):
    nfts = nft_client.fetch_nfts_from_wallet_address(wallet_id)
    count = 0
    Status = "INACTIVE"
    for nft in nfts:
        nft_token_metadata = nft["token_metadata"]
        nft_metadata = nft_token_metadata["metadata"]
        nft_data = nft_metadata["data"]
        if nft_data["symbol"] == 'TOAST':
            count += 1
            Status = "ACTIVE"

    return Status, count

def StartStacking(wallet_id):
    #update database with current time as staking start
    #init total rewards to 0
    #init claimed reward to 0
    return 0

def ClaimStaking(wallet_id):
    #get wallet_id document total rewards - claimed rewards = amount to claim
    #send amount back to frontend
    # return amount
    return 0

def UpdateStaking(wallet_id):
    #get staking start time - current time = staking period
    #if staking period is within set frames award x amount
    #set total rewards in db
    return 0

def UpdateClaim(wallet_id, amount_claimed):
    #get db claimed + amount_claimed = total claimed
    #updated db with total claimed
    return 0


async def HolderChecker():
    all_holders = await get_all_holders()
    for holder in all_holders:
        wallet_id = holder['wallet_id']
        discord_id = holder['discord_id']
        holder_info = NFTCheck(wallet_id)
        status = holder_info[0]
        amount = holder_info[1]
        await update_holder(wallet_id, status, amount)
        if status == "ACTIVE":
            await AddRole(discord_id)
        if status == "INACTIVE":
            await RemoveRole(discord_id)
            await remove_holder(wallet_id)

