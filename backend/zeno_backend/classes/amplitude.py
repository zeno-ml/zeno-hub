"""Amplitude handler for tracking after env has been set up with a singleton object."""
import os

from amplitude import Amplitude, BaseEvent


class AmplitudeHandler:
    """Class to handle amplitude events.

    Attributes:
        _client (Amplitude | None): amplitude client object.
        _instance (AmplitudeHandler | None): amplitude handler singleton object.
    """

    _client = None
    _instance = None

    def __new__(cls):
        """Create a new amplitude handler if one doesn't exist."""
        if cls._instance is None:
            cls._instance = super(AmplitudeHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the amplitude singleton."""
        if not hasattr(self, "initialized"):
            if "AMPLITUDE_API_KEY" in os.environ:
                self._client = Amplitude(os.environ["AMPLITUDE_API_KEY"])
            self.initialized = True

    def track(self, event: BaseEvent):
        """Track an amplitude event.

        Args:
            event (BaseEvent): the event to track.
        """
        if self._client is not None:
            self._client.track(event)
