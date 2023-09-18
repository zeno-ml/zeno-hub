"""Amplitude handler for tracking after env has been set up with a singleton object."""
import os

from amplitude import Amplitude, BaseEvent


class AmplitudeHandler:
    """Class to handle amplitude events.

    Attributes:
        _client (Amplitude | None): amplitude client singleton object.
    """

    _client = None

    def __new__(cls):
        """Create a new amplitude handler if one doesn't exist."""
        if "AMPLITUDE_API_KEY" in os.environ:
            if cls._client is None:
                cls._client = Amplitude(os.environ["AMPLITUDE_API_KEY"])
        return cls._client

    def track(self, event: BaseEvent):
        """Track an amplitude event.

        Args:
            event (BaseEvent): the event to track.
        """
        if self._client is not None:
            self._client.track(event)
