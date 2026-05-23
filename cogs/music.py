import discord
from discord.ext import commands
from datetime import datetime
import aiohttp

class Music(commands.Cog):
    """Music commands for playing songs."""
    
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
    
    # PLAY COMMAND
    @commands.command(name='play')
    async def play(self, ctx, *, song_name):
        """Play a song.
        
        Usage: /play <song_name>
        """
        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{song_name}**",
            color=discord.Color.purple()
        )
        embed.add_field(name="Status", value="▶️ Playing", inline=True)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # SKIP COMMAND
    @commands.command(name='skip')
    async def skip(self, ctx):
        """Skip the current song.
        
        Usage: /skip
        """
        embed = discord.Embed(
            title="⏭️ Skipped",
            description="Song skipped!",
            color=discord.Color.blurple()
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # PAUSE COMMAND
    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pause the current song.
        
        Usage: /pause
        """
        embed = discord.Embed(
            title="⏸️ Paused",
            description="Music paused!",
            color=discord.Color.orange()
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # RESUME COMMAND
    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resume playing.
        
        Usage: /resume
        """
        embed = discord.Embed(
            title="▶️ Resumed",
            description="Music resumed!",
            color=discord.Color.green()
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # QUEUE COMMAND
    @commands.command(name='queue')
    async def queue(self, ctx):
        """View the music queue.
        
        Usage: /queue
        """
        embed = discord.Embed(
            title="🎵 Queue",
            description="Songs in queue",
            color=discord.Color.purple()
        )
        embed.add_field(name="Songs", value="Queue is empty", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # LYRICS COMMAND
    @commands.command(name='lyrics')
    async def lyrics(self, ctx, *, song_name):
        """Get lyrics for a song.
        
        Usage: /lyrics <song_name>
        """
        embed = discord.Embed(
            title=f"📝 Lyrics - {song_name}",
            description="Lyrics not found. Try a different song.",
            color=discord.Color.purple()
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # VOLUME COMMAND
    @commands.command(name='volume')
    async def volume(self, ctx, level: int):
        """Set music volume.
        
        Usage: /volume <0-100>
        """
        if level < 0 or level > 100:
            await ctx.send("❌ Volume must be between 0 and 100.")
            return
        
        embed = discord.Embed(
            title="🔊 Volume",
            description=f"Volume set to {level}%",
            color=discord.Color.green()
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # SHUFFLE COMMAND
    @commands.command(name='shuffle')
    async def shuffle(self, ctx):
        """Shuffle the queue.
        
        Usage: /shuffle
        """
        embed = discord.Embed(
            title="🔀 Shuffled",
            description="Queue shuffled!",
            color=discord.Color.blurple()
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # LOOP COMMAND
    @commands.command(name='loop')
    async def loop(self, ctx, mode: str = None):
        """Set loop mode.
        
        Usage: /loop [off|song|queue]
        """
        modes = ['off', 'song', 'queue']
        if mode is None:
            mode = 'queue'
        
        if mode.lower() not in modes:
            await ctx.send(f"❌ Invalid mode. Use: {', '.join(modes)}")
            return
        
        embed = discord.Embed(
            title="🔁 Loop",
            description=f"Loop mode: {mode.upper()}",
            color=discord.Color.green()
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    
    # STOP COMMAND
    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stop the music.
        
        Usage: /stop
        """
        embed = discord.Embed(
            title="⏹️ Stopped",
            description="Music stopped!",
            color=discord.Color.red()
        )
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
