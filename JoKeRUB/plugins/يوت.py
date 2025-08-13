import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from JoKeRUB import l313l
from telethon import events

# إنشاء مجلد التنزيلات
os.makedirs("downloads", exist_ok=True)

def get_audio_from_clipto(youtube_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.clipto.com/ar/media-downloader/youtube-downloader")
        time.sleep(3)

        input_box = driver.find_element(By.NAME, "url")
        input_box.send_keys(youtube_url)
        driver.find_element(By.CLASS_NAME, "btn-download").click()
        time.sleep(7)

        audio_link = driver.find_element(By.PARTIAL_LINK_TEXT, ".mp3").get_attribute("href")
        return audio_link
    except Exception as e:
        print("Clipto error:", e)
        return None
    finally:
        driver.quit()

@l313l.on(events.NewMessage(pattern=r"^.تحميل يوت (.+)"))
async def clipto_download(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        return await event.reply("❌ اكتب الرابط بعد الأمر مثل:\n.تحميل يوت https://youtube.com/watch?v=...")

    await event.reply("🔄 جاري استخراج رابط الصوت من Clipto...")

    audio_url = get_audio_from_clipto(query)
    if not audio_url:
        return await event.reply("❌ لم أتمكن من استخراج الرابط من الموقع.")

    temp = f"downloads/{os.urandom(4).hex()}.mp3"
    try:
        resp = requests.get(audio_url, timeout=20).content
        with open(temp, "wb") as f:
            f.write(resp)

        await event.reply(file=temp, caption="*- Uploader : @laiecbot*", parse_mode="markdown")
        os.remove(temp)
    except Exception:
        await event.reply("⚠️ حدث خطأ أثناء تحميل أو إرسال الملف.")
