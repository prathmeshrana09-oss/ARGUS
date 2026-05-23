import discord
from discord.ext import commands
from datetime import datetime
import json
import os
import random

class Social(commands.Cog):
    """Social and roleplay commands for community interaction."""
    
    def __init__(self, bot):
        self.bot = bot
        self.profiles_file = 'data/profiles.json'
        self.ensure_data_files()
    
    def ensure_data_files(self):
        """Ensure data directory and JSON files exist."""
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(self.profiles_file):
            with open(self.profiles_file, 'w') as f:
                json.dump({}, f)
    
    def load_profiles(self):
        """Load profiles."""
        with open(self.profiles_file, 'r') as f:
            return json.load(f)
    
    def save_profiles(self, data):
        """Save profiles."""
        with open(self.profiles_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    # HUG COMMAND
    @commands.command(name='hug')
    async def hug(self, ctx, member: discord.Member = None):
        """Hug someone.
        
        Usage: /hug [@user]
        """
        if member is None:
            await ctx.send(f"{ctx.author.mention} hugs themselves 🤗")
            return
        
        embed = discord.Embed(
            title="🤗 Hug",
            description=f"{ctx.author.mention} hugs {member.mention}",
            color=discord.Color.pink()
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # SLAP COMMAND
    @commands.command(name='slap')
    async def slap(self, ctx, member: discord.Member):
        """Slap someone.
        
        Usage: /slap @user
        """
        embed = discord.Embed(
            title="👋 Slap",
            description=f"{ctx.author.mention} slaps {member.mention}",
            color=discord.Color.red()
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # PAT COMMAND
    @commands.command(name='pat')
    async def pat(self, ctx, member: discord.Member = None):
        """Pat someone.
        
        Usage: /pat [@user]
        """
        if member is None:
            await ctx.send(f"{ctx.author.mention} pats themselves 👋")
            return
        
        embed = discord.Embed(
            title="👋 Pat",
            description=f"{ctx.author.mention} pats {member.mention}",
            color=discord.Color.blue()
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # WAVE COMMAND
    @commands.command(name='wave')
    async def wave(self, ctx, member: discord.Member = None):
        """Wave at someone.
        
        Usage: /wave [@user]
        """
        if member is None:
            await ctx.send(f"{ctx.author.mention} waves 👋")
            return
        
        embed = discord.Embed(
            title="👋 Wave",
            description=f"{ctx.author.mention} waves at {member.mention}",
            color=discord.Color.blurple()
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # MARRY COMMAND
    @commands.command(name='marry')
    async def marry(self, ctx, member: discord.Member):
        """Marry someone (roleplay).
        
        Usage: /marry @user
        """
        embed = discord.Embed(
            title="💍 Marriage",
            description=f"{ctx.author.mention} proposes to {member.mention}",
            color=discord.Color.pink()
        )
        embed.add_field(name="Status", value="💒 Married!", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # PROFILE COMMAND
    @commands.command(name='profile')
    async def profile(self, ctx, member: discord.Member = None):
        """View your profile.
        
        Usage: /profile [@user]
        """
        if member is None:
            member = ctx.author
        
        profiles = self.load_profiles()
        user_id = str(member.id)
        
        if user_id not in profiles:
            profiles[user_id] = {
                'bio': 'No bio set',
                'level': 1,
                'rep': 0,
                'badges': []
            }
            self.save_profiles(profiles)
        
        profile = profiles[user_id]
        
        embed = discord.Embed(
            title=f"👤 Profile - {member.name}",
            color=member.color if member.color != discord.Color.default() else discord.Color.blurple()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="Bio", value=profile['bio'], inline=False)
        embed.add_field(name="Level", value=profile['level'], inline=True)
        embed.add_field(name="Reputation", value=f"⭐ {profile['rep']}", inline=True)
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # LEVEL COMMAND
    @commands.command(name='level')
    async def level(self, ctx, member: discord.Member = None):
        """Check your level.
        
        Usage: /level [@user]
        """
        if member is None:
            member = ctx.author
        
        profiles = self.load_profiles()
        user_id = str(member.id)
        
        if user_id not in profiles:
            level = 1
            exp = 0
        else:
            level = profiles[user_id].get('level', 1)
            exp = profiles[user_id].get('exp', 0)
        
        embed = discord.Embed(
            title=f"📊 Level - {member.name}",
            description=f"Level {level}",
            color=discord.Color.gold()
        )
        embed.add_field(name="Experience", value=f"⭐ {exp} XP", inline=True)
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # REP COMMAND
    @commands.command(name='rep')
    async def rep(self, ctx, member: discord.Member):
        """Give someone a reputation point.
        
        Usage: /rep @user
        """
        if member == ctx.author:
            await ctx.send("❌ You can't rep yourself!")
            return
        
        profiles = self.load_profiles()
        user_id = str(member.id)
        
        if user_id not in profiles:
            profiles[user_id] = {
                'bio': 'No bio set',
                'level': 1,
                'rep': 0,
                'badges': []
            }
        
        profiles[user_id]['rep'] += 1
        self.save_profiles(profiles)
        
        embed = discord.Embed(
            title="⭐ Reputation",
            description=f"{ctx.author.mention} gave {member.mention} a reputation point!",
            color=discord.Color.gold()
        )
        embed.add_field(name="Total Rep", value=profiles[user_id]['rep'], inline=False)
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Social(bot))
