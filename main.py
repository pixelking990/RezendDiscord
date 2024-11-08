import discord

import textwrap
import urllib

import datetime
import os
import json
import praw

import aiohttp
import asyncio
import akinator
import requests
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from discord.ext import commands
import keep_alive
import random
from keep_alive import keep_alive
from discord.ext import commands, tasks

from itertools import cycle
from requests import get
from discord_components import Button, Select, SelectOption, ComponentsBot

from discord.ext import commands
from akinator.async_aki import Akinator
from setup import token, channel_id
from discord.ext.commands import BucketType

from pytimeparse.timeparse import timeparse

client = commands.Bot(command_prefix=".")
bot = ComponentsBot(".")

status = cycle(
    ['New Features Every Month :)', 'Rezend is cool', 'New Website!'])


@tasks.loop(seconds=8)
async def change_status():
    await client.change_presence(status=discord.Status.dnd,
                                 activity=discord.Game(next(status)))

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


@client.command()
async def send_anonymous_dm(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)





@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title=f"✅ {amount} Messages Cleared ✅",
                          color=0x9522c9,
                          timestamp=ctx.message.created_at)
    await ctx.send(embed=embed)


@client.command(aliases=['l', 'ly', 'lyric'])
async def lyrics(ctx, *, search=None):
    """A command to find lyrics easily!"""
    if not search:
        embed = discord.Embed(
            title="No search argument!",
            description=
            "You havent entered anything, so i couldnt find lyrics!",
            color=0x9522c9)
        return await ctx.reply(embed=embed)

    song = urllib.parse.quote(search)  #

    async with aiohttp.ClientSession() as lyricsSession:
        async with lyricsSession.get(
                f'https://some-random-api.ml/lyrics?title={song}') as jsondata:
            if not 300 > jsondata.status >= 200:
                return await ctx.send(
                    f'Recieved poor status code of {jsondata.status}')

            lyricsData = await jsondata.json()

    error = lyricsData.get('error')
    if error:
        return await ctx.send(f'Recieved unexpected error: {error}')

    songLyrics = lyricsData['lyrics']  # the lyrics
    songArtist = lyricsData['author']  # the author's name
    songTitle = lyricsData['title']  # the song's title
    songThumbnail = lyricsData['thumbnail'][
        'genius']  # the song's picture/thumbnail

    for chunk in textwrap.wrap(songLyrics, 4096, replace_whitespace=False):
        embed = discord.Embed(title=songTitle,
                              description=chunk,
                              color=0x9522c9,
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=songThumbnail)
        await ctx.send(embed=embed)


@client.event
async def on_ready():
    print(f"Connected to {client.user}")
    change_status.start()


