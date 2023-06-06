# -*- coding: utf-8 -*-

# IMPORTS
import sys

sys.path.append("modules")

import discordTennis
import export
import threading
import os

# KEEPING ALIVE (en cas de deploiement sur replit)
if "Replit" in os.environ:
  import keep_alive
  keep_alive.keep_alive()


def main():
  thread1 = threading.Thread(target=export.main)
  thread1.start()
  discordTennis.main()


main()