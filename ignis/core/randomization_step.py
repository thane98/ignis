from abc import ABC, abstractmethod


class RandomizationStep(ABC):
    @abstractmethod
    def should_run(self, user_config) -> bool:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self, gd, user_config, dependencies):
        pass
