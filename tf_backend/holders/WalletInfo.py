from asyncio import tasks
from datetime import datetime, timezone
import logging
from solana_nfts import Client
from tf_backend.data.db_access import remove_holder, update_holder, get_all_holders, get_holder, update_reward, UpdatedClaimed
from tf_backend.discord_bot.bot import AddRole, RemoveRole

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

async def ClaimStaking(wallet_id):
    await UpdateStaking(wallet_id)
    resp = await get_holder(wallet_id)
    total_rewards = resp["total rewards"]
    claimed_rewards = resp["claimed rewards"]
    claim_amount = total_rewards - claimed_rewards
    await UpdateClaim(wallet_id, claim_amount, claimed_rewards)
    return claim_amount

async def UpdateStaking(wallet_id):
    resp = await get_holder(wallet_id)
    amount = resp["amount"]
    print(amount)
    start_staking = resp["staking start"]
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    cnvrt2 = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%S')
    cnvrt = datetime.strptime(start_staking, '%Y-%m-%dT%H:%M:%S')
    stake_period = cnvrt2 - cnvrt
    print(stake_period)
    seconds = stake_period.total_seconds()
    
    total_rewards = 0
    y = 0
    if seconds < 604800:
        while y < amount:
            y += 1
            x = 0
            while x < seconds:
                x += 1
                total_rewards += 0.00003472
    elif stake_period >= 604800 and stake_period < 1296000:
        while y < amount:
            y += 1
            x = 0
            while x < seconds:
                x += 1
                total_rewards += 0.00005787
    elif stake_period >= 1296000 and stake_period < 2592000:
        while y < amount:
            y += 1
            x = 0
            while x < seconds:
                x += 1
                total_rewards += 0.00008102
    else:
        while y < amount:
            y += 1
            x = 0
            while x < seconds:
                x += 1
                total_rewards += 0.00011574
    await update_reward(wallet_id, total_rewards)


async def UpdateClaim(wallet_id, amount_claimed, claimed_rewards):
    claimed = claimed_rewards + amount_claimed
    await UpdatedClaimed(wallet_id, claimed)

#ADD ROLE PER AMOUNT
async def HolderChecker():
    all_holders = await get_all_holders()
    for holder in all_holders:
        wallet_id = holder['wallet_id']
        discord_id = holder['discord_id']
        holder_info = NFTCheck(wallet_id)
        status = holder_info[0]
        amount = holder_info[1]
        await update_holder(wallet_id, status, amount)
        await UpdateStaking(wallet_id)
        if status == "ACTIVE":
            await AddRole(discord_id)
        if status == "INACTIVE":
            await RemoveRole(discord_id)
            await remove_holder(wallet_id)

