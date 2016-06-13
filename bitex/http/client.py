"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew


logging.basicConfig(level=logging.DEBUG, datefmt='%m-%d %H:%M',
                    filename='{}.log'.format(__name__), filemode='w+')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s %(name)-4s: %(levelname)-4s %(message)s')
console.setFormatter(formatter)
log = logging.getLogger().addHandler(console)