import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# --- SERVEUR POUR RENDER ---
app = Flask('')
@app.route('/')
def home():
    return "Bot en ligne !"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIG BOT ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

# Remplace par tes vrais IDs
ADMIN_IDS = [1337085414275682437, 719517140390248480] 

@bot.event
async def on_ready():
    print(f'✅ BOT CONNECTÉ : {bot.user.name}')

@bot.command()
async def join(ctx):
    if ctx.author.id in ADMIN_IDS:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"✅ Arrivée dans **{channel}**")
        else:
            await ctx.send("❌ Connecte-toi d'abord !")
    else:
        await ctx.send("🚫 Non autorisé.")

@bot.command()
async def leave(ctx):
    if ctx.author.id in ADMIN_IDS:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Déconnexion")

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv('DISCORD_TOKEN'))
