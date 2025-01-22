import requests

def check_discord_api():
    try:
        response = requests.get("https://discord.com/api/v10/gateway")
        return response.status_code == 200
    except Exception as e:
        return False

def check_twitch_api(client_id):
    try:
        headers = {"Client-ID": client_id}
        response = requests.get("https://api.twitch.tv/helix/streams", headers=headers)
        return response.status_code == 200
    except Exception as e:
        return False

def check_discord_api():
    try:
        response = requests.get("https://discord.com/api/v10/gateway")
        return response.status_code == 200
    except Exception as e:
        print(f"Discord API check failed: {e}")
        return False
