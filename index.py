MESSAGES_TRIGGER = 3 # how many messages all in unique channels
DURATION_TRIGGER = 5 # the time in which all messages must be sent for it to flag

import discord
import time
from bottoken import TOKEN

# message definition
class SpamMessageView(discord.ui.DesignerView):
    def __init__(self, msg: discord.Message):
        super().__init__(timeout=None)

        container = discord.ui.Container(color=discord.Color.from_rgb(222, 40, 65))

        container.add_text("your account was automatically flagged by a scam detection system because you sent too many messages across too many channels in a short amount of time. once you've gained access to your account (or if this was an error) then feel free to rejoin the server.")

        container.add_text(f"the server in question: `{msg.guild.name}`")

        self.add_item(container)

# Setup bot
bot = discord.Bot(
    intents=discord.Intents(messages=True, guilds=True)
)

message_cache = []

@bot.event
async def on_message(msg: discord.Message):
    global message_cache
    if msg.author.bot or not msg.guild or msg.snapshots:
        return
    
    # get basic info
    user_id = msg.author.id
    current_time = time.time()
    channel_id = msg.channel.id

    # remove old messages from cache
    message_cache = list(filter(lambda m: (current_time - m['time']) <= DURATION_TRIGGER, message_cache))

    # add new message to cache
    message_cache.append({
        "user_id":user_id,
        "time":current_time,
        "channel_id":channel_id
    })

    # detect spam (3+ messages in 3+ channels in cache)
    from_user = list(filter(lambda m: m["user_id"] == user_id, message_cache))
    
    if len(from_user) < MESSAGES_TRIGGER: # skip if less than 3 recent messages
        return
    
    different_channels = len({item['channel_id'] for item in from_user}) == len(from_user) # if amount of channels is equal to amount of messages then they are all in different channels

    if not different_channels: # skip if they're in the same channel
        return
    
    print(f"user {msg.author.global_name} triggered scam detector in server {msg.guild.name}")
    
    try:
        await msg.author.send(view=SpamMessageView(msg)) # send user notice
    except Exception as err: 
        print("error on message send: " + str(err.args))
        pass

    # remove users messages from cache
    message_cache = list(filter(lambda m: m["user_id"] != user_id, message_cache))

    # softban to remove messages
    try:
        await msg.author.ban(delete_message_seconds=30,reason="scamn't detected that this user sent 3 messages in 3 channels in 5 seconds")
        await msg.author.unban(reason="Spam detection system")
    except Exception as err:
        print("error on ban: " + str(err.args))
        await msg.reply("-# scamn't couldn't softban this user. please double check that i have permission to ban members!",allowed_mentions=discord.AllowedMentions(replied_user=False, roles=False,everyone=False))

    # try:
    #     await msg.guild.get_channel(variables.modlogs).send(embed=discord.Embed(
    #         title="User Softbanned",
    #         description=f"{msg.author.name} (UID {msg.author.id}) was softbanned.",
    #         colour=discord.Colour.red(),
    #     )
    #     .set_author(name="Spam detection system")
    #     .add_field(name="Reason",value="Flagged by spam detection system for sending 3 messages across 3 channels within 7 seconds.",inline=False)
    #     .add_field(name="Message",value=f"```\n{content}\n\n({len(msg.attachments)} attachments)```",inline=False)
    #     )
    # except:
    #     pass

# logging purposes
@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f"i was added to '{guild.name}'")

@bot.event
async def on_guild_removed(guild: discord.Guild):
    print(f"i was removed from guild '{guild.name}'")

bot.run(TOKEN)