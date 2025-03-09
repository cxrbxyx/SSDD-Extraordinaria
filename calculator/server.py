"""calculator server application."""

import logging

import Ice

from calculator.calculator import Calculator


class Server(Ice.Application):
    """Ice.Application for the server."""

    def __init__(self) -> None:
        """Initialise the Server objects."""
        super().__init__()
        self.logger = logging.getLogger(__file__)

    def run(self, args: list[str]) -> int:
        """Execute the main server actions..

        It will initialise the needed middleware elements in order to execute the server.
        """
        servant = Calculator()
        adapter = self.communicator().createObjectAdapter("calculator")
        proxy = adapter.add(servant, self.communicator().stringToIdentity("calculator"))
        self.logger.info('Proxy: "%s"', proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()
        return 0
