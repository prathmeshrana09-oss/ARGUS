import discord
from discord.ext import commands
from datetime import datetime
import random
import aiohttp

class Fun(commands.Cog):
    """Fun commands for entertainment and laughter."""
    
    def __init__(self, bot):
        self.bot = bot
    
    # MEME COMMAND
    @commands.command(name='meme')
    async def meme(self, ctx):
        """Get a random meme.
        
        Usage: /meme
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://meme-api.com/gimme') as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        embed = discord.Embed(
                            title=data['title'],
                            color=discord.Color.random()
                        )
                        embed.set_image(url=data['url'])
                        embed.add_field(name="Subreddit", value=f"r/{data['subreddit']}", inline=True)
                        embed.add_field(name="Upvotes", value=f"👍 {data['ups']}", inline=True)
                        embed.timestamp = datetime.now()
                        
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("❌ Failed to fetch meme.")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
    
    # 8BALL COMMAND
    @commands.command(name='8ball')
    async def eightball(self, ctx, *, question):
        """Ask the magic 8 ball a question.
        
        Usage: /8ball <question>
        """
        responses = [
            "Yes",
            "No",
            "Maybe",
            "Ask again later",
            "Definitely",
            "Not sure",
            "Without a doubt",
            "Absolutely not",
            "The signs point to yes",
            "Don't count on it",
            "Very doubtful",
            "Outlook good",
            "All signs point to yes",
            "Reply hazy, try again",
            "Better not tell you now"
        ]
        
        response = random.choice(responses)
        
        embed = discord.Embed(
            title="🔮 Magic 8 Ball",
            description=f"Q: {question}\n\nA: **{response}**",
            color=discord.Color.purple()
        )
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # COINFLIP COMMAND
    @commands.command(name='coinflip')
    async def coinflip(self, ctx):
        """Flip a coin.
        
        Usage: /coinflip
        """
        result = random.choice(['Heads', 'Tails'])
        emoji = '🪙'
        
        embed = discord.Embed(
            title=f"{emoji} Coin Flip",
            description=f"**{result}**!",
            color=discord.Color.gold()
        )
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # JOKE COMMAND
    @commands.command(name='joke')
    async def joke(self, ctx):
        """Get a random joke.
        
        Usage: /joke
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://v2.jokeapi.dev/joke/Any') as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        embed = discord.Embed(
                            title="😂 Joke",
                            color=discord.Color.random()
                        )
                        
                        if data['type'] == 'single':
                            embed.description = data['joke']
                        else:
                            embed.description = f"{data['setup']}\n\n{data['delivery']}"
                        
                        embed.timestamp = datetime.now()
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("❌ Failed to fetch joke.")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
    
    # ROAST COMMAND
    @commands.command(name='roast')
    async def roast(self, ctx, member: discord.Member = None):
        """Roast someone (in a fun way).
        
        Usage: /roast [@user]
        """
        if member is None:
            member = ctx.author
        
        roasts = [
            f"{member.mention}, you're so boring, even your shadow left you.",
            f"{member.mention}, I'd insult you, but you're not worth my time.",
            f"{member.mention}, you're like a software update. Everyone hates you.",
            f"{member.mention}, you bring everyone so much joy... when you leave.",
            f"{member.mention}, if you were a vegetable, you'd be a carrot. Not because of your color, but because you bore everyone.",
            f"{member.mention}, you're proof that God has a sense of humor.",
            f"{member.mention}, I'd agree with you, but then we'd both be wrong.",
            f"{member.mention}, you're so fake, even your mirror doesn't recognize you."
        ]
        
        roast = random.choice(roasts)
        
        embed = discord.Embed(
            title="🔥 Roast",
            description=roast,
            color=discord.Color.red()
        )
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # SHIP COMMAND
    @commands.command(name='ship')
    async def ship(self, ctx, member1: discord.Member = None, member2: discord.Member = None):
        """Ship two members together.
        
        Usage: /ship [@user1] [@user2]
        """
        if member1 is None or member2 is None:
            await ctx.send("❌ Please mention two users to ship.")
            return
        
        compatibility = random.randint(0, 100)
        
        # Generate ship name
        name1 = member1.name[:len(member1.name)//2]
        name2 = member2.name[len(member2.name)//2:]
        ship_name = name1 + name2
        
        embed = discord.Embed(
            title=f"💕 Shipping {member1.name} & {member2.name}",
            description=f"**Ship Name:** {ship_name}\n**Compatibility:** {compatibility}%",
            color=discord.Color.pink()
        )
        
        # Add compatibility bar
        bar_length = 20
        filled = int(bar_length * compatibility / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        embed.add_field(name="Compatibility Bar", value=f"`{bar}` {compatibility}%", inline=False)
        
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # DICE COMMAND
    @commands.command(name='dice')
    async def dice(self, ctx, sides: int = 6):
        """Roll a dice.
        
        Usage: /dice [sides]
        """
        if sides < 2:
            await ctx.send("❌ Dice must have at least 2 sides.")
            return
        
        result = random.randint(1, sides)
        
        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"You rolled a **{result}** on a {sides}-sided dice!",
            color=discord.Color.blurple()
        )
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # CAT COMMAND
    @commands.command(name='cat')
    async def cat(self, ctx):
        """Get a random cat image.
        
        Usage: /cat
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.thecatapi.com/v1/images/search') as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        embed = discord.Embed(
                            title="🐱 Random Cat",
                            color=discord.Color.orange()
                        )
                        embed.set_image(url=data[0]['url'])
                        embed.timestamp = datetime.now()
                        
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("❌ Failed to fetch cat image.")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
    
    # DOG COMMAND
    @commands.command(name='dog')
    async def dog(self, ctx):
        """Get a random dog image.
        
        Usage: /dog
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://dog.ceo/api/breeds/image/random') as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        embed = discord.Embed(
                            title="🐕 Random Dog",
                            color=discord.Color.orange()
                        )
                        embed.set_image(url=data['message'])
                        embed.timestamp = datetime.now()
                        
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("❌ Failed to fetch dog image.")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
    
    # GIF COMMAND
    @commands.command(name='gif')
    async def gif(self, ctx, *, query):
        """Search for a GIF.
        
        Usage: /gif <search_query>
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.giphy.com/v1/gifs/search?q={query}&limit=1&api_key=dc6zaTOxFJmzC"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data['data']:
                            gif_url = data['data'][0]['images']['original']['url']
                            
                            embed = discord.Embed(
                                title=f"🎬 GIF - {query}",
                                color=discord.Color.random()
                            )
                            embed.set_image(url=gif_url)
                            embed.timestamp = datetime.now()
                            
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f"❌ No GIFs found for '{query}'.")
                    else:
                        await ctx.send("❌ Failed to fetch GIF.")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