@client.command()
async def pfp(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    embed = discord.Embed(title=f'{member}',
                          color=0x9522c9,
                          timestamp=ctx.message.created_at)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def cointoss(ctx):
    messages = ["Head", "Tail"]
    embed = discord.Embed(title="Coin Flip",
                          url="",
                          description=random.choice(messages),
                          color=0x9522c9)
    embed.set_thumbnail(
        url="https://thumbs.gfycat.com/BabyishShrillKomododragon-max-1mb.gif")
    await ctx.send(embed=embed)


@client.command()
async def rolldice(ctx):
    messages = [
        "The dice landed with 1", "The dice landed with 2",
        "The dice landed with 3", "The dice landed with 4",
        "The dice landed with 5", "The dice landed with 6"
    ]
    embed = discord.Embed(title="Roll a Dice",
                          url="",
                          description=random.choice(messages),
                          color=0x9522c9)
    embed.set_thumbnail(
        url=
        "https://cdn.dribbble.com/users/6059148/screenshots/14425859/media/3f67e0e620f3818a68a03fdb874b7a56.gif"
    )
    await ctx.send(embed=embed)


@client.command(aliases=["8ball"])
async def eball(ctx):

    messages = [
        "🎱 Yep,sure why not", "🎱 Nah, you are too dumb", "🎱 Never ever",
        "🎱 Yes, but I am not sure ", "🎱 No lol", "🎱 Yes????",
        "🎱IDK, dont ask me"
        "Ur Mom"
    ]
    embed = discord.Embed(title="8ball",
                          url="",
                          description=random.choice(messages),
                          color=0x9522c9)
    embed.set_thumbnail(url="https://i.gifer.com/PTQh.gif")
    await ctx.send(embed=embed)


@client.command()
async def rickroll(ctx, member: discord.Member = None):
    if member == None:
        await ctx.send("Wait, who do you want me to rickroll? ahh!")
        await ctx.send("**Tip:** Try mentioning at someone lol!")
        return
    rick = "https://cdn.discordapp.com/attachments/812986360389697577/824967972971216926/tenor.gif"
    await ctx.send(
        f'**{member.name} got rickrolled by {ctx.author.name}, LMAO!**')
    await ctx.send(rick)


@client.command(aliases=["serverstat", "serverinfo"])
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(title=name + " Server Information",
                          description=description,
                          color=0x9522c9,
                          timestamp=ctx.message.created_at)
    embed.set_thumbnail(url=icon)
    embed.add_field(name=":crown:Owner", value=owner, inline=False)
    embed.add_field(name=":rocket:Server ID", value=id, inline=False)
    embed.add_field(name=":city_sunset: Region", value=region, inline=False)
    embed.add_field(name=":snowman2:Member Count",
                    value=memberCount,
                    inline=False)
    embed.set_footer(text=f"Provided by {client.user}",
                     icon_url=client.user.avatar_url)

    await ctx.send(embed=embed)


@client.command(aliases=["aboutuser"])
@commands.has_permissions(manage_messages=True)
async def userinfo(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    roles = [role for role in member.roles]

    embed = discord.Embed(colour=0x9522c9, timestamp=ctx.message.created_at)
    embed.set_author(name=f"User Info - {member}", icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author.name}",
                     icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id, inline=False)
    embed.add_field(name="Name:", value=member.name)
    embed.add_field(
        name="Created at:",
        value=member.created_at.strftime("%a, %#d, %B, %Y, %I:%M %p UTC"),
        inline=False)
    embed.add_field(
        name="Joined at:",
        value=member.joined_at.strftime("%a, %#d, %B, %Y, %I:%M %p UTC"),
        inline=False)

    embed.add_field(name="Roles",
                    value="".join([role.mention for role in roles]),
                    inline=False)

    embed.add_field(name="Top role:",
                    value=member.top_role.mention,
                    inline=False)

    embed.add_field(name="Bot?", value=member.bot, inline=False)

    await ctx.send(embed=embed)


@client.command()
async def about(ctx):
    embed = discord.Embed(
        title="About Rezend",
        url="",
        description=
        "Rezend is a minigame and multipurpose discord bot made by\n Dice Flip#1262 ,\n PixelKing#0441 ,\n NotDiscountLeafy#0999",
        color=0x9522c9)
    embed.set_thumbnail(
        url=
        "https://images-ext-2.discordapp.net/external/6PEiOTNFZy9MwEloJsoqZCdmgceN8qzBpTqKYQNIiOE/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/900996938495819776/6e78d2595d5130fd54b93caa26973c18.webp?width=378&height=378"
    )
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def meme(ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content, )
    meme = discord.Embed(
        title=f"{data['title']}",
        Color=discord.Color.random()).set_image(url=f"{data['url']}")
    await ctx.reply(embed=meme)


@client.command(aliases=["count", "botcount"])
async def servercount(ctx):
    embed = discord.Embed(title="Server Count",
                          url="",
                          description=("I'm in " + str(len(client.guilds)) +
                                       " Discord Servers."),
                          color=0x9522c9)
    embed.set_thumbnail(
        url=
        "https://cliply.co/wp-content/uploads/2021/08/372108630_DISCORD_LOGO_400.gif"
    )
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def kill(ctx):
    embed = discord.Embed(title="Take this bi**h",
                          url="",
                          description="Muhahahahhaa",
                          color=0x9522c9)
    embed.set_thumbnail(
        url=
        "https://images.squarespace-cdn.com/content/v1/51f01830e4b08d0b403ccef0/1380251234226-P7I3LRBZL62R6X03U4SL/ke17ZwdGBToddI8pDm48kJVRtKjA0PjKFTc3Ikwm1P9Zw-zPPgdn4jUwVcJE1ZvWEtT5uBSRWt4vQZAgTJucoTqqXjS3CfNDSuuf31e0tVEPjZsFPY_KQTC75ExbxVy3MVjw6wrNBclotoCzMu3MK6QvevUbj177dmcMs1F0H-0/EvShooting2.gif"
    )
    await ctx.send(embed=embed)


@client.command()
async def an(ctx):

    embed = discord.Embed(
        title="New Animal Commands",
        url="",
        description=
        "New 10+ animal commands added\n.cat    -      to show random pictures of cats\n.catfact  -      to show random facts of cats\n.dog   -      to show random pictures of dogs\n.dogfact  -      to show random facts of dogs\n.panda   -      to show random pictures of pandas\n.pandafact  -      to show random facts of pandas\n.fox   -      to show random pictures of foxes\n.foxfact  -      to show random facts of foxes\n.bird   -      to show random pictures of birds\n.birdfact  -      to show random facts of birds\n.koala   -      to show random pictures of koalas\n.koalafact  -      to show random facts of koala\n.raccoon  -      to show random pictures of raccoons\n.raccoonfact  -      to show random facts of raccoon\n\n**THIS UPDATE IS CURRENTLY LIVE**",
        color=0x9522c9)
    await ctx.send(embed=embed)


@client.command()
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/cat')
        dogjson = await request.json()
    embed = discord.Embed(title="Cats", color=discord.Color.red())
    embed.set_image(url=dogjson['link'])
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog'
                                    )  # Make a request
        dogjson = await request.json()  # Convert it to a JSON dictionary
    embed = discord.Embed(title="Doggo!",
                          color=discord.Color.red())  # Create embed
    embed.set_image(url=dogjson['link']
                    )  # Set the embed image to the value of the 'link' key
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)  # Send the embed


