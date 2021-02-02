# bot.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

import yfinance as yf
import mplfinance as mpf

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#client = discord.Client()
bot = commands.Bot(command_prefix='*')

# @client.event
# async def on_ready():
#     for guild in client.guilds:
#         if guild.name == GUILD:
#             break

#     print(f'{client.user} is connected to the following guild:\n'
#           f'{guild.name}(id: {guild.id})')

#     members = '\n - '.join([member.name for member in guild.members])
#     print(f'Guild Members:\n - {members}')


@bot.command(name="8ball", help="ask the magic 8 ball a question and shake")
async def magic_8_ball(ctx, question: str):
    results = ["As I see it, yes.",
                "Ask again later.",
                "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don’t count on it.",
                 "It is certain.",
                 "It is decidedly so.",
                 "Most likely.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Outlook good.",
                 "Reply hazy, try again.",
                 "Signs point to yes.",
                 "Very doubtful.",
                 "Without a doubt.",
                 "Yes.",
                 "Yes – definitely.",
                 "You may rely on it."]

    response = random.choice(results)
    await ctx.send(response)

@bot.command(name="charts")
async def show_chart(ctx,
                     ticker,
                     period="max",
                     interval="1wk",
                     start=None,
                     end=None,
                     help=""):
    
    ticker = ticker.upper()
    t = yf.Ticker(ticker)
    if start != None and end != None:
        hist = t.history(interval=interval, start=start, end=end)
    else:
        hist = t.history(period=period, interval=interval)

    # Create my own `marketcolors` to use with the `nightclouds` style:
    mc = mpf.make_marketcolors(up='green',down='red',inherit=True)
    # Create a new style based on `nightclouds` but with my own `marketcolors`:
    s  = mpf.make_mpf_style(base_mpf_style='classic',marketcolors=mc)
    # Plot my new custom mpf style:
    mpf.plot(hist.iloc[:],type='candle', volume=True, style=s, savefig='./plot.png')

    await ctx.send(file=discord.File('./plot.png'))
    os.remove('./plot.png')


#client.run(TOKEN)
bot.run(TOKEN)