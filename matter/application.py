import asyncio
import logging
import signal
from collections.abc import AsyncIterator
from typing import final


@final
class EventIteratorWrapper(AsyncIterator):
    def __init__(self, event):
        self._event = event

    async def _to_list(self):
        items = []

        async for item in self:
            items.append(item)

        return items

    def __await__(self):
        return self._to_list().__await__()

    def __aiter__(self) -> 'EventIteratorWrapper':
        return self

    async def __anext__(self):
        try:
            event = next(self._event)
        except StopIteration:
            raise StopAsyncIteration

        return event


class Application:

    HANDLED_SIGNALS = signal.SIGINT, signal.SIGTERM,

    def __init__(self, loop=None):
        self._loop = loop or asyncio.get_running_loop()
        self._queue = asyncio.Queue(maxsize=15)

        self.should_exit = False

    def add_job(self, target, *args) -> None:
        self._loop.call_soon_threadsafe(self.async_add_job, target, *args)

    def async_add_job(
            self,
            target,
            *args,
    ):
        check_target = target
        if asyncio.iscoroutine(check_target):
            task = self._loop.create_task(target)
        elif asyncio.iscoroutinefunction(check_target):
            task = self._loop.create_task(target(*args))
        else:
            task = self._loop.run_in_executor(None, target, *args)

        return task

    async def run(self):
        while True:
            if self.should_exit:
                break

            await asyncio.sleep(1)

    async def startup(self):
        self.install_signal_handlers()
        task = self.async_add_job(self.run())
        await asyncio.sleep(1)

    async def shutdown(self, sockets=None):
        pass

    def install_signal_handlers(self):
        try:
            for sig in self.HANDLED_SIGNALS:
                self._loop.add_signal_handler(sig, self.handle_exit, sig)
        except NotImplementedError:
            for sig in self.HANDLED_SIGNALS:
                signal.signal(sig, self.handle_exit)

    def handle_exit(self, sig):
        logging.error(f'Got signal {sig}')

        for task in asyncio.all_tasks(loop=self._loop):
            task.cancel()

        self._loop.remove_signal_handler(signal.SIGTERM)
        self._loop.add_signal_handler(signal.SIGINT, lambda: None)

        self.should_exit = True
