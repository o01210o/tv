import requests
import os

SOURCE_URL = os.getenv("SOURCE_M3U_URL")
TARGET_FILE = os.path.join("c", "lci.m3u")

def update_lci():
	try:
		response = requests.get(SOURCE_URL, timeout=15)
		response.raise_for_status()
		lines = response.text.splitlines()

		lci_url = None
		for i in range(len(lines)):
			if "#EXTINF" in lines[i] and "LCI" in lines[i].upper():
				if i + 1 < len(lines):
					lci_url = lines[i+1].strip()
					break

		if lci_url:
			header = "#EXTM3U"
			infotag = '#EXTINF:-1 tvg-id="lci.fr" tvg-logo="https://raw.githubusercontent.com/o01210o/tv/refs/heads/main/i/lci.png",LCI'
			#infotag2 = '#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
			content = f"{header}\n{infotag}\n{lci_url}"
			
			with open(TARGET_FILE, "w", encoding="utf-8") as f:
				f.write(content)
			print(f"✅ {TARGET_FILE} updated.")
		else:
			print("❌ LCI not found in source.")

	except Exception as e:
		print(f"⚠️ Error : {e}")
		exit(1)

if __name__ == "__main__":
	update_lci()
