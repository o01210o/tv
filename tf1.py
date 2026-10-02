import json
import os
import requests

SOURCE_M3U_URL = os.getenv("SOURCE_M3U_URL")


def get_tf1_m3u():
    if not SOURCE_M3U_URL:
        exit(1)

    try:
        response = requests.get(SOURCE_M3U_URL, timeout=15)
        response.raise_for_status()
        lines = response.text.splitlines()

        tf1_url = None
        for i in range(len(lines)):
            if "#EXTINF" in lines[i] and "TF1" in lines[i].upper():
                if i + 1 < len(lines):
                    tf1_url = lines[i + 1].strip()
                    break

        return tf1_url

    except Exception as e:
        print(f"⚠️ Error : {e}")
        exit(1)


def update_msx_json(target_label, new_action):
    file_path = "c.json"

    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = False
    target_full_action = (
        "video:plugin:http://msx.benzac.de/plugins/hls.html?url=" + new_action
    )

    for item in data.get("items", []):
        if item.get("label") == target_label:
            old_action = item.get("action", "")

            if old_action != target_full_action:
                item["action"] = target_full_action
                updated = True
                print(f"Updated action for '{target_label}'")
            else:
                print(f"Action for '{target_label}' is already up to date.")

            break

    if updated:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent="\t", ensure_ascii=False)
        print("File saved successfully.")
    else:
        print("No changes made to the file.")


if __name__ == "__main__":
    m3u = get_tf1_m3u()

    if m3u:
        update_msx_json("TF1", m3u)
    else:
        print("Failed to retrieve TF1 stream URL.")
