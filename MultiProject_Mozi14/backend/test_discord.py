# backend/test_discord.py
import os
import requests

print("Webhook URL:", os.getenv("DISCORD_WEBHOOK_URL"))

url = os.getenv("DISCORD_WEBHOOK_URL")
if url:
    r = requests.post(url, json={"content": "Render teszt üzenet"})
    print(r.status_code, r.text)
else:
    print("⚠️ DISCORD_WEBHOOK_URL nincs beállítva!")
  
