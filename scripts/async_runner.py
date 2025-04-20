import asyncio


class async_runner:
    """
    This thing's a singleton. Allows me to hav ea single async loop to talk to.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def run_once(self):
        """should be run once per game tick, to start scheduled tasks."""
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    def create_task(self, task: callable, *args, **kwargs) -> asyncio.Task:
        """pass an async function. It will begin execution starting at the next game tick."""
        return self.loop.create_task(task(*args, **kwargs))
