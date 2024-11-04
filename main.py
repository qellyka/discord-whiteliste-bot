from cProfile import label

import discord
from discord import Interaction
from discord.ui import Button, View, Modal, InputText
from mcrcon import MCRcon

import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RCON_PASSWORD = os.getenv('RCON_PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

bot = discord.Bot()

class WhitelistAddModel(Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title="Добавление ника в вайтлист")

        self.add_item(InputText(label="Введите свой ник в майнкрафт: ", placeholder="steve"))

    async def callback(self, interaction: discord.Interaction):
        nickname = self.children[0].value
        with MCRcon(HOST, RCON_PASSWORD, int(PORT)) as mcr:
            response = mcr.command(f"whitelist add {nickname}")
            print(response)
        await interaction.response.send_message("Ваш ник добавлен в вайтлист!!!")

@bot.command()
async def add_button(ctx: discord.ApplicationContext):
    addButton = Button(label="Добавить ник", emoji="➕", style=discord.ButtonStyle.green)

    buttonManager = View(addButton)

    async def addCallback(interaction: discord.Interaction):
        buttonManager.disable_all_items()
        await interaction.response.send_modal(WhitelistAddModel())
        await interaction.followup.edit_message(view=buttonManager)

    addButton.callback = addCallback

    await ctx.respond("Нажмите на кнопку чтобы добавить ник в вайтлист!", view=buttonManager)

@bot.command()
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hello")

if __name__ == "__main__":
    bot.run(BOT_TOKEN)