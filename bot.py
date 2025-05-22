import discord
from discord.ext import commands
import os

# Railway Umgebungsvariablen
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
NACHRICHTENGRENZE = int(os.getenv("MESSAGE_LIMIT", 200))

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

nachrichten_zaehler = 0

# 📜 Regel- & Disclaimer-Text
DISCLAIMER_TEXT = (
    "**📢 Wichtiger Disclaimer:**\n\n"
    "Forex, Futures, Kryptowährungen und Aktien unterliegen Kursveränderungen und sind gehebelte Finanzinstrumente mit erheblichen Verlustrisiken. "
    "Diese Risiken können Ihre Kontoeinlage überschreiten – bis hin zu **unbegrenzten Verlusten**.\n\n"
    "Diese Produkte sind **nicht für alle Investoren geeignet**. "
    "Bitte informieren Sie sich sorgfältig über die Risiken und ziehen Sie ggf. eine **externe Beratung** hinzu. "
    "**Vergangene Gewinne garantieren keine zukünftigen Erträge.**\n"
    "_Diese Inhalte stellen keine Anlageberatung dar._\n\n"
    "---\n\n"
    "**📜 Regeln der Community:**\n\n"
    "1️⃣ Freundlichkeit hat oberste Priorität – wir unterstützen und respektieren einander.\n"
    "2️⃣ Beleidigungen, Rassismus oder Spam sind strengstens untersagt.\n"
    "3️⃣ Inhalte sind **nur für den Eigengebrauch** bestimmt – keine Weitergabe an Dritte.\n"
    "4️⃣ Mit dem Beitritt zum Server **akzeptierst du diese Regeln**.\n\n"
    "---\n\n"
    "**📊 Verhalten in Analyse-Textkanälen (Future, Forex, Krypto, Aktien):**\n\n"
    "- Verwende **gut lesbare Charts** mit Timeframes (TF).\n"
    "- Gib bei Open-Calls **SL (Stop Loss)** und **TP (Take Profit)** an.\n"
    "- Zeichne erkennbar **Patterns** ein und begründe sie ggf.\n"
    "- Bleib **on-topic** – alles andere bitte in 💎 ⁠community-chat.\n"
    "- Indices-Kanal = Diskussionen zu Pro & Contra einer Analyse.\n\n"
    "---\n\n"
    "**📌 Regelverstöße:**\n"
    "- 1. Verstoß → 24h Timeout\n"
    "- 2. Verstoß → 7 Tage Timeout\n"
    "- 3. Verstoß → permanenter Timeout\n\n"
    "_Das Team behält sich vor, die Regeln jederzeit zu ändern._"
)

# ✅ View mit Button – jetzt mit custom_id!
class RegelnButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="📜 Regeln & Disclaimer anzeigen",
        style=discord.ButtonStyle.primary,
        custom_id="regeln_button"
    )
    async def regel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(DISCLAIMER_TEXT, ephemeral=True)

# 📦 Embed für die 500-Nachrichten-Nachricht
def create_embed():
    embed = discord.Embed(
        title="💬 Liebe Community",
        description=(
            "Bitte denkt immer daran, **respektvoll miteinander umzugehen**.\n"
            "Jeder hat mal bei null angefangen – daher sind **Unterstützung** und **Verständnis** entscheidend.\n\n"
            "📌 Um die **Regeln** und den **Disclaimer** zu sehen, klickt auf den Button unten!"
        ),
        color=discord.Color.blurple()
    )
    return embed

# 🔁 Slash-Command /regeln
@bot.tree.command(name="regeln", description="Zeigt dir die Regeln und den Disclaimer")
async def regeln_command(interaction: discord.Interaction):
    await interaction.response.send_message(DISCLAIMER_TEXT, ephemeral=True)

# 🔁 Slash-Command /start
@bot.tree.command(name="start", description="Begrüßung und Übersicht über die Funktionen")
async def start_command(interaction: discord.Interaction):
    text = (
        "**👋 Liebe Community!**\n\n"
        "Dieser Bot hilft dir, immer informiert zu bleiben und die Community-Regeln im Blick zu behalten.\n\n"
        "Hier sind die wichtigsten Befehle:\n"
        "• `/regeln` – Zeigt dir die Regeln und den wichtigen Disclaimer.\n\n"
        "Wenn du Fragen hast, melde dich gerne per Support-Ticket bei uns.\n\n"
        "**Viel Spaß & bleib respektvoll!** ✨"
    )
    await interaction.response.send_message(text, ephemeral=True)

# 🔁 Bot ready
@bot.event
async def on_ready():
    print(f"✅ Bot läuft als: {bot.user}")
    bot.add_view(RegelnButton())  # Persistenter Button

    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash-Commands synchronisiert: {len(synced)} Befehle")
    except Exception as e:
        print(f"❌ Fehler beim Slash-Command-Sync: {e}")

# 🔁 Nachrichten zählen
@bot.event
async def on_message(message):
    global nachrichten_zaehler

    if message.author.bot or message.channel.id != CHANNEL_ID:
        return

    nachrichten_zaehler += 1

    if nachrichten_zaehler >= NACHRICHTENGRENZE:
        embed = create_embed()
        view = RegelnButton()
        await message.channel.send(embed=embed, view=view)
        nachrichten_zaehler = 0

    await bot.process_commands(message)

bot.run(TOKEN)
