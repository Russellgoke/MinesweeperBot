from collections import defaultdict

class EventDispatcher:
    def __init__(self):
        self.listeners = defaultdict(list)

    def register(self, event_type, listener):
        self.listeners[event_type].append(listener)

    def unregister(self, event_type, listener):
        self.listeners[event_type].remove(listener)

    def dispatch(self, event_type, data=None):
        for listener in self.listeners.get(event_type, []):
            listener(data)
