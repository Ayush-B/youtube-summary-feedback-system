from abc import ABC, abstractmethod
from typing import Any

class BaseAnalyzer(ABC):
    """
    Abstract base class for all analyzers.
    Ensures consistency in the analyze() method implementation.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key

    @abstractmethod
    def analyze(self, data: Any) -> Any:
        """Abstract method to be implemented by all subclasses."""
        pass
