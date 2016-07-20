"""
Task:
Do fancy shit.
"""

# Import Built-Ins
import logging
import json
from collections import defaultdict
from socket import AF_INET, SOCK_DGRAM, socket

# Import Third-Party

# Import Homebrew


log = logging.getLogger(__name__)


class Receiver:
    """
    Example of how receivers are to be set up.
    """
    def __init__(self, address):
        self.addr = address  # i.e. ('localhost', 6666)

    def deliver(self, message):
        socket(AF_INET, SOCK_DGRAM).sendto(message, self.addr)
        return True

    def __eq__(self, other):
        return self.addr == other.addr

    def __hash__(self):
        return hash(repr(self))


class Subscription:
    """
    Subscription Object; attached subscribers must have a deliver method.

    Used to register receivers, like paper traders for example; These will
    have a message send to them whenever Subscription.deliver() is called.
    """
    def __init__(self):
        self._subscribers = set()

    def attach(self, receiver):
        """
        Add a receiver to the subscription list
        :param receiver: object with a deliver() method.
        :return:
        """
        self._subscribers.add(receiver)

    def detach(self, receiver):
        """
        Remove a receiver from the subscription list.
        :param receiver:
        :return:
        """
        self._subscribers.remove(receiver)

    def deliver(self, message):
        """
        Send message to all subscribers.
        :param message:
        :return:
        """
        for subscriber in self._subscribers:
            subscriber.deliver(message)


class PostOffice:
    """
    Stores subscriptions for exchanges. Whenever a message is received it's
    unpacked and its contents checked.

    Subscribe message:
    ['subscribe', name_of_subscription, receiver object]

    Unsubscribe message:
    ['unsubscribe', name_of_subscription, receiver object]

    Deliver message:
    ['deliver', name_of_subscription, message]

    """
    def __init__(self):
        self._subscriptions = defaultdict(Subscription)

    def get_subscription(self, name):
        return self._subscriptions[name]

    def serve(self, addr):
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(addr)

        while True:
            sender, data = sock.recvfrom(8192)
            action, message = json.loads(data)
            if action is 'subscribe':
                sub, subscriber_addr = message
                self.get_subscription(sub).attach(Receiver(subscriber_addr))
            elif action is 'unsubscribe':
                sub, subscriber_addr = message
                self.get_subscription(sub).detach(Receiver(subscriber_addr))
            elif action is 'deliver':
                sub, msg = message
                self.get_subscription(sub).deliver(msg)





