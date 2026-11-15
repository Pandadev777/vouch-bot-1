import os
import random
from datetime import datetime
from threading import Thread

import discord
from discord import app_commands
from discord.ext import commands, tasks
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

# Start Flask immediately so Render detects the open port right away
server_thread = Thread(target=run_flask, daemon=True)
server_thread.start()

# ==============================================================================
# 2. ENVIRONMENT & CONFIGURATION
# ==============================================================================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID")) if os.getenv("GUILD_ID") else None

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing in your .env file.")

PROOFS_FILE = "proofs.txt"

def load_proofs() -> list[str]:
    """Loads image proof links strictly from proofs.txt, creating the file if missing."""
    if not os.path.exists(PROOFS_FILE):
        with open(PROOFS_FILE, "w", encoding="utf-8") as f:
            f.write("# Paste your 100+ direct image proof URLs below (one link per line)\n")
    
    with open(PROOFS_FILE, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    return links if links else ["https://i.imgur.com/8Q9Z5vE.png"]

def append_proof(url: str):
    """Appends a new image proof URL to proofs.txt."""
    with open(PROOFS_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

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
    "Vouch!
