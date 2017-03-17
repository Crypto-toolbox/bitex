"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew

# Init Logging Facilities
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from bitex.api.WSS import PoloniexWSS

websockets = [PoloniexWSS()]

for wss in websockets:
    wss.start()

while True:
    try:
        for wss in websockets:
            if not wss.data_q.empty():
                try:
                    print(wss.data_q.get(timeout=1))
                except TimeoutError:
                    continue
    except KeyboardInterrupt:
        for wss in websockets:
            wss.stop()
        break
