from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PMTask:
    title: str
    description: str
    estimate_days: float
    labels: list[str]


class PMAdapter(ABC):
    @abstractmethod
    def push_tasks(self, project_key: str, tasks: list[PMTask]) -> list[str]:
        """Returns list of created issue IDs."""
        pass
