import datetime
import hikari
import lightbulb
import os


bot = lightbulb.BotApp(
    token=os.environ['TOKEN'],
    default_enabled_guilds=int(os.environ['DEFAULT_GUILD_ID']),
    help_slash_command=False,
)


@bot.command
@lightbulb.option("nft", "Image of NFT", type=hikari.Attachment)
@lightbulb.option("url", "MagicEden link for collection", type=str)
@lightbulb.option("collection", "The collection name", type=str)
@lightbulb.option("startbid", "This will be the opening bid for the auction", type=float)
# @lightbulb.option("quitetime", "This will be the period the bot waits without receiving a bid to start countdown.", type=int)
@lightbulb.option("prize", "The prize being auctioned off", type=str)
@lightbulb.command("startauction", "This will initialize a auction.")
@lightbulb.implements(lightbulb.SlashCommand)
async def start_auction(ctx):
    bot.d.bid = ctx.options.startbid
    # bot.d.wait_time = ctx.options.quitetime
    bot.d.prize = ctx.options.prize
    nft = ctx.options.nft
    collection = ctx.options.collection
    url = ctx.options.url
    startEmbed = (
        hikari.Embed(
                        title=f"**The auction will begin shortly**",
                        color="#996515",
                        
                    ) 
                    .set_thumbnail(
                        nft
                    )
                    .set_footer(
                        text=f"Powered by TOAST",
                    )
                    .add_field(
                        name="***Prize:***",
                        value=f"{bot.d.prize}"
                    )
                    .add_field(
                        name="***Starting Bid:***",
                        value=f"{ctx.options.startbid} OSARU"
                    )
                    .add_field(
                        name="***Collection:***",
                        value=f"[{collection}]({url})"
                    )
                    
                )
    actRow = (
        bot.rest.build_action_row()

        .add_button(hikari.ButtonStyle.SUCCESS, (f"start"))
            .set_label("Start Auction")
            .add_to_container()
    
    )
    await ctx.respond(content=startEmbed,component= actRow )

@bot.listen(hikari.InteractionCreateEvent)
async def add_bid(event: hikari.InteractionCreateEvent) -> None:
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return
    if event.interaction.custom_id == "start":
        user_roles = event.interaction.member.role_ids
        if 941508613724332052 in user_roles:
            await event.interaction.create_initial_response(
                hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,  # Create a new message as response to this interaction
            )
            updateEmbed = (
            hikari.Embed(
                            title=f"**The Auction has begun**",
                            color="#996515",
                            
                        ) 
                        .set_footer(
                            text=f"Powered by TOAST",
                        )
                        .add_field(
                            name="**Prize:**",
                            value=f"{bot.d.prize}"
                        )
                        .add_field(
                            name="**Starting Bid:**",
                            value=f"{bot.d.bid} OSARU"
                        )
                    )
            actRow = (
                bot.rest.build_action_row()

                .add_button(hikari.ButtonStyle.SUCCESS, (f"add250"))
                    .set_label("+250")
                    .add_to_container()
            
                .add_button(hikari.ButtonStyle.SUCCESS, (f"add500"))
                    .set_label("+500")
                    .add_to_container()
            
                .add_button(hikari.ButtonStyle.SUCCESS, (f"add750"))
                    .set_label("+750")
                    .add_to_container()
            
                .add_button(hikari.ButtonStyle.SUCCESS, (f"add1000"))
                    .set_label("+1000")
                    .add_to_container()
            )
            await event.interaction.message.edit(
            content=updateEmbed,
            component=actRow
            )
        else:
            await event.interaction.create_initial_response(
                
                hikari.ResponseType.MESSAGE_CREATE,  # Create a new message as response to this interaction
                "You dont have authority to do that!",  # Message content
                flags=hikari.MessageFlag.EPHEMERAL  # Ephemeral message, only visible to the user who pressed the button
            )
    else:
        await event.interaction.create_initial_response(
                hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,  # Create a new message as response to this interaction
            ) 
        if event.interaction.custom_id == f"add250":
            bot.d.bid = bot.d.bid + 250
            bot.d.bidder = event.interaction.user.username
        elif event.interaction.custom_id == f"add500":
            bot.d.bid = bot.d.bid + 500
            bot.d.bidder = event.interaction.user.username
        elif event.interaction.custom_id == f"add750":
            bot.d.bid = bot.d.bid + 750
            bot.d.bidder = event.interaction.user.username
        elif event.interaction.custom_id == f"add1000":
            bot.d.bid = bot.d.bid + 1000
            bot.d.bidder = event.interaction.user.username

        updateEmbed = (
            hikari.Embed(
                            title=f"**The Auction has begun**",
                            color="#996515",
                            
                        ) 
                        .set_footer(
                            text=f"Powered by TOAST",
                        )
                        .add_field(
                            name="**Prize:**",
                            value=f"{bot.d.prize}"
                        )
                        .add_field(
                            name="**Current Bid:**",
                            value=f"{bot.d.bid} OSARU"
                        )
                        .add_field(
                            name="**Bidder:**",
                            value=f"{bot.d.bidder}"
                        )
                        
                    )
        actRow = (
            bot.rest.build_action_row()

            .add_button(hikari.ButtonStyle.SUCCESS, (f"add250"))
                .set_label("+250")
                .add_to_container()
        
            .add_button(hikari.ButtonStyle.SUCCESS, (f"add500"))
                .set_label("+500")
                .add_to_container()
        
            .add_button(hikari.ButtonStyle.SUCCESS, (f"add750"))
                .set_label("+750")
                .add_to_container()
        
            .add_button(hikari.ButtonStyle.SUCCESS, (f"add1000"))
                .set_label("+1000")
                .add_to_container()
        )
        await event.interaction.message.edit(
            content=updateEmbed,
            component=actRow
        )    

@bot.command
@lightbulb.command("endauction", "This will end a auction and delete countdown.")
@lightbulb.implements(lightbulb.SlashCommand)
async def end_auction(ctx):
    messages = (
        await bot.rest.fetch_messages(ctx.channel_id)
        .take_until(lambda m: datetime.datetime.now(datetime.timezone.utc)- datetime.timedelta(days=14)>m.created_at)
        .limit(12)
    )
    await bot.rest.delete_messages(ctx.channel_id, messages)
    # remove 12 messages
    end_embed = (
        hikari.Embed(
                        title=f"**The auction has ended**",
                        color="#996515",
                        
                    ) 
                    .set_footer(
                        text=f"Powered by TOAST",
                    )
                    .add_field(
                        name="**Prize:**",
                        value=f"{bot.d.prize}"
                    )
                    .add_field(
                        name="**Ending Bid:**",
                        value=f"{bot.d.bid} OSARU"
                    )
                    .add_field(
                        name="**Winner:**",
                        value=f"{bot.d.bidder}"
                    )
                )
    await ctx.respond(content=end_embed)

def run() -> None:
    if os.name != 'nt':
        import uvloop
        uvloop.install()
    bot.run()