@client.command()
async def dogfact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/dog')
        factjson = await request.json()
    embed = discord.Embed(title="Dog Facts",
                          url="",
                          description=factjson['fact'],
                          color=0xe00d0d)
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def catfact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/cat')
        factjson = await request.json()
    embed = discord.Embed(title="Cat Facts",
                          url="",
                          description=factjson['fact'],
                          color=0xe00d0d)
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def panda(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/panda'
                                    )  # Make a request
        dogjson = await request.json()  # Convert it to a JSON dictionary
    embed = discord.Embed(title="Pandas",
                          color=discord.Color.red())  # Create embed
    embed.set_image(url=dogjson['link']
                    )  # Set the embed image to the value of the 'link' key
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)  # Send the embed


@client.command()
async def pandafact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/panda')
        factjson = await request.json()
    embed = discord.Embed(title="Panda Facts",
                          url="",
                          description=factjson['fact'],
                          color=0xe00d0d)
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def fox(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/fox'
                                    )  # Make a request
        dogjson = await request.json()  # Convert it to a JSON dictionary
    embed = discord.Embed(title="Fox!",
                          color=discord.Color.red())  # Create embed
    embed.set_image(url=dogjson['link']
                    )  # Set the embed image to the value of the 'link' key
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)  # Send the embed


@client.command()
async def foxfact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/fox')
        factjson = await request.json()
    embed = discord.Embed(title="Fox Facts",
                          url="",
                          description=factjson['fact'],
                          color=0xe00d0d)
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def bird(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/bird'
                                    )  # Make a request
        dogjson = await request.json()  # Convert it to a JSON dictionary
    embed = discord.Embed(title="Birds!",
                          color=discord.Color.red())  # Create embed
    embed.set_image(url=dogjson['link']
                    )  # Set the embed image to the value of the 'link' key
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)  # Send the embed


