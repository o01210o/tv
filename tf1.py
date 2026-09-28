import requests
import os

SOURCE_URL = os.getenv("SOURCE_M3U_URL")
TARGET_FILE = os.path.join("c", "tf1.m3u")

def update_tf1():
	try:
		response = requests.get(SOURCE_URL, timeout=15)
		response.raise_for_status()
		lines = response.text.splitlines()

		tf1_url = None
		for i in range(len(lines)):
			if "#EXTINF" in lines[i] and "TF1" in lines[i].upper():
				if i + 1 < len(lines):
					tf1_url = lines[i+1].strip()
					break

		if tf1_url:
			header = "#EXTM3U"
			infotag = '#EXTINF:-1 tvg-id="TF1.fr" tvg-logo="https://raw.githubusercontent.com/o01210o/tv/refs/heads/main/i/tf1.png",TF1'
			infotag2 = '#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36'
			content = f"{header}\n{infotag}\n{tf1_url}\n{infotag2}"
			
			with open(TARGET_FILE, "w", encoding="utf-8") as f:
				f.write(content)
			print(f"✅ {TARGET_FILE} updated.")
		else:
			print("❌ tf1 not found in source.")

	except Exception as e:
		print(f"⚠️ Error : {e}")
		exit(1)

if __name__ == "__main__":
	update_tf1()
