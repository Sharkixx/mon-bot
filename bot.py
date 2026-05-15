import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# --- SERVEUR WEB ---
app = Flask('')
@app.route('/')
def home():
    return "Bot OK"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

# AJOUTE TES IDS ICI (IMPORTANT)
ADMIN_IDS = [1337085414275682437, 719517140390248480]

@bot.event
async def on_ready():
    print(f'✅ CONNECTE : {bot.user.name}')

@bot.command()
async def join(ctx):
    if ctx.author.id in ADMIN_IDS:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
            await ctx.send("✅ Connecté au vocal !")
        else:
            await ctx.send("❌ Va en vocal d'abord.")

@bot.command()
async def leave(ctx):
    if ctx.author.id in ADMIN_IDS and ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Bye !")

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv('DISCORD_TOKEN'))
