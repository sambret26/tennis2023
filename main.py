# -*- coding: utf-8 -*-

# IMPORTS
import sys

sys.path.append("modules")

import discordTennis
import export
import asyncio
import os

# KEEPING ALIVE (en cas de deploiement sur replit)
if "Replit" in os.environ:
  import keep_alive
  keep_alive.keep_alive()


# START
async def run_discord():
  await discordTennis.main()


async def run_export():
  export.main()


async def main():
  task1 = asyncio.create_task(run_discord())
  task2 = asyncio.create_task(run_export())
  await asyncio.gather(task1, task2)


asyncio.run(main())
