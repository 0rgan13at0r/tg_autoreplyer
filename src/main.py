import sys
import asyncio

from lib.autoreplyer import AutoReplyer

async def main():
    replyer = AutoReplyer("config.yml")
    await replyer.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, RuntimeError):
        sys.exit(0)
