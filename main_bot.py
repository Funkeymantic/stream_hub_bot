import os
import json
import asyncio
from bot_core import run_bot

async def main():
    config_files = [f for f in os.listdir('configs') if f.endswith('.json')]
    if not config_files:
        print("⚠️ No config files found in 'configs' directory.")
        return

    for config_file in config_files:
        with open(f'configs/{config_file}') as f:
            config = json.load(f)
            print(f"📄 Loaded config: {config_file}")
            await run_bot(config)

if __name__ == "__main__":
    asyncio.run(main())
