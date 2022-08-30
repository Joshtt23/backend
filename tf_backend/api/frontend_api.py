from quart import Quart, jsonify, request, sessions, redirect
from quart_cors import cors
from tf_backend.discord_bot.bot import RemoveRole
from tf_backend.discord_bot.bot import AddRole
from tf_backend.holders.WalletInfo import NFTCheck, ClaimStaking
from tf_backend.api.config import CLIENT_SECRET, REDIRECT_URI, TOKEN

from tf_backend.data.db_access import add_holder, get_holder

app = Quart(__name__)
# app.config["SECRET_KEY"] = 'ToastyFriendsGang4Lyfe'
app = cors(app, allow_origin="*")
    

@app.route("/set_holder", methods=["POST"])
async def SetHolder():
    wallet_id = request.args.get("wallet_id")
    discord_id = request.args.get("discord_id")
    holder_info = NFTCheck(wallet_id)
    status = holder_info[0]
    amount = holder_info[1]
    resp = await add_holder(wallet_id, discord_id, status, amount)
    if status == "ACTIVE":
        await AddRole(discord_id)
    if status == "INACTIVE":
        await RemoveRole(discord_id)
    return resp


@app.route("/holder/<wallet_id>")
async def holder(wallet_id):
    holder = await get_holder(wallet_id)
    return holder

@app.route("/test")
async def Test():
    return "It works"

@app.route("/claim")
async def claim():
    wallet_id = request.args.get("wallet_id")
    claim = await ClaimStaking(wallet_id)
    return str(claim)



def run() -> None:
    app.run()