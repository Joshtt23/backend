import hikari
import lightbulb
import os
import string
from tf_backend.discord_bot.extensions.col_stats import ColStats, HistStats
from tf_backend.discord_bot.extensions.tweet_tracker import GetMentions, GetName, GetUserId, SearchTweets
from tf_backend.discord_bot.extensions.wallet_tracker import TokenTracker
from tf_backend.discord_bot.extensions.wallets import create_account, fund_account, get_balance, send_sol
from tf_backend.discord_bot.extensions.pph_tracker import Paper_Tracker
from lightbulb.ext import tasks


bot = lightbulb.BotApp(
    token=os.environ['TOKEN'],
    default_enabled_guilds=int(os.environ['DEFAULT_GUILD_ID']),
    help_slash_command=True,
    # intents = hikari.Intents.ALL,
)

tasks.load(bot)

@tasks.task(
    s=15, auto_start=True, 
    wait_before_execution=False, 
    pass_app=True
    )
async def bgph(app):
    async for listing in Paper_Tracker():
        try:
            price = str(listing["price"]/1000000000)
            col_name = str(listing["collection_name"])
            col_key = str(listing["mint"])
        except:
            print("No paper here!")
        else:
            if listing['marketplace']== 'MagicEden V2':
                url = "https://magiceden.io/item-details/" + col_key
            else:
                url = "https://coralcube.io/detail/" + col_key
            paper_embed = (
                hikari.Embed(
                    title="**PAPER FOUND**",
                    color="#996515",
                ))
            paper_embed.set_thumbnail(
                listing["image"]
            )   
            paper_embed.set_footer(
                text=f"Toast or DIE",
            )
            paper_embed.add_field(
                name="Collection:",
                value=col_name
            )
            paper_embed.add_field(
                name="Price:",
                value=price
            )
            paper_embed.add_field(
                name=f"\u200b",
                value=f"[BUY NOW]({url})"
            )
            
            
        await bot.rest.create_message(996588760860991518, content=paper_embed)

@bot.command
@lightbulb.command('create', 'create a Solana wallet')
@lightbulb.implements(lightbulb.SlashCommand)
async def create(ctx):
    sender_username = ctx.author.username
    resp = create_account(sender_username)
    await ctx.respond(resp)

@bot.command
@lightbulb.option("sol", "amount of sol >=2", type=float)
@lightbulb.command('fund', 'Fund your Solana wallet (devnet)')
@lightbulb.implements(lightbulb.SlashCommand)
async def fund(ctx):
    sender_username = ctx.author.username
    amount = ctx.options.sol
    resp = fund_account(sender_username, amount)
    await ctx.respond(resp)

@bot.command
@lightbulb.command("bal", "Balance of your account")
@lightbulb.implements(lightbulb.SlashCommand)
async def bal(ctx):
    sender_username = ctx.author.username
    resp = get_balance(sender_username)
    await ctx.respond(resp)


@bot.command
@lightbulb.option("amount", "Amount of SOL to send", type=float)
@lightbulb.option("account", "Public Key to send to")
@lightbulb.command("send", "Send SOL to account.")
@lightbulb.implements(lightbulb.SlashCommand)
async def send(ctx):
    sender_username = ctx.author.username
    amount = ctx.options.amount
    receiver = ctx.options.account
    emb_proc = (
        hikari.Embed(
            title="**Toasty Friends**",
            color="#996515",
        )

        .set_footer(
            text=f"Toast or DIE",
        )
        .add_field(
            name="Status",
            value=f'Sending {amount} SOL'
        )
        .add_field(
            name="Receiver",
            value=receiver,
        )
    )
    og_message = await ctx.respond(emb_proc)
    resp = send_sol(sender_username, amount, receiver)
    await og_message.edit(resp)

@bot.command
@lightbulb.option('wallet', 'The ID of wallet to check.')
@lightbulb.command('tokens', 'Track a wallets actions.')
@lightbulb.implements(lightbulb.SlashCommand)
async def tokens(ctx):
    wallet_id = ctx.options.wallet
    resp = TokenTracker(wallet_id)  
    await ctx.respond(resp)

@bot.command
@lightbulb.option('username', 'Project username')
@lightbulb.command('tweets', 'Track a tweets containing project names.')
@lightbulb.implements(lightbulb.SlashCommand)
async def tweets(ctx):
    username = ctx.options.username
    try:
        name = GetName(username)
        user_id = GetUserId(username)
        polarity = SearchTweets(username)
        mentions = GetMentions(user_id)
    except:
        twitter_embed = (
            hikari.Embed(
                            title="**" + username + "**",
                            color="#996515",
                        )
                        .set_footer(
                            text=f"Toast or DIE",
                        )
                        .add_field(
                            name="***DOES NOT EXIST***",
                            value="Please, check username on twitter.",
                            inline=True
                        )
                        
                    )
    else:
        twitter_embed = (
            hikari.Embed(
                            title="**" + name + "**",
                            color="#996515",
                        )
                        .set_footer(
                            text=f"Toast or DIE",
                        )
                        .add_field(
                            name="***Mentions***",
                            value=mentions,
                            inline=True
                        )
                        .add_field(
                            name="***Polarity Score***",
                            value=polarity,
                            inline=True
                        )
                    )
    await ctx.respond(twitter_embed)


@bot.command
@lightbulb.option('col', 'Collection name.', type=string)
@lightbulb.command('stats', 'Find floor of collection')
@lightbulb.implements(lightbulb.SlashCommand)
async def stats(ctx):
    col = ctx.options.col
    col = col.replace(" ", "_")
    col = col.lower()

    resp= ColStats(col)
    resp = await HistStats(col, resp)

    await ctx.respond(resp)

@bot.command
@lightbulb.option('role', 'Role to give')
@lightbulb.command('roleadder', 'Send sinner role embed')
@lightbulb.implements(lightbulb.SlashCommand)
async def roleadder(ctx):
    callChannel= ctx.channel_id
    role = ctx.options.role
    verifyEmbed = (
        hikari.Embed(
                        title=f"**GET YOUR NEW ROLE**",
                        color="#996515",
                        
                    ) 
                    .set_footer(
                        text=f"Toast or DIE",
                    )
                    .add_field(
                        name="***ADD ROLE***",
                        value=f"\nClick below to get {role} role"
                    )
                )
    roleparse = role[3:-1]
    actRow = (
        bot.rest.build_action_row()

        .add_button(hikari.ButtonStyle.SUCCESS, (f"add{roleparse}"))
            .set_label("Add/Remove Role")
            .add_to_container()
    )
    await bot.rest.create_message(callChannel, content=verifyEmbed,component= actRow )
    await ctx.respond(f"Role adder successfully created for {role}")

@bot.listen(hikari.InteractionCreateEvent)
async def on_component_interaction(event: hikari.InteractionCreateEvent) -> None:
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return
    role = int(event.interaction.custom_id[3:]) #returns id of role parse to number
    if event.interaction.custom_id == f"add{role}":
        userroles = event.interaction.member.role_ids
        if role in userroles:
            await event.interaction.member.remove_role(role) #This is where the role needs to be imported
            await event.interaction.create_initial_response(
                
                hikari.ResponseType.MESSAGE_CREATE,  # Create a new message as response to this interaction
                "You have been removed!",  # Message content
                flags=hikari.MessageFlag.EPHEMERAL  # Ephemeral message, only visible to the user who pressed the button
            )
        else:
            await event.interaction.member.add_role(role) #This is where the role needs to be imported
            await event.interaction.create_initial_response(
                
                hikari.ResponseType.MESSAGE_CREATE,  # Create a new message as response to this interaction
                "You have been added!",  # Message content
                flags=hikari.MessageFlag.EPHEMERAL  # Ephemeral message, only visible to the user who pressed the button
            )

async def AddRole(discord_id):
    await bot.rest.add_role_to_member(guild='899757430211223642',user=discord_id, role='1002246971966365736')

async def RemoveRole(discord_id):
    await bot.rest.remove_role_from_member(guild='899757430211223642',user=discord_id, role='1002246971966365736')


def run() -> None:
    if os.name != 'nt':
        import uvloop
        uvloop.install()
    bot.run()