@client.command()
async def birdfact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/bird')
        factjson = await request.json()
    embed = discord.Embed(title="Bird Facts",
                          url="",
                          description=factjson['fact'],
                          color=0xe00d0d)
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def koala(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/koala'
                                    )  # Make a request
        dogjson = await request.json()  # Convert it to a JSON dictionary
    embed = discord.Embed(title="Koalas!",
                          color=discord.Color.red())  # Create embed
    embed.set_image(url=dogjson['link']
                    )  # Set the embed image to the value of the 'link' key
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)  # Send the embed


@client.command()
async def koalafact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/koala')
        factjson = await request.json()
    embed = discord.Embed(title="Koala Facts",
                          url="",
                          description=factjson['fact'],
                          color=0xe00d0d)
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def raccoon(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/raccoon'
                                    )  # Make a request
        dogjson = await request.json()  # Convert it to a JSON dictionary
    embed = discord.Embed(title="Raccoon!",
                          color=discord.Color.red())  # Create embed
    embed.set_image(url=dogjson['link']
                    )  # Set the embed image to the value of the 'link' key
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)  # Send the embed


@client.command()
async def raccoonfact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/raccoon')
        factjson = await request.json()
    embed = discord.Embed(title="Raccoon Facts",
                          url="",
                          description=factjson['fact'],
                          color=0xe00d0d)
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def hug(ctx, member: discord.Member = None):
    if member == None:
        await ctx.send("Wait, who do you want to hug? ahh!")
        await ctx.send("**Tip:** Try mentioning at someone lol!")
        return
    embed = discord.Embed(
        title=f'**{member.name}** got a hug from **{ctx.author.name}**!',
        url="",
        color=0x9522c9)
    embed.set_image(
        url="https://c.tenor.com/jtgk_sgtJuoAAAAC/milk-and-mocha-hugs.gif")
    await ctx.send(embed=embed)


@client.command()
async def joke(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/joke')
        jokejson = await request.json()
    embed = discord.Embed(title="Jokes",
                          url="",
                          description=jokejson['joke'],
                          color=0xe00d0d)
    embed.set_footer(text=f'Requested by {ctx.author.name}',
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def cattus(ctx):
    embed = discord.Embed(title="Cat Game",
                          url="",
                          description="Cat game coming this january!",
                          color=0x9522c9)
    embed.set_thumbnail(url="https://tenor.com/view/cool-cat-gif-18199666")
    await ctx.send(embed=embed)


@client.command()
async def guess(ctx):
    embed = discord.Embed(title='Number Guess',
                          description='Guess the number from 1 to 10!',
                          color=0x9522c9)
    embed.set_thumbnail(
        url='https://images-na.ssl-images-amazon.com/images/I/61BRwWBPKfL.png')
    await ctx.send(embed=embed)

    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    choice = random.choice(numbers)

    answer = await client.wait_for("message")

    if answer.content == choice:
        embed = discord.Embed(title='Number Guess',
                              description='You guessed the correct number!',
                              color=0x9522c9)
        embed.set_thumbnail(
            url=
            'https://images-na.ssl-images-amazon.com/images/I/61BRwWBPKfL.png')
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title='Number Guess',
                              description=f"You lost! The number was {choice}",
                              color=0x9522c9)
        embed.set_thumbnail(
            url=
            'https://images-na.ssl-images-amazon.com/images/I/61BRwWBPKfL.png')
        await ctx.send(embed=embed)


@client.command(name='create-channel')
@commands.has_permissions(administrator=True)
async def create_channel(ctx, *, channel_name=None):
    if channel_name == None:
        await ctx.send("What, you making fool of me?")
        await ctx.send("Type the channel's name also smarty!")
        return
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    await ctx.send(f"New channel {channel_name} created!")
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason=None):
    if member == None:
        await ctx.send("Who do you want to kick lol?")
        return

    if member == ctx.author:
        await ctx.send("You can't kick yourself dumb-dumb!")
        return
    if reason == None:
        await ctx.send(
            f"Reason required to kick {member.name} from this server!")
        return
    await member.kick(reason=reason)
    embed = discord.Embed(title=f"✅ {member} was kicked form this server! ✅",
                          timestamp=ctx.message.created_at)
    embed.add_field(name="Reason", value=reason)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if member == None:
        await ctx.send("Who do you want to ban lol?")
        return

    if member == ctx.author:
        await ctx.send("You can't ban yourself dumb-dumb!")
        return
    if reason == None:
        await ctx.send(
            f"Reason required to ban {member.name} from this server!")
        return
    await member.ban(reason=reason)
    embed = discord.Embed(title=f"✅ {member} was banned from this server! ✅",
                          timestamp=ctx.message.created_at)
    embed.add_field(name="Reason", value=reason)
    await ctx.send(embed=embed)


