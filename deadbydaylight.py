# Some typing for ease of use
from typing import List

# All pycord Imports 
from discord.ext import commands
from discord.commands import slash_command
from discord.ext.commands.context import Context
import discord

# Database stuff
from jsondbpy import Manager

# not big stuff
import datetime
import os

class DeadByDaylight(commands.Cog):
    members: List[discord.User] = []
    timeSinceKiller: dict = {}
    # statics: dict = {}
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Manager(os.getenv("DATABASE_LOCATION"))
        self.data = self.db.get()
        self.members = self.data["members"]
        timeSinceKillerValues = list(self.data["timeSinceKiller"].values())
        timeSinceKillerKeys = list(self.data["timeSinceKiller"].keys())
        for i in range(len(timeSinceKillerKeys)):
            self.timeSinceKiller[timeSinceKillerKeys[i]] = datetime.datetime.strptime(timeSinceKillerValues[i], "%m/%d/%Y, %H:%M:%S")

        
    @commands.command()
    async def join(self, ctx):
        """Join the list of possible killers."""
        if self.members.count(ctx.author) > 0:
            await ctx.send(f"You are already part of the Killers")
        else:
            self.members.append(ctx.author.name)
            self.timeSinceKiller[ctx.author.name] = datetime.datetime.now()
            
            self.data["members"] = self.members
            self.data["timeSinceKiller"][ctx.author.name] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            self.db.save()
            await ctx.send(f"You have joined the Killers")
    
    @commands.command()
    async def leave(self,ctx: Context):
        """Leave the list of possible killers."""
        if self.members.count(ctx.author.name) > 0:
            self.members.remove(ctx.author.name)
            del self.timeSinceKiller[ctx.author.name]
            del self.data["timeSinceKiller"][ctx.author.name]
            self.db.save()
            await ctx.send(f"You have left the Killers")
        else:
            await ctx.send(f"You are not part of the Killers")
        
    @commands.command()
    async def killer(self,ctx, member: discord.Member = None):
        if member and self.members.count(member.name):
            self.timeSinceKiller[member.name] = datetime.datetime.now()
            self.data["timeSinceKiller"][member.name] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            self.db.save()
            await ctx.send("You are now the killer have fun!")
        elif self.members.count(ctx.author.name) > 0:
            self.timeSinceKiller[ctx.author.name] = datetime.datetime.now()
            self.data["timeSinceKiller"][ctx.author.name] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            self.db.save()
            await ctx.send("You are now the killer have fun!")
        else:
            await ctx.send("You are not one of the killers, Type /join to join the killers")
    
    @commands.command()
    async def list(self,ctx):
        self.timeSinceKiller = dict(sorted(self.timeSinceKiller.items(),key= lambda x:x[-1]))
        timeSinceKillerKeys = list(self.timeSinceKiller.keys())[::-1]
        timeSinceKillerValues = list(self.timeSinceKiller.values())[::-1]
        s = "The one at the bottom is the killer. \n"
        if len(self.timeSinceKiller) < 1:
            s = "Nobody has joined, Weird probably a bug"
        for i in range(len(timeSinceKillerKeys)):
            s += f"{timeSinceKillerKeys[i]}\n"
        await ctx.send(s)




def setup(bot):
    print("Turning on DeadByDaylight Module")
    bot.add_cog(DeadByDaylight(bot))


def teardown(bot):
    print("Shutting down DeadByDaylight Module")
