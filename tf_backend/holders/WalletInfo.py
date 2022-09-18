from datetime import datetime, timezone
from tf_backend.data.db_access import remove_holder, update_holder, get_all_holders, get_holder, update_reward
from tf_backend.discord_bot.bot import AddRole, RemoveRole
from jsonrpcclient import request, parse, Ok
import requests


def NFTCheck(wallet_id):
    response_og = requests.post(
            "https://empty-radial-paper.solana-mainnet.discover.quiknode.pro/b445018a765524154d66d84417fca5130233526c/",
            json=request("qn_fetchNFTs", {
                "wallet": wallet_id,
                "omitFields": [
                    "provenance",
                    "traits",
                    "description",
                    "tokenAddress",
                    "imageUrl",
                    "chain",
                    "creators",
                    "network"
                ],
                "page": 1,
                "perPage": 1000
            })
        )
    parsed_og = parse(response_og.json())
    total_pages = parsed_og.result["totalPages"]
    page = 1
    count = 0
    Status = "INACTIVE"

    while page <= total_pages:
        response = requests.post(
            "https://empty-radial-paper.solana-mainnet.discover.quiknode.pro/b445018a765524154d66d84417fca5130233526c/",
            json=request("qn_fetchNFTs", {
                "wallet": wallet_id,
                "omitFields": [
                    "provenance",
                    "traits",
                    "description",
                    "tokenAddress",
                    "imageUrl",
                    "chain",
                    "creators",
                    "network"
                ],
                "page": page,
                "perPage": 1000
            })
        )
        parsed = parse(response.json())
        NFTs = parsed.result["assets"]
        page += 1
        for nft in NFTs:
            if nft["collectionAddress"] == '493ZbidfhGB51vkwBPtLUc6onMXFcRmsPkrNY9FJXQSR':
                count += 1
                if Status != "ACTIVE":
                    Status = "ACTIVE"

    return Status, count

async def ClaimStaking(wallet_id):
    await UpdateStaking(wallet_id)
    resp = await get_holder(wallet_id)
    total_rewards = resp["total rewards"]
    claimed_rewards = resp["claimed rewards"]
    claim_amount = total_rewards - claimed_rewards
    return claim_amount

async def UpdateStaking(wallet_id):
    resp = await get_holder(wallet_id)
    amount = int(resp["amount"])
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
    elif seconds >= 604800 and seconds < 1296000:
        while y < amount:
            y += 1
            x = 0
            while x < seconds:
                x += 1
                total_rewards += 0.00005787
    elif seconds >= 1296000 and seconds < 2592000:
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


#ADD ROLE PER AMOUNT
async def HolderChecker():
    all_holders = await get_all_holders()
    for holder in all_holders:
        wallet_id = holder['wallet_id']
        discord_id = holder['discord_id']
        holder_info = NFTCheck(wallet_id)
        status = holder_info[0]
        amount = holder_info[1]
        await update_holder(wallet_id, amount, status)
        await UpdateStaking(wallet_id)
        if status == "ACTIVE":
            await AddRole(discord_id)
        if status == "INACTIVE":
            await RemoveRole(discord_id)
            # await remove_holder(wallet_id)

