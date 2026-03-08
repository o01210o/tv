import requests
import re
import json
import os



def get_latest_stream_id():
	url = "https://www.youtube.com/i24NEWS_FR/streams"
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
	}
	
	try:
		response = requests.get(url, headers=headers)
		match = re.search(r'"videoId":"([^"]+)"', response.text)
		if match:
			return match.group(1)

	except Exception as e:
		print(f"Error fetching YouTube page: {e}")

	return None



def update_msx_json(new_video_id):
	file_path = "c.json"
	
	if not os.path.exists(file_path):
		print(f"Error: {file_path} not found.")
		return

	with open(file_path, 'r', encoding='utf-8') as f:
		data = json.load(f)

	updated = False
	target_label = "{sp}i24NEWS FR" 

	for item in data.get('items', []):
		if item.get('label') == target_label:
			old_action = item.get('action', '')

			new_action = re.sub(r'(id=)[^&]+', r'\1' + new_video_id, old_action)
			
			if old_action != new_action:
				item['action'] = new_action
				updated = True
				print(f"Success: Updated ID to {new_video_id}")

			else:
				print("Status: ID is already up to date.")

			break

	if updated:
		with open(file_path, 'w', encoding='utf-8') as f:
			json.dump(data, f, indent="\t", ensure_ascii=False)
	else:
		print("No changes made to the file.")



if __name__ == "__main__":

	latest_id = get_latest_stream_id()

	if latest_id:
		update_msx_json(latest_id)
	else:
		print("Failed to retrieve the stream ID.")