@client.command(aliases=["emoji", "new_emoji", "createemoji"])
@commands.has_permissions(manage_emojis=True)
async def create_emoji(ctx, url: str, *, name):
    guild = ctx.guild
    if ctx.author.guild_permissions.manage_emojis:
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:

                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=b_value,
                                                                name=name)
                        await ctx.send(
                            f'Successfully created emoji: <:{name}:{emoji.id}>'
                        )
                        await ses.close()
                    else:
                        await ctx.send(
                            f'Error when making request | {r.status} response.'
                        )
                        await ses.close()

                except discord.HTTPException:
                    await ctx.send('File size is too big!')


@client.command(alaises=["deleteemoji", "demoji"])
@commands.has_permissions(manage_emojis=True)
async def delete_emoji(ctx, emoji: discord.Emoji):
    guild = ctx.guild
    if ctx.author.guild_permissions.manage_emojis:
        await ctx.send(f'Successfully deleted: {emoji}')
        await emoji.delete()


player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command(aliases = ["ttt"])
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")



@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game to use this command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention @ any player for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


aki = Akinator()
emojis_c = ['✅', '❌', '🤷', '👍', '👎', '⏮', '🛑']
emojis_w = ['✅', '❌']



def w(name, desc, picture):
    embed_win = discord.Embed(title=f"It's {name} ({desc})! Was I correct?",
                              colour=0x9522c9)
    embed_win.set_image(url=picture)
    return embed_win
    


@client.command()
async def akihelp(ctx):
    desc_helpme = '__**HOW TO PLAY**__\n\nUse the `.aki` command followed by the game mode you want to play. Here is ' \
       'a list of currently available game modes : **people, animals, objects**.\nFor example : `.aki people`\n\n__**GAME MODES**__\n\n' \
       '**People** : This is the game mode for guessing people (fictional or real)\n**Animals** : ' \
       'This is the game mode for guessing animals\n**Objects** : This is the game mode for guessing objects' \
       '\n\n__**MISCELLANEOUS**__\n\n**1.**Wait until all emojis are displayed before adding your reaction, or' \
       ' else it will not register it and you will have to react again once it is done displaying' \
       '\n**2.**The game ends in 45 seconds if you do not answer the question by reacting with the right' \
       ' emoji\n**3.** The bot might sometimes be slow, please be patient and wait for it to ask you the questions. If it is stuck, do not worry the game will automatically end in 30 seconds and you can start playing again\n**4.** Only one person can play at a time\n\n' \
       '__**EMOJI MEANINGS**__\n\n✅ = This emoji means "yes"\n❌ = This emoji means "no"\n🤷 = This emoji means' \
       '"I do not know"\n👍 = This emoji means "probably"\n👎 = This emoji means "probably not"\n⏮ = This ' \
       'emoji repeats the question before\n🛑 = This emoji ends the game being played'
    embed_var_helpme = discord.Embed(description=desc_helpme, color=0x9522c9)
    await ctx.send(embed=embed_var_helpme)


