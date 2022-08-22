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
                    url=url,
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
@lightbulb.option('role', 'Role to give')
@lightbulb.command('verify', 'Send verify embed')
@lightbulb.implements(lightbulb.SlashCommand)
async def verify(ctx):
    callChannel= ctx.channel_id
    verifyEmbed = (
        hikari.Embed(
                        title="**Welcome to Toasty Friends!**",
                        color="#996515",
                    )
                    .set_thumbnail(
                        
                    )   
                    .set_footer(
                        text=f"Toast or DIE",
                    )
                    .add_field(
                        name="***VERIFY HERE***",
                        value="\nClick <:Toast_Gang:963520515924975616> below to gain access to our server!\n\n Thank you for joining and make sure to check out <#938861568739922012> and <#938861849867321414>\n"
                    )
                    .add_field(
                        name="***NO JOBS/POSITIONS/ROLES AVAILABLE***",
                        value='Thank you!'
                    )
                )
    actRow = (
        bot.rest.build_action_row()

        .add_button(hikari.ButtonStyle.SUCCESS, ("role"))
            .set_label("")
            .set_emoji(963520515924975616)
            .add_to_container()
    )
    await bot.rest.create_message(callChannel, content=verifyEmbed,component= actRow )

@bot.listen(hikari.InteractionCreateEvent)
async def on_component_interaction(event: hikari.InteractionCreateEvent) -> None:
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return

    if event.interaction.custom_id == "role":
        await event.interaction.member.add_role(942137787149352990)
        await event.interaction.create_initial_response(
            
            hikari.ResponseType.MESSAGE_CREATE,  # Create a new message as response to this interaction
            "You have been verified!",  # Message content
            flags=hikari.MessageFlag.EPHEMERAL  # Ephemeral message, only visible to the user who pressed the button
        )

@bot.command
@lightbulb.option('sinnerrole', 'Role to give')
@lightbulb.command('addrole', 'Send sinner role embed')
@lightbulb.implements(lightbulb.SlashCommand)
async def verify(ctx):
    callChannel= ctx.channel_id
    verifyEmbed = (
        hikari.Embed(
                        title="**GET PINGED BY SINNER SIGNAL**",
                        color="#996515",
                    )
                    .set_thumbnail(
                        
                    )   
                    .set_footer(
                        text=f"Toast or DIE",
                    )
                    .add_field(
                        name="***ADD ROLE***",
                        value="\nClick below to be pinged on all new signals!"
                    )
                )
    actRow = (
        bot.rest.build_action_row()

        .add_button(hikari.ButtonStyle.SUCCESS, ("signalrole"))
            .set_label("Add Signal Role")
            .add_to_container()
    )
    await bot.rest.create_message(callChannel, content=verifyEmbed,component= actRow )

@bot.listen(hikari.InteractionCreateEvent)
async def on_component_interaction(event: hikari.InteractionCreateEvent) -> None:
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return

    if event.interaction.custom_id == "signalrole":
        await event.interaction.member.add_role(1010611851517759549)
        await event.interaction.create_initial_response(
            
            hikari.ResponseType.MESSAGE_CREATE,  # Create a new message as response to this interaction
            "You have been added!",  # Message content
            flags=hikari.MessageFlag.EPHEMERAL  # Ephemeral message, only visible to the user who pressed the button
        )

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

    



def run() -> None:
    if os.name != 'nt':
        import uvloop
        uvloop.install()
    bot.run()