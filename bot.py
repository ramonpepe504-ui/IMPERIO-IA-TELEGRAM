import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import requests, urllib.parse, sqlite3
from datetime import datetime

TOKEN = os.getenv("TOKEN") or "8558587887:AAFTqEmjAVfiPbKAND7Xcet5ANO7OA0AIHA"

conn = sqlite3.connect("imperio_memoria.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS programas (id INTEGER PRIMARY KEY, user TEXT, idea TEXT, fecha TEXT)")
conn.commit()

def crear_audio(texto, nombre="clase.mp3"):
    try:
        from gtts import gTTS
        from moviepy.editor import AudioFileClip, concatenate_audioclips
        tts = gTTS(texto[:350], lang='es', slow=False)
        tts.save("temp_tts.mp3")
        if os.path.exists("mi_voz.mp3"):
            intro = AudioFileClip("mi_voz.mp3").subclip(0, min(2, AudioFileClip("mi_voz.mp3").duration))
            clase = AudioFileClip("temp_tts.mp3")
            final = concatenate_audioclips([intro, clase])
            final.write_audiofile(nombre, logger=None)
            os.remove("temp_tts.mp3")
        else:
            os.rename("temp_tts.mp3", nombre)
        return True
    except: return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botones = [
        [InlineKeyboardButton("💻 Crear Programa", callback_data='crear'), InlineKeyboardButton("🎓 Ser Programador V16", callback_data='serprog')],
        [InlineKeyboardButton("🛡️ Antivirus", callback_data='antivirus'), InlineKeyboardButton("🧬 Vuln Scanner", callback_data='vuln')],
        [InlineKeyboardButton("🎵 Musica YouTube", callback_data='musica'), InlineKeyboardButton("🎬 Pelicula", callback_data='peli')],
        [InlineKeyboardButton("⚖️ Denuncia Legal", callback_data='denuncia'), InlineKeyboardButton("🎨 Imagen", callback_data='img')],
        [InlineKeyboardButton("🎤 Guardar Mi Voz", callback_data='guardarvoz')],
    ]
    await update.message.reply_text("🦍👑 IMPERIO V16 @PocholoMonkeyreportes_bot - MISMO BOT NIVEL DIOS\n\n/codigo idea\n/serprogramador\n/antivirus url\n/vuln misitio.com\n/musica trap oscuro\n/peli gorila hacker\n/denuncia @usuario motivo\n/img logo gorila", reply_markup=InlineKeyboardMarkup(botones))

async def click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    await q.message.reply_text(f"Usa comando: /{q.data}")

async def ser_programador(update, context):
    texto = "Hola mi gente soy la maestra V16 imperio total. Hoy nivel dios antivirus vuln scanner musica pelicula denuncias."
    await update.reply_text("🎓 CLASE V16")
    if crear_audio(texto, "clase16.mp3"):
        await update.reply_voice(voice=open("clase16.mp3","rb")); os.remove("clase16.mp3")
async def serprog_cmd(u,c): await ser_programador(u.message,c)
async def antivirus_cmd(u,c):
    t=" ".join(c.args) or "archivo"
    r=requests.get(f"https://text.pollinations.ai/{urllib.parse.quote(f'Analiza antivirus {t} espanol')}",timeout=30)
    await u.message.reply_text(r.text[:3000])
async def vuln_cmd(u,c):
    t=" ".join(c.args) or "misitio.com"
    r=requests.get(f"https://text.pollinations.ai/{urllib.parse.quote(f'Vuln scanner {t} puertos fix espanol')}",timeout=30)
    await u.message.reply_text(r.text[:3500])
async def musica_cmd(u,c):
    t=" ".join(c.args) or "LoFi"
    r=requests.get(f"https://text.pollinations.ai/{urllib.parse.quote(f'Prompt Suno AI musica {t} BPM')}",timeout=30)
    await u.message.reply_text(r.text[:3500])
async def peli_cmd(u,c):
    t=" ".join(c.args) or "Gorila hacker"
    r=requests.get(f"https://text.pollinations.ai/{urllib.parse.quote(f'Guion pelicula {t} prompts Pika Runway')}",timeout=40)
    await u.message.reply_text(r.text[:3500])
async def denuncia_cmd(u,c):
    t=" ".join(c.args) or "usuario"
    r=requests.get(f"https://text.pollinations.ai/{urllib.parse.quote(f'Denuncia legal {t} donde reportar abuse')}",timeout=30)
    await u.message.reply_text(r.text[:3500])
async def guardar_voz(u,c):
    vf=await u.message.voice.get_file(); await vf.download_to_drive("mi_voz_original.ogg")
    from moviepy.editor import AudioFileClip; AudioFileClip("mi_voz_original.ogg").write_audiofile("mi_voz.mp3",logger=None)
    await u.message.reply_text("✅ VOZ GUARDADA")
async def codigo_cmd(u,c):
    idea=" ".join(c.args); r=requests.get(f"https://text.pollinations.ai/{urllib.parse.quote(f'Programa python que haga {idea}')}",timeout=40)
    await u.message.reply_text(r.text[:3500])
async def img_cmd(u,c):
    p=" ".join(c.args); r=requests.get(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1024&height=1024&nologo=true",timeout=40)
    open("temp.jpg","wb").write(r.content); await u.message.reply_photo(photo=open("temp.jpg","rb")); os.remove("temp.jpg")

app=Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("serprogramador", serprog_cmd))
app.add_handler(CommandHandler("codigo", codigo_cmd))
app.add_handler(CommandHandler("antivirus", antivirus_cmd))
app.add_handler(CommandHandler("vuln", vuln_cmd))
app.add_handler(CommandHandler("musica", musica_cmd))
app.add_handler(CommandHandler("peli", peli_cmd))
app.add_handler(CommandHandler("denuncia", denuncia_cmd))
app.add_handler(CommandHandler("img", img_cmd))
app.add_handler(MessageHandler(filters.VOICE, guardar_voz))
app.add_handler(CallbackQueryHandler(click))
print("✅ IMPERIO V16 @PocholoMonkeyreportes_bot ACTIVO")
app.run_polling()g()