import os, json, re, asyncio
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, DEV_ZAID

# ========== تخزين بسيط بديل عن Redis (يحفظ في ملف JSON) ==========
class SimpleStorage:
    def __init__(self, filename="bot_data.json"):
        self.filename = filename
        self.data = self._load()
    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    def _save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    def set(self, key, value):
        self.data[str(key)] = value
        self._save()
    def get(self, key, default=None):
        return self.data.get(str(key), default)
    def delete(self, key):
        if str(key) in self.data:
            del self.data[str(key)]
            self._save()

storage = SimpleStorage()

# تعيين القيم الافتراضية (مثلما كان يفعل Redis في الكود الأصلي)
if not storage.get(f"{DEV_ZAID}:botkey"):
    storage.set(f"{DEV_ZAID}:botkey", "⇜")
if not storage.get(f"{DEV_ZAID}botname"):
    storage.set(f"{DEV_ZAID}botname", "رعد")
if not storage.get(f"{DEV_ZAID}botchannel"):
    storage.set(f"{DEV_ZAID}botchannel", "eFFb0t")

# ========== إنشاء عميل البوت ==========
app = Client(
    f"{DEV_ZAID}_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Plugins")   # توقع وجود مجلد Plugins
)

# ========== دوال مساعدة (مثل Find) ==========
def find_urls(text):
    pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
    return [x[0] for x in re.findall(pattern, text)]

# ========== تشغيل البوت ==========
if __name__ == "__main__":
    print("""
[===========================]
🔮 Bot is starting...
[===========================]
""")
    app.start()
    me = app.get_me()
    print(f"✅ Bot @{me.username} is running!")
    print(f"👑 Owner ID: {OWNER_ID}")
    print("📁 Using JSON storage instead of Redis.")
    idle()