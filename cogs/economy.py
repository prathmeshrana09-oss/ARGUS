import discord
from discord.ext import commands
from datetime import datetime
import json
import os
import aiohttp

class Economy(commands.Cog):
    """Economy system with currency and trading."""
    
    def __init__(self, bot):
        self.bot = bot
        self.economy_file = 'data/economy.json'
        self.ensure_data_files()
    
    def ensure_data_files(self):
        """Ensure data directory and JSON files exist."""
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(self.economy_file):
            with open(self.economy_file, 'w') as f:
                json.dump({}, f)
    
    def load_economy(self):
        """Load economy data."""
        with open(self.economy_file, 'r') as f:
            return json.load(f)
    
    def save_economy(self, data):
        """Save economy data."""
        with open(self.economy_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_or_create_account(self, user_id):
        """Get or create user economy account."""
        economy = self.load_economy()
        user_id_str = str(user_id)
        
        if user_id_str not in economy:
            economy[user_id_str] = {
                'balance': 1000,
                'bank': 0,
                'level': 1,
                'inventory': {},
                'last_daily': None,
                'last_work': None
            }
            self.save_economy(economy)
        
        return economy[user_id_str]
    
    # BALANCE COMMAND
    @commands.command(name='balance')
    async def balance(self, ctx, member: discord.Member = None):
        """Check your money balance.
        
        Usage: /balance [@user]
        """
        if member is None:
            member = ctx.author
        
        account = self.get_or_create_account(member.id)
        total = account['balance'] + account['bank']
        
        embed = discord.Embed(
            title=f"💰 Balance - {member.name}",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="Wallet", value=f"💵 ${account['balance']}", inline=True)
        embed.add_field(name="Bank", value=f"🏦 ${account['bank']}", inline=True)
        embed.add_field(name="Total", value=f"💎 ${total}", inline=True)
        embed.add_field(name="Level", value=f"📊 {account['level']}", inline=True)
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # DAILY COMMAND
    @commands.command(name='daily')
    async def daily(self, ctx):
        """Claim your daily reward.
        
        Usage: /daily
        """
        account = self.get_or_create_account(ctx.author.id)
        economy = self.load_economy()
        
        # Check if already claimed today
        if account['last_daily']:
            last_daily = datetime.fromisoformat(account['last_daily'])
            if (datetime.now() - last_daily).days < 1:
                await ctx.send("❌ You already claimed your daily reward. Come back tomorrow!")
                return
        
        reward = 500
        account['balance'] += reward
        account['last_daily'] = datetime.now().isoformat()
        economy[str(ctx.author.id)] = account
        self.save_economy(economy)
        
        embed = discord.Embed(
            title="🎁 Daily Reward",
            description=f"You claimed **${reward}**!",
            color=discord.Color.green()
        )
        embed.add_field(name="New Balance", value=f"💵 ${account['balance']}", inline=False)
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # WORK COMMAND
    @commands.command(name='work')
    async def work(self, ctx):
        """Work to earn money.
        
        Usage: /work
        """
        import random
        
        account = self.get_or_create_account(ctx.author.id)
        economy = self.load_economy()
        
        jobs = {
            'Developer': 150,
            'Designer': 120,
            'Teacher': 100,
            'Doctor': 200,
            'Artist': 90,
            'Streamer': 110
        }
        
        job = random.choice(list(jobs.keys()))
        salary = random.randint(int(jobs[job] * 0.8), int(jobs[job] * 1.2))
        
        account['balance'] += salary
        economy[str(ctx.author.id)] = account
        self.save_economy(economy)
        
        embed = discord.Embed(
            title="💼 Work",
            description=f"You worked as a **{job}** and earned **${salary}**!",
            color=discord.Color.blue()
        )
        embed.add_field(name="New Balance", value=f"💵 ${account['balance']}", inline=False)
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # DEPOSIT COMMAND
    @commands.command(name='deposit')
    async def deposit(self, ctx, amount: int):
        """Deposit money into your bank.
        
        Usage: /deposit <amount>
        """
        account = self.get_or_create_account(ctx.author.id)
        economy = self.load_economy()
        
        if amount <= 0:
            await ctx.send("❌ Amount must be positive.")
            return
        
        if account['balance'] < amount:
            await ctx.send(f"❌ You don't have ${amount}. Your balance: ${account['balance']}")
            return
        
        account['balance'] -= amount
        account['bank'] += amount
        economy[str(ctx.author.id)] = account
        self.save_economy(economy)
        
        embed = discord.Embed(
            title="🏦 Deposit",
            description=f"You deposited **${amount}** into your bank!",
            color=discord.Color.green()
        )
        embed.add_field(name="Wallet", value=f"💵 ${account['balance']}", inline=True)
        embed.add_field(name="Bank", value=f"🏦 ${account['bank']}", inline=True)
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # WITHDRAW COMMAND
    @commands.command(name='withdraw')
    async def withdraw(self, ctx, amount: int):
        """Withdraw money from your bank.
        
        Usage: /withdraw <amount>
        """
        account = self.get_or_create_account(ctx.author.id)
        economy = self.load_economy()
        
        if amount <= 0:
            await ctx.send("❌ Amount must be positive.")
            return
        
        if account['bank'] < amount:
            await ctx.send(f"❌ You don't have ${amount} in your bank. Your bank balance: ${account['bank']}")
            return
        
        account['bank'] -= amount
        account['balance'] += amount
        economy[str(ctx.author.id)] = account
        self.save_economy(economy)
        
        embed = discord.Embed(
            title="💰 Withdraw",
            description=f"You withdrew **${amount}** from your bank!",
            color=discord.Color.green()
        )
        embed.add_field(name="Wallet", value=f"💵 ${account['balance']}", inline=True)
        embed.add_field(name="Bank", value=f"🏦 ${account['bank']}", inline=True)
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # SHOP COMMAND
    @commands.command(name='shop')
    async def shop(self, ctx):
        """View available items in the shop.
        
        Usage: /shop
        """
        items = {
            'Gold Coin': 100,
            'Gem': 500,
            'Potion': 200,
            'Sword': 1000,
            'Shield': 800,
            'Crown': 5000
        }
        
        embed = discord.Embed(
            title="🛍️ Shop",
            description="Available items for purchase",
            color=discord.Color.gold()
        )
        
        for item, price in items.items():
            embed.add_field(name=item, value=f"💰 ${price}", inline=True)
        
        embed.add_field(name="Buy Item", value="Use `/buy <item_name>`", inline=False)
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # BUY COMMAND
    @commands.command(name='buy')
    async def buy(self, ctx, *, item_name):
        """Buy an item from the shop.
        
        Usage: /buy <item_name>
        """
        items = {
            'gold coin': 100,
            'gem': 500,
            'potion': 200,
            'sword': 1000,
            'shield': 800,
            'crown': 5000
        }
        
        item_name_lower = item_name.lower()
        
        if item_name_lower not in items:
            await ctx.send(f"❌ Item '{item_name}' not found. Use `/shop` to see available items.")
            return
        
        account = self.get_or_create_account(ctx.author.id)
        economy = self.load_economy()
        price = items[item_name_lower]
        
        if account['balance'] < price:
            await ctx.send(f"❌ You don't have enough money. Price: ${price}, Your balance: ${account['balance']}")
            return
        
        account['balance'] -= price
        if 'items' not in account:
            account['items'] = {}
        account['items'][item_name_lower] = account['items'].get(item_name_lower, 0) + 1
        
        economy[str(ctx.author.id)] = account
        self.save_economy(economy)
        
        embed = discord.Embed(
            title="🎉 Purchase Successful",
            description=f"You bought a **{item_name}** for **${price}**!",
            color=discord.Color.green()
        )
        embed.add_field(name="New Balance", value=f"💵 ${account['balance']}", inline=False)
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # SELL COMMAND
    @commands.command(name='sell')
    async def sell(self, ctx, *, item_name):
        """Sell an item from your inventory.
        
        Usage: /sell <item_name>
        """
        account = self.get_or_create_account(ctx.author.id)
        
        if 'items' not in account or item_name.lower() not in account['items']:
            await ctx.send(f"❌ You don't have a '{item_name}' to sell.")
            return
        
        items = {
            'gold coin': 50,
            'gem': 250,
            'potion': 100,
            'sword': 500,
            'shield': 400,
            'crown': 2500
        }
        
        item_lower = item_name.lower()
        price = items.get(item_lower, 100)
        
        account['items'][item_lower] -= 1
        if account['items'][item_lower] <= 0:
            del account['items'][item_lower]
        
        account['balance'] += price
        economy = self.load_economy()
        economy[str(ctx.author.id)] = account
        self.save_economy(economy)
        
        embed = discord.Embed(
            title="💰 Item Sold",
            description=f"You sold a **{item_name}** for **${price}**!",
            color=discord.Color.green()
        )
        embed.add_field(name="New Balance", value=f"💵 ${account['balance']}", inline=False)
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # GAMBLE COMMAND
    @commands.command(name='gamble')
    async def gamble(self, ctx, amount: int):
        """Gamble your money.
        
        Usage: /gamble <amount>
        """
        import random
        
        account = self.get_or_create_account(ctx.author.id)
        
        if amount <= 0:
            await ctx.send("❌ Amount must be positive.")
            return
        
        if account['balance'] < amount:
            await ctx.send(f"❌ You don't have ${amount}. Your balance: ${account['balance']}")
            return
        
        result = random.random()
        
        if result > 0.5:
            # Win
            winnings = int(amount * 1.5)
            account['balance'] += winnings
            color = discord.Color.green()
            title = "🎰 You Won!"
            description = f"You won **${winnings}**!"
        else:
            # Lose
            account['balance'] -= amount
            color = discord.Color.red()
            title = "💔 You Lost!"
            description = f"You lost **${amount}**..."
        
        economy = self.load_economy()
        economy[str(ctx.author.id)] = account
        self.save_economy(economy)
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        embed.add_field(name="New Balance", value=f"💵 ${account['balance']}", inline=False)
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    # LEADERBOARD COMMAND
    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        """View the economy leaderboard.
        
        Usage: /leaderboard
        """
        economy = self.load_economy()
        
        # Sort by balance
        sorted_accounts = sorted(
            economy.items(),
            key=lambda x: x[1]['balance'] + x[1]['bank'],
            reverse=True
        )
        
        embed = discord.Embed(
            title="💰 Economy Leaderboard",
            description="Top 10 Richest Players",
            color=discord.Color.gold()
        )
        
        for i, (user_id, account) in enumerate(sorted_accounts[:10], 1):
            try:
                user = await self.bot.fetch_user(int(user_id))
                username = user.name
            except:
                username = f"User {user_id}"
            
            total = account['balance'] + account['bank']
            embed.add_field(
                name=f"#{i} - {username}",
                value=f"💎 ${total}",
                inline=False
            )
        
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
