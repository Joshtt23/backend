import motor.motor_asyncio
import json
from bson import ObjectId, json_util

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://Joshtt23:Tyler03061998?!@Holder-DB:27017/Holders?authSource=admin")
db = client['Holders']
tf_holders=db["TF_Holders"]

async def add_holder(wallet_id, discord_id, amount):
    key = {'wallet_id':wallet_id}
    document={"$set":{'wallet_id': wallet_id, 'discord_id':discord_id, 'status':'ACTIVE', 'amount':amount}}
    await tf_holders.update_one(key, document, upsert=True)
    result = await get_holder(wallet_id)
    return result

async def get_holder(wallet_id):
    document = await tf_holders.find_one({'wallet_id':wallet_id})
    return json.loads(json_util.dumps(document))

async def update_holder(wallet_id, amount, discord_id):
    #update doc based on wallet
    await tf_holders.update_one(
        {'wallet_id':wallet_id},
        {'$set': 
            {'discord_id':discord_id,
            'amount':amount
            }
        })
    result = get_holder(wallet_id)
    return result

async def remove_holder(wallet_id):
    await tf_holders.delete_one({'wallet_id': wallet_id})

async def get_all_holders():
    holders = []
    async for document in tf_holders.find():
        holders.append(document)

    return json.loads(json_util.dumps(holders))
