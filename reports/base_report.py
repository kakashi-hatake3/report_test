from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseReport(ABC):
    """Абстрактный базовый класс для отчетов"""

    @abstractmethod
    def generate_report(self, records: List[Dict[str, Any]]) -> None:
        """
        Генерирует отчет на основе переданных записей

        Args:
            records: Список записей с данными
        """
        pass
