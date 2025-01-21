import os
import json
import asyncio
from bot_core import run_bot

async def main():
    config_files = [f for f in os.listdir('configs') if f.endswith('.json')]
    tasks = []

    for config_file in config_files:
        with open(f'configs/{config_file}') as f:
            config = json.load(f)
            tasks.append(asyncio.create_task(run_bot(config)))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
