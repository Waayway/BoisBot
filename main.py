from dotenv import load_dotenv
load_dotenv()
import discord
from discord.ext import commands
import os


class BoisToolkit(commands.Bot):
    def __init__(self, description=None, **options):
        super().__init__(command_prefix="!",description=description, **options)

    async def on_ready(self):
        print(self.guilds)
        await self.register_commands()
        print('Logged on as {0}!'.format(self.user))

client = BoisToolkit()
client.load_extension("deadbydaylight")

client.run(os.getenv("BOT_TOKEN"))