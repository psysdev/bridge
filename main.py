import discord

from config import token , gc_id , wc_id , rc_id , hnfc_id

welcome_channel = None
general_channel = None
rules_channel = None
hnf_channel = None

channels_ready = False

intents = discord.Intents.default()
"""
This creates an intents configuration.
Intents are permissions for receiving event categories.
Using default intents as we don't need every possible event.

We explicity enable the members intent.
"""
intents.members = True
client = discord.Client(intents=intents)
"""
discord.Client() creates our client.
intents=intents configures which intents the client should receive.

Client can be understood as the main object that controls our bot.

client is essential as event decorators need an existing client to register
handlers on.
"""

@client.event
async def on_ready():
    global welcome_channel
    global general_channel
    global rules_channel
    global hnf_channel
    global channels_ready 

    channels_ready = False
    """
    We reset the flag and the channel references so that whenever on_ready is called again, no redundant
    reference survives.
    """
    welcome_channel = None
    general_channel = None
    rules_channel = None
    hnf_channel = None

    """
    global keyword is used as we're assigning values to variables defined outside
    of the function.

    Without global keyword, Python treats those variables as local variables.
    """
    print(f"Logged in as {client.user}")
    """
    Updated handling to have channels be accessible
    Channels are only accessible once they are cached after the bot starts.
    If channels are not cached ,get_channel can return a None value.
    """
    try:
        new_welcome_channel = (client.get_channel(wc_id) or  await client.fetch_channel(wc_id))
        new_general_channel = (client.get_channel(gc_id) or await client.fetch_channel(gc_id))
        new_rules_channel = (client.get_channel(rc_id) or await client.fetch_channel(rc_id))
        new_hnf_channel = (client.get_channel(hnfc_id) or await client.fetch_channel(hnfc_id))

        channels = {
            "Welcome": (new_welcome_channel, discord.TextChannel),
            "General": (new_general_channel,discord.TextChannel),
            "Rules": (new_rules_channel,discord.TextChannel),
            "Feedback": (new_hnf_channel,(discord.ForumChannel,discord.Thread))
        }

        for name , (channel , expected_type) in channels.items():
            if not isinstance(channel, expected_type):
                raise RuntimeError(
                    f"{name} channel has an unexpected type!"
                )
        """
        new_channelname_chanel has been used earlier to ensure
        INITIALIZATION BEFORE ASSIGNMENT.

        This ensures we retrieve and validate everything using temporary variables.
        Only after all validations succeed do we assign the global references.

        This prevents global references from being left partially initialized.
        """
        general_channel = new_general_channel
        rules_channel = new_rules_channel
        hnf_channel = new_hnf_channel
        welcome_channel = new_welcome_channel
        print("All channels initialized successfully!")
        print("Bot is live!")
        channels_ready = True
    except (discord.HTTPException, RuntimeError) as error:
        print(f"Channel initialization failed: {error}")
"""
@client.event

this descorator registers a function as an event handler.

on_ready()

this event runs when the bot  has successfully connected and is ready.

client.user

This is used to fetch information about the account to which the bot is connected.
"""

@client.event
async def on_member_join(member):
    print("\n--- New Member Joined ---")
    print(f"{member.name} joined the server!")
    print(f"Username: {member.name}")
    print(f"Display name: {member.display_name}")
    print(f"User id: {member.id}")
    print(f"Server: {member.guild.name}")
    if channels_ready:
        try:
            await welcome_channel.send(
            f"Welcome to the server, {member.mention}. \n\n"
            f"Familiarise yourself with {rules_channel.mention}.\n"
            f"{general_channel.mention} and " 
            f"{hnf_channel.mention} are available for posting. "
            )
            print("Public welcome message delivered!")
        except discord.Forbidden as error:
            print(f"Missing permissions: {error}")
        except discord.HTTPException as error:
            print(f"Public welcome message failed: {error}")
    else:
        print("Channels not initialized. Skipping public welcome.")
    try:
        await member.send(
            f"Hey {member.display_name}! Welcome to the server!"
        )
        print(f"Welcome DM sent to {member.name}")
    except discord.Forbidden:
        print(f"Could not DM {member.name}")
    except discord.HTTPException as error:
        print(f"DM failed: {error}")
"""
on_member_join

the event name recognised by discord.py

member

the object representing the person who just joined

member.name 

the data member containing the name within the member objects
"""

client.run(token)

"""
Member data object 

member.name          # Username
member.display_name  # Server display name
member.id            # Unique Discord user ID
member.mention       # Mention the member in Discord
member.avatar        # Member's avatar
member.guild         # Server they joined
"""