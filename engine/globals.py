import collections

from engine import actor


class _GameState:

    def __init__(self):
        self.current_room = None
        self._player = actor.create_actor(
            strength=10, stamina=10, will=10, wisdom=10, insanity=0,
            name='player')
        self._text_queue = collections.deque()

    @property
    def player(self):
        return self._player

    def enqueue_text(self, text):
        self._text_queue.append(text)

    def generate_text(self):
        while self._text_queue:
            yield self._text_queue.popleft()


G = _GameState()