@client.command(name='aki')
@commands.max_concurrency( 1, per=BucketType.default, wait=False)
async def guess(ctx, *, extra):
        desc_loss = ''
        d_loss = ''

        def check_c(reaction, user):
            return user == ctx.author and str(
                reaction.emoji) in emojis_c and reaction.message.content == q

        def check_w(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emojis_w

        async with ctx.typing():
            if extra == 'people':
                q = await aki.start_game(child_mode=True)
            elif extra == 'objects' or extra == 'animals':
                q = await aki.start_game(language=f'en_{extra}',
                                         child_mode=True)
            else:
                title_error_three = 'This game mode does not exist'
                desc_error_three = 'Use **.help** to see a list of all the game modes available'
                embed_var_three = discord.Embed(title=title_error_three,
                                                description=desc_error_three,
                                                color=0x9522c9)
                await ctx.reply(embed=embed_var_three)
                return

            embed_question = discord.Embed(
                title=
                'Tip : Wait until all emojis finish being added before reacting'
                ' or you will have to unreact and react again',
                color=0x9522c9)
            await ctx.reply(embed=embed_question)

        while aki.progression <= 85:
            message = await ctx.reply(q)

            for m in emojis_c:
                await message.add_reaction(m)

            try:
                symbol, username = await bot.wait_for('reaction_add',
                                                      timeout=45.0,
                                                      check=check_c)
            except asyncio.TimeoutError:
                embed_game_ended = discord.Embed(
                    title='You took too long,the game has ended',
                    color=0x9522c9)
                await ctx.reply(embed=embed_game_ended)
                return

            if str(symbol) == emojis_c[0]:
                a = 'y'
            elif str(symbol) == emojis_c[1]:
                a = 'n'
            elif str(symbol) == emojis_c[2]:
                a = 'idk'
            elif str(symbol) == emojis_c[3]:
                a = 'p'
            elif str(symbol) == emojis_c[4]:
                a = 'pn'
            elif str(symbol) == emojis_c[5]:
                a = 'b'
            elif str(symbol) == emojis_c[6]:
                embed_game_end = discord.Embed(
                    title='I ended the game because you asked me to do it',
                    color=0x9522c9)
                await ctx.reply(embed=embed_game_end)
                return

            if a == "b":
                try:
                    q = await aki.back()
                except akinator.CantGoBackAnyFurther:
                    pass
            else:
                q = await aki.answer(a)

        await aki.win()

        wm = await ctx.reply(
            embed=w(aki.first_guess['name'], aki.first_guess['description'],
                    aki.first_guess['absolute_picture_path']))

        for e in emojis_w:
            await wm.add_reaction(e)

        try:
            s, u = await bot.wait_for('reaction_add',
                                      timeout=30.0,
                                      check=check_w)
        except asyncio.TimeoutError:
            for times in aki.guesses:
                d_loss = d_loss + times['name'] + '\n'
            t_loss = 'Here is a list of all the people I had in mind :'
            embed_loss = discord.Embed(title=t_loss,
                                       description=d_loss,
                                       color=0x9522c9)
            await ctx.reply(embed=embed_loss)
            return

        if str(s) == emojis_w[0]:
            embed_win = discord.Embed(
                title='Great, guessed right one more time!', color=0x00FF00)
            await ctx.reply(embed=embed_win)
        elif str(s) == emojis_w[1]:
            for times in aki.guesses:
                desc_loss = desc_loss + times['name'] + '\n'
            title_loss = 'No problem, I will win next time! But here is a list of all the people I had in mind :'
            embed_loss = discord.Embed(title=title_loss,
                                       description=desc_loss,
                                       color=0x9522c9)
            await ctx.reply(embed=embed_loss)



@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        title_error_one = 'You have not entered anything after the command'
        desc_error_one = 'Use **.akihelp** to see a list of all the game modes available'
        embed_var_one = discord.Embed(title=title_error_one,
                                      description=desc_error_one,
                                      color=0x9522c9)
        await ctx.reply(embed=embed_var_one)

    if isinstance(error, commands.MaxConcurrencyReached):
        title_error_four = 'Someone is already playing'
        desc_error_four = 'Please wait until the person currently playing is done with their turn'
        embed_var_four = discord.Embed(title=title_error_four,
                                       description=desc_error_four,
                                       color=0x9522c9)
        await ctx.reply(embed=embed_var_four)


my_secret = os.environ['Token']
keep_alive()
client.run(my_secret)
#client embed
#minigame embed

##@2024 Rezend Inc
