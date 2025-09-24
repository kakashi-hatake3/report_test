import csv
from typing import List, Dict, Any


class CSVReader:
    """Класс для чтения CSV файлов с данными о студентах"""

    REQUIRED_COLUMNS = {"student_name", "subject", "teacher_name", "date", "grade"}

    def read_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Читает CSV файл и возвращает список записей

        Args:
            file_path: Путь к CSV файлу

        Returns:
            Список словарей с данными студентов

        Raises:
            FileNotFoundError: Если файл не найден
            ValueError: Если формат файла некорректен
        """
        records = []

        try:
            with open(file_path, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                if not self.REQUIRED_COLUMNS.issubset(set(reader.fieldnames or [])):
                    missing_cols = self.REQUIRED_COLUMNS - set(reader.fieldnames or [])
                    raise ValueError(f"Отсутствуют необходимые колонки: {missing_cols}")

                for row_num, row in enumerate(
                    reader, start=2
                ):  # start=2 учитывает заголовок
                    try:
                        processed_row = self._process_row(row, row_num)
                        records.append(processed_row)
                    except ValueError as e:
                        raise ValueError(f"Ошибка в строке {row_num}: {e}")

        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {file_path} не найден")
        except UnicodeDecodeError:
            raise ValueError(f"Ошибка кодировки файла {file_path}")

        return records

    def _process_row(self, row: Dict[str, str], row_num: int) -> Dict[str, Any]:
        """
        Обрабатывает строку CSV файла

        Args:
            row: Словарь с данными строки
            row_num: Номер строки для отображения ошибок

        Returns:
            Обработанная строка с правильными типами данных
        """
        try:
            grade = float(row["grade"].strip())
            if not (1 <= grade <= 5):
                raise ValueError(f"Оценка должна быть от 1 до 5, получено: {grade}")
        except (ValueError, TypeError):
            raise ValueError(f"Некорректная оценка: {row['grade']}")

        required_fields = ["student_name", "subject", "teacher_name", "date"]
        for field in required_fields:
            if not row[field].strip():
                raise ValueError(f"Поле {field} не может быть пустым")

        return {
            "student_name": row["student_name"].strip(),
            "subject": row["subject"].strip(),
            "teacher_name": row["teacher_name"].strip(),
            "date": row["date"].strip(),
            "grade": grade,
        }
