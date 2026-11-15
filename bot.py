import asyncio
import os
import random
from datetime import datetime
from threading import Thread

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask

# ==============================================================================
# 1. FLASK KEEP-ALIVE SERVER (MANDATORY FOR RENDER PORT BINDING)
# ==============================================================================
app = Flask(__name__)

@app.route("/")
def health_check():
    return {
        "status": "online",
        "service": "Auto-Vouch Engine",
        "timestamp": datetime.utcnow().isoformat()
    }, 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

server_thread = Thread(target=run_flask, daemon=True)
server_thread.start()

# ==============================================================================
# 2. ENVIRONMENT & ROBUST PROOFS.TXT LOADER
# ==============================================================================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID")) if os.getenv("GUILD_ID") else None

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing in your .env file.")

PROOFS_FILE = "proofs.txt"

def load_proofs() -> list[str]:
    """Loads image proof links from proofs.txt, automatically stitching wrapped multi-line URLs."""
    if not os.path.exists(PROOFS_FILE):
        with open(PROOFS_FILE, "w", encoding="utf-8") as f:
            f.write("# Paste your 100+ direct image proof URLs below\n")

    links = []
    with open(PROOFS_FILE, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith(("http://", "https://")):
                links.append(line)
            elif links:
                links[-1] += line

    return links if links else ["https://i.imgur.com/8Q9Z5vE.png"]

def append_proof(url: str):
    """Appends a new image proof URL to proofs.txt."""
    with open(PROOFS_FILE, "a", encoding="utf-8") as f:
        f.write(url.strip() + "\n")

# ==============================================================================
# 3. 210+ REALISTIC MARKETPLACE & MM FEEDBACKS
# ==============================================================================
FEEDBACK_POOL = [
    "Super fast delivery! Got my Robux within 2 minutes of paying. 10/10.",
    "Legit seller and super smooth MM service. Will definitely buy again!",
    "Vouch! Went first with $50 crypto and received my items immediately.",
    "Fastest transaction I've ever had on Discord. Trusted MM!",
    "100% legit, clean trade, zero issues. Highly recommended.",
    "Vouch for the seller and MM, held the items safely and delivered right away.",
    "Bought 10k Robux, smooth gamepass transfer and great communication.",
    "Super polite seller, walked me through the whole process. A++",
    "Vouch! Trusted middleman, didn't waste any time.",
    "Instant response and quick delivery. Best shop around!",
    "Went first via PayPal F&F, got my fruit in less than a minute.",
    "Massive vouch! Handled a $120 trade smoothly with zero hiccups.",
    "Cleanest trade ever, MM was super professional and fast.",
    "Legit shop, prices are unbeatable and delivery is instant.",
    "Vouch! Traded limiteds using the MM here, 100% safe.",
    "Fastest seller online right now, got everything I paid for.",
    "Super reliable! Bought multiple times and never had a single problem.",
    "Vouch for both! Smooth cross-trade handled safely by the MM.",
    "Quick, easy, and trustworthy. Definitely coming back for more.",
    "10/10 service, responded to my ticket in seconds.",
    "Vouch! Sent LTC first and received my order right after 1 confirmation.",
    "Awesome seller, threw in a small bonus too. Much appreciated!",
    "Very patient MM, waited while we sorted out private server links.",
    "Legit and fast! Don't hesitate to deal with them.",
    "Vouch! Smooth $35 deal, everything went according to plan.",
    "Best middleman service on Discord, fast and reliable.",
    "Got my items right after payment cleared. Super trustworthy!",
    "Vouch! Zero stress trade, MM verified everything before releasing.",
    "Amazing service, fast replies, and 100% legit.",
    "Bought bulk items, got a great deal and instant delivery.",
    "Vouch! Trusted with high-tier items, smooth handoff.",
    "Quickest trade of my life, took less than 90 seconds total.",
    "Super chill seller and very fast MM. 5 stars!",
    "Legit! Thought I might get scammed elsewhere so came here—glad I did.",
    "Vouch! Smooth CashApp transaction, received everything immediately.",
    "Great communication from start to finish. 100% vouch.",
    "Trusted MM! Held both sides and completed the swap cleanly.",
    "Fastest Robux supplier I've used. Will be a regular customer.",
    "Vouch! No delays, no excuses, just straight business.",
    "Super professional staff and instant ticket handling.",
    "Legit seller! Bought twice today and both went flawlessly.",
    "Vouch for the MM, super responsive and kept the trade safe.",
    "Delivered right away in private server. 10/10 vouch!",
    "Smooth $80 trade, went first without any worries.",
    "Great prices and even better service. Vouch!",
    "Vouch! Fast crypto transaction, seller confirmed right away.",
    "Super helpful and legit, answered all my questions before buying.",
    "Trusted middleman, smooth 3-way trade completed cleanly.",
    "Instant delivery! Couldn't ask for a better experience.",
    "Vouch! 100% safe and secure, will recommend to my friends.",
    "Bought a gamepass, gifted within 30 seconds of payment.",
    "Legit! Very friendly seller and quick MM response.",
    "Vouch! Smooth transaction, zero complications.",
    "Reliable as always. My go-to shop for everything.",
    "Fast, safe, and easy. 10/10 vouch for the team!",
    "Vouch! Went first with gift card, redeemed and delivered fast.",
    "Super smooth MM deal, both parties happy. Thanks!",
    "Legit seller, very transparent and quick to deliver.",
    "Vouch! Best rates I've seen and instant delivery.",
    "Handled a huge bundle trade effortlessly. Massive vouch!",
    "Quick response time and super polite. 5/5 stars.",
    "Vouch! Trusted with $150+ deal, everything went smoothly.",
    "No issues at all, fast trade and great communication.",
    "Legit! Got my order right on time as promised.",
    "Vouch for the seller, super fast and reliable.",
    "MM was super quick to claim the ticket and finish the trade.",
    "Smooth PayPal transaction, instant in-game delivery.",
    "Vouch! Honest seller and great customer support.",
    "10/10 would trade again, very trustworthy.",
    "Fastest delivery in the market, hands down. Vouch!",
    "Vouch! Clean account/item transfer with zero issues.",
    "Super safe MM service, felt completely secure the whole time.",
    "Legit and professional! Will definitely return.",
    "Vouch! Paid via USDT, received items in under 2 minutes.",
    "Great experience, smooth and hassle-free.",
    "Vouch for both seller and MM! Top-tier service.",
    "Quickest ticket response ever, got my items fast.",
    "100% trusted, never disappoints.",
    "Vouch! Fair prices and super fast delivery.",
    "Smooth trade, seller was online and ready immediately.",
    "Legit MM! Verified all items carefully before completing.",
    "Vouch! Bought 25k Robux, smooth and safe process.",
    "Super reliable shop, always stocked and ready.",
    "Vouch! Great communication and instant delivery.",
    "Fast and trustworthy, couldn't ask for more.",
    "Vouch! Completed a complex multi-item trade smoothly.",
    "Legit seller, went first and everything went great.",
    "10/10 vouch, super fast and friendly!",
    "Vouch! Smooth LTC payment and immediate handoff.",
    "Trusted middleman, super fast and polite.",
    "Bought a rare item, delivered within seconds. Vouch!",
    "Legit! Best trading server I've joined.",
    "Vouch! Zero problems, super smooth from start to finish.",
    "Fast response, clean trade, 100% legit.",
    "Vouch for the MM, made the trade super easy for both of us.",
    "Great seller, very patient and trustworthy.",
    "Vouch! Instant delivery after payment confirmation.",
    "Smooth $60 deal, highly recommend this shop!",
    "Legit and fast! Will be buying more soon.",
    "Vouch! Everything was exactly as described.",
    "Super quick MM service, didn't keep us waiting at all.",
    "100% vouch, smooth and secure transaction.",
    "Fastest shop around, delivered before I even closed my wallet app.",
    "Vouch! Trusted with rare limiteds, super safe.",
    "Great communication, fast delivery, 5 stars.",
    "Vouch! Smooth trade, no middleman issues whatsoever.",
    "Legit seller! Very responsive and easy to work with.",
    "Vouch! Paid first, got my items right away.",
    "Super clean transaction, will definitely use again.",
    "Vouch for the team, best service on Discord!",
    "Fast and reliable, 10/10 experience.",
    "Vouch! Smooth crypto deal, zero delays.",
    "Trusted MM, handled everything professionally.",
    "Legit! Quick delivery and great prices.",
    "Vouch! Bought a starter bundle, received instantly.",
    "Super friendly and trustworthy seller. Vouch!",
    "Smooth transaction from start to finish. 10/10.",
    "Vouch! Fast gamepass delivery, very satisfied.",
    "Legit MM service, super secure and quick.",
    "Vouch! Went first without hesitation, 100% worth it.",
    "Quick, professional, and legit. Vouch!",
    "Vouch! Best shop for fast and safe trades.",
    "Super smooth handoff in game, thanks a lot!",
    "Legit seller, delivered in less than 60 seconds.",
    "Vouch! Trusted middleman for high-value trades.",
    "Great prices, fast service, zero complaints.",
    "Vouch! Smooth PayPal deal, instant delivery.",
    "100% legit, super easy process.",
    "Vouch! Fast reply and smooth completion.",
    "Trusted seller, always delivers on time.",
    "Vouch for the MM, quick and unbiased.",
    "Super fast delivery, very happy with my purchase!",
    "Legit! Cleanest shop experience I've had.",
    "Vouch! Smooth $45 transaction, 10/10.",
    "Quick and safe trade, will come back again.",
    "Vouch! Reliable seller and fast MM.",
    "Instant service, great communication. Vouch!",
    "Legit! Everything went smoothly with zero stress.",
    "Vouch! Fast transfer and polite staff.",
    "Super trustworthy, went first and had no issues.",
    "Vouch! Best middleman experience so far.",
    "Quick delivery and fair pricing. 5/5!",
    "Legit seller! Handled my order right away.",
    "Vouch! Smooth trade, everything verified properly.",
    "10/10 vouch, super responsive and legit.",
    "Vouch! Fast BTC/LTC confirmation and instant delivery.",
    "Trusted shop, never had a bad experience.",
    "Vouch! Great seller, super smooth process.",
    "Fastest MM around, completed in under 2 minutes.",
    "Legit! Bought multiple items, all delivered fast.",
    "Vouch! Zero hassle, straight to the point.",
    "Super reliable and professional. 10/10.",
    "Vouch! Smooth transaction, highly recommended.",
    "Quick response and instant delivery. Vouch!",
    "Legit MM! Kept both sides safe during the swap.",
    "Vouch! Paid first, received everything immediately.",
    "Great service, very trustworthy seller.",
    "Vouch! Fast and clean trade, will return.",
    "100% legit, best place to buy and trade.",
    "Vouch! Smooth deal, no issues at all.",
    "Super fast ticket support and delivery. Vouch!",
    "Legit seller, very helpful and quick.",
    "Vouch! Trusted with a big order, delivered everything.",
    "Quick, safe, and reliable. 5 stars!",
    "Vouch for the MM, super smooth and fast.",
    "Instant delivery, great prices, 100% legit.",
    "Vouch! Clean trade and friendly communication.",
    "Super satisfied with the speed and service. Vouch!",
    "Legit! Everything went off without a hitch.",
    "Vouch! Fast payment verification and delivery.",
    "Trusted middleman, super easy to work with.",
    "Vouch! Bought Robux again, always fast and safe.",
    "10/10 service, very reliable shop.",
    "Vouch! Smooth cross-game trade with MM.",
    "Fast and legit, couldn't ask for better.",
    "Vouch! Great experience, will definitely buy again.",
    "Super quick delivery, 100% trusted.",
    "Vouch! Polite seller and smooth transaction.",
    "Legit MM service, fast and dependable.",
    "Vouch! Everything delivered as promised.",
    "Quickest trade I've done all week. Vouch!",
    "100% legit seller, zero problems.",
    "Vouch! Smooth transaction and instant response.",
    "Trusted with high-tier trade, flawless execution.",
    "Vouch! Fast, friendly, and 100% reliable.",
    "Great shop, always fast and trustworthy.",
    "Vouch! Smooth deal, MM was super helpful.",
    "Legit! Received my items right away.",
    "Vouch! Best prices and fastest delivery.",
    "Super clean and safe trade. 10/10 vouch!",
    "Vouch! Went first, super smooth and legit.",
    "Fast response, great service, 5/5.",
    "Vouch! Reliable MM and fast seller.",
    "100% trusted, smooth transaction every time.",
    "Vouch! Instant delivery and zero issues.",
    "Legit seller! Very professional and quick.",
    "Vouch! Smooth $100+ deal handled cleanly.",
    "Super fast and safe, highly recommend!",
    "Vouch! Great communication and fast handoff.",
    "Trusted shop, will definitely be back.",
    "Vouch! Cleanest MM service on Discord.",
    "Fast delivery, legit items, 10/10.",
    "Vouch! Smooth and easy transaction.",
    "100% legit, thanks for the quick service!",
    "Vouch! Reliable, fast, and trustworthy.",
    "Super smooth trade, 5 stars all around.",
    "Vouch! Best trading hub, always legit.",
    "Fast, secure, and hassle-free. Massive vouch!",
    "Vouch! Delivered instantly, 10/10 seller.",
    "Legit and trustworthy, pleasure doing business!",
]

# ==============================================================================
# 4. DISCORD BOT & RANDOM-INTERVAL AUTO-VOUCH ENGINE
# ==============================================================================
class AutoVouchBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True

        super().__init__(
            command_prefix=["$", "/"],
            intents=intents,
            help_command=None
        )

        self.vouch_channel_id: int | None = None
        self.seller_role_id: int | None = None
        self.buyer_role_id: int | None = None
        self.mm_role_id: int | None = None
        self.min_delay_minutes: int = 1
        self.max_delay_minutes: int = 5
        self.total_sent: int = 0
        self.is_running: bool = False
        self.vouch_task: asyncio.Task | None = None

    def pick_participants(self, guild: discord.Guild):
        seller_role = guild.get_role(self.seller_role_id) if self.seller_role_id else None
        buyer_role = guild.get_role(self.buyer_role_id) if self.buyer_role_id else None
        mm_role = guild.get_role(self.mm_role_id) if self.mm_role_id else None

        if not (seller_role and buyer_role and mm_role):
            return None, "One or more roles (`Seller`, `Buyer`, `MM`) are not configured."

        sellers = [m for m in seller_role.members if not m.bot]
        buyers = [m for m in buyer_role.members if not m.bot]
        mms = [m for m in mm_role.members if not m.bot]

        if not sellers or not buyers or not mms:
            return None, "Each configured role must have at least 1 non-bot member."

        seller = random.choice(sellers)
        buyer_pool = [m for m in buyers if m.id != seller.id] or buyers
        buyer = random.choice(buyer_pool)
        mm_pool = [m for m in mms if m.id not in (seller.id, buyer.id)] or mms
        mm = random.choice(mm_pool)

        return (seller, buyer, mm), None

    def build_vouch_embed(self, guild: discord.Guild, seller: discord.Member, buyer: discord.Member, mm: discord.Member) -> discord.Embed:
        stars_count = random.choice([4, 5])
        stars_display = "⭐" * stars_count + f" ({stars_count}/5)"
        feedback_text = random.choice(FEEDBACK_POOL)

        proof_links = load_proofs()
        proof_url = random.choice(proof_links) if proof_links else None

        self.total_sent += 1

        embed = discord.Embed(
            title=f"✅ Verified Transaction Vouch #{self.total_sent}",
            description=f"**Feedback:**\n> *\"{feedback_text}\"*",
            color=0x57F287 if stars_count == 5 else 0xFEE75C,
            timestamp=datetime.utcnow()
        )

        if guild.icon:
            embed.set_author(name=f"{guild.name} • Automated Vouch System", icon_url=guild.icon.url)
        else:
            embed.set_author(name=f"{guild.name} • Automated Vouch System")

        embed.add_field(name="🛒 SELLER", value=f"{seller.mention}\n`{seller.name}`", inline=True)
        embed.add_field(name="💳 BUYER", value=f"{buyer.mention}\n`{buyer.name}`", inline=True)
        embed.add_field(name="🤝 MM", value=f"{mm.mention}\n`{mm.name}`", inline=True)
        embed.add_field(name="🌟 RATING", value=stars_display, inline=False)

        if proof_url:
            embed.set_image(url=proof_url)

        embed.set_thumbnail(url=buyer.display_avatar.url)
        embed.set_footer(text=f"Transaction ID: VX-{random.randint(100000, 999999)} • Verified Proof")
        return embed

    async def random_vouch_worker(self):
        """Background worker that posts vouches at randomized intervals between min and max minutes."""
        await self.wait_until_ready()
        while self.is_running:
            # Pick a random float duration in seconds between min_delay_minutes and max_delay_minutes
            wait_seconds = random.uniform(self.min_delay_minutes * 60, self.max_delay_minutes * 60)
            await asyncio.sleep(wait_seconds)

            if not self.is_running:
                break

            if not self.vouch_channel_id:
                continue

            channel = self.get_channel(self.vouch_channel_id)
            if not channel or not isinstance(channel, discord.TextChannel):
                continue

            participants, error = self.pick_participants(channel.guild)
            if error:
                print(f"[!] Auto-Vouch Skipped: {error}")
                continue

            seller, buyer, mm = participants
            embed = self.build_vouch_embed(channel.guild, seller, buyer, mm)
            ping_line = f"**SELLER:** {seller.mention} | **BUYER:** {buyer.mention} | **MM:** {mm.mention}"
            await channel.send(content=ping_line, embed=embed)


bot = AutoVouchBot()

# ==============================================================================
# 5. APP_COMMANDS.GROUP DEFINITION & $SYNC COMMAND
# ==============================================================================
vouch_group = app_commands.Group(name="vouch", description="Manage and configure the automated vouch system.")

@vouch_group.command(name="configure", description="Set roles, destination channel, and random delay range (min to max minutes).")
@app_commands.describe(
    channel="Channel where auto-vouches will be posted",
    seller_role="Role representing store sellers",
    buyer_role="Role representing store buyers",
    mm_role="Role representing middleman staff",
    min_minutes="Minimum delay between vouches in minutes (1 to 30)",
    max_minutes="Maximum delay between vouches in minutes (1 to 30)"
)
@app_commands.checks.has_permissions(administrator=True)
async def vouch_configure(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    seller_role: discord.Role,
    buyer_role: discord.Role,
    mm_role: discord.Role,
    min_minutes: int,
    max_minutes: int
):
    if not (1 <= min_minutes <= 30) or not (1 <= max_minutes <= 30):
        return await interaction.response.send_message("❌ Both `min_minutes` and `max_minutes` must be between **1** and **30**.", ephemeral=True)

    if min_minutes > max_minutes:
        return await interaction.response.send_message("❌ `min_minutes` cannot be greater than `max_minutes`.", ephemeral=True)

    bot.vouch_channel_id = channel.id
    bot.seller_role_id = seller_role.id
    bot.buyer_role_id = buyer_role.id
    bot.mm_role_id = mm_role.id
    bot.min_delay_minutes = min_minutes
    bot.max_delay_minutes = max_minutes

    embed = discord.Embed(
        title="⚙️ Auto-Vouch System Configured",
        description=(
            f"📢 **Channel:** {channel.mention}\n"
            f"🛒 **Seller Role:** {seller_role.mention}\n"
            f"💳 **Buyer Role:** {buyer_role.mention}\n"
            f"🤝 **MM Role:** {mm_role.mention}\n"
            f"⏱️ **Random Delay Range:** `{min_minutes} - {max_minutes} minute(s)`"
        ),
        color=0x5865F2
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@vouch_group.command(name="toggle", description="Start or stop the automated vouch loop (on/off).")
@app_commands.describe(state="Select 'On / Start' or 'Off / Stop'")
@app_commands.choices(state=[
    app_commands.Choice(name="On / Start", value="on"),
    app_commands.Choice(name="Off / Stop", value="off")
])
@app_commands.checks.has_permissions(administrator=True)
async def vouch_toggle(interaction: discord.Interaction, state: str):
    if state == "on":
        if not bot.vouch_channel_id or not (bot.seller_role_id and bot.buyer_role_id and bot.mm_role_id):
            return await interaction.response.send_message("⚠️ Please run `/vouch configure` first!", ephemeral=True)

        if not bot.is_running:
            bot.is_running = True
            bot.vouch_task = bot.loop.create_task(bot.random_vouch_worker())

        await interaction.response.send_message(
            f"✅ **Auto-Vouch Started!** Posting every **{bot.min_delay_minutes} to {bot.max_delay_minutes} minute(s)** in <#{bot.vouch_channel_id}>."
        )
    else:
        bot.is_running = False
        if bot.vouch_task and not bot.vouch_task.done():
            bot.vouch_task.cancel()
        await interaction.response.send_message("🛑 **Auto-Vouch Stopped.**")

@vouch_group.command(name="test", description="Send an immediate test vouch preview in the current channel.")
@app_commands.checks.has_permissions(administrator=True)
async def vouch_test(interaction: discord.Interaction):
    participants, error = bot.pick_participants(interaction.guild)
    if error:
        return await interaction.response.send_message(f"❌ **Cannot generate test vouch:** {error}", ephemeral=True)

    seller, buyer, mm = participants
    embed = bot.build_vouch_embed(interaction.guild, seller, buyer, mm)
    ping_line = f"**SELLER:** {seller.mention} | **BUYER:** {buyer.mention} | **MM:** {mm.mention}"

    await interaction.response.send_message("✅ Test vouch generated below:", ephemeral=True)
    await interaction.channel.send(content=ping_line, embed=embed)

@vouch_group.command(name="status", description="View current auto-vouch settings, proof count, and statistics.")
@app_commands.checks.has_permissions(administrator=True)
async def vouch_status(interaction: discord.Interaction):
    status_text = "🟢 Running" if bot.is_running else "🔴 Stopped"
    ch_text = f"<#{bot.vouch_channel_id}>" if bot.vouch_channel_id else "`Not Set`"
    s_text = f"<@&{bot.seller_role_id}>" if bot.seller_role_id else "`Not Set`"
    b_text = f"<@&{bot.buyer_role_id}>" if bot.buyer_role_id else "`Not Set`"
    m_text = f"<@&{bot.mm_role_id}>" if bot.mm_role_id else "`Not Set`"
    proofs_count = len(load_proofs())

    embed = discord.Embed(title="📊 Auto-Vouch System Dashboard", color=0x5865F2)
    embed.add_field(name="Engine Status", value=status_text, inline=True)
    embed.add_field(name="Delay Window", value=f"`{bot.min_delay_minutes} - {bot.max_delay_minutes} min`", inline=True)
    embed.add_field(name="Vouches Sent", value=f"`{bot.total_sent}`", inline=True)
    embed.add_field(name="Target Channel", value=ch_text, inline=True)
    embed.add_field(name="Feedback Pool", value=f"`{len(FEEDBACK_POOL)} quotes`", inline=True)
    embed.add_field(name="Proof Images File", value=f"`{proofs_count} links` (`proofs.txt`)", inline=True)
    embed.add_field(name="Assigned Roles", value=f"**Seller:** {s_text}\n**Buyer:** {b_text}\n**MM:** {m_text}", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@vouch_group.command(name="addproof", description="Add a new direct image URL to proofs.txt.")
@app_commands.describe(image_url="Direct image link (https://...)")
@app_commands.checks.has_permissions(administrator=True)
async def vouch_addproof(interaction: discord.Interaction, image_url: str):
    if not image_url.startswith(("http://", "https://")):
        return await interaction.response.send_message("❌ Please provide a valid direct image URL (`https://...`).", ephemeral=True)

    append_proof(image_url)
    total = len(load_proofs())
    await interaction.response.send_message(f"✅ Added proof image to `proofs.txt`! Total active proof images: **{total}**.", ephemeral=True)

bot.tree.add_command(vouch_group)

# Instant Force-Sync Command ($sync)
@bot.command(name="sync")
@commands.has_permissions(administrator=True)
async def sync_commands(ctx):
    """Manually force-syncs slash commands to the current server instantly."""
    try:
        bot.tree.copy_global_to(guild=ctx.guild)
        synced = await bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"✅ Successfully synced `{len(synced)}` slash command(s) to this server!")
    except Exception as e:
        await ctx.send(f"❌ Failed to sync commands: `{e}`")

# ==============================================================================
# 6. ON_READY & STARTUP
# ==============================================================================
@bot.event
async def on_ready():
    load_proofs()
    print("==================================================")
    print(f"[+] Logged in as: {bot.user} (ID: {bot.user.id})")
    print(f"[+] Loaded {len(FEEDBACK_POOL)} feedbacks & {len(load_proofs())} proof images from proofs.txt")
    print("==================================================")
    if GUILD_ID:
        guild = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Verified Vouches | /vouch status"))


if __name__ == "__main__":
    bot.run(TOKEN)
