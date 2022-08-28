import logging
import motor.motor_asyncio
import json
from bson import ObjectId, json_util
#for production
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://Joshtt23:Tyler03061998?!@Holder-DB:27017/Holders?authSource=admin")
#for development
# client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client['Holders']
tf_holders=db["TF_Holders"]

async def add_holder(wallet_id, discord_id, status, amount):
    key = {'wallet_id':wallet_id}
    document={"$set":{'wallet_id': wallet_id, 'discord_id':discord_id, 'status':status, 'amount':amount}}
    await tf_holders.update_one(key, document, upsert=True)
    result = await get_holder(wallet_id)
    return result

async def get_holder(wallet_id):
    document = await tf_holders.find_one({'wallet_id':wallet_id})
    if document is None:
        return "No Holder Found!"
    else:
        return json.loads(json_util.dumps(document))

async def update_holder(wallet_id, amount, status):
    #update doc based on wallet
    await tf_holders.update_one(
        {'wallet_id':wallet_id},
        {'$set': 
            {
            'amount':amount,
            'status':status,
            }
        })

async def remove_holder(wallet_id):
    await tf_holders.delete_one({'wallet_id': wallet_id})

async def get_all_holders():
    holders = []
    cursor = tf_holders.find()
    async for holder in  cursor:
        # holder = json.loads(json_util.dumps(document))
        holders.append(holder)
        # holders.append(holder)
    return holders
