import json
import requests
import hikari


def TokenTracker(wallet_id):
    col_url = "https://api-mainnet.magiceden.dev/v2/wallets/" + str(wallet_id) + "/tokens?offset=0&limit=100&listStatus=both"
    url_col_info = requests.get(col_url)
    collection_data = json.loads(url_col_info.text)


    token_embed = hikari.Embed(
        title="**TOKENS IN \n**" + str(wallet_id.upper()),
        color="#996515",
    )
    token_embed.set_footer(f"Toast or DIE")
    for token in collection_data:
        collection = "NO COLLECTION"
        if "collectionName" in token:
            collection = token["collectionName"]
        name = token["name"]
        image = token["image"]
        token_embed.set_thumbnail(image)
        token_embed.add_field(name=collection,value=name,inline=True)
        
    return token_embed

#NEEDS COMPLETION
def ActivityTracker(wal):
        colUrl = "https://api-mainnet.magiceden.dev/v2/wallets/" + str(wal) + "/activities?offset=0&limit=1"
        urlColInfo = requests.get(colUrl)
        collectionData = json.loads(urlColInfo.text)
        return collectionData