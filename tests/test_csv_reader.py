import pytest
import tempfile
import os
from data.csv_reader import CSVReader


class TestCSVReader:

    def setup_method(self):
        """Настройка для каждого теста"""
        self.csv_reader = CSVReader()

    def test_read_valid_file(self):
        """Тест чтения корректного CSV файла"""
        csv_content = """student_name,subject,teacher_name,date,grade
Иванов Иван,Математика,Петров Петр,2023-10-01,5
Сидоров Сидор,Физика,Иванова Анна,2023-10-02,4"""

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        ) as f:
            f.write(csv_content)
            f.flush()
            temp_path = f.name

        try:
            records = self.csv_reader.read_file(temp_path)

            assert len(records) == 2
            assert records[0]["student_name"] == "Иванов Иван"
            assert records[0]["grade"] == 5.0
            assert records[1]["student_name"] == "Сидоров Сидор"
            assert records[1]["grade"] == 4.0

        finally:
            os.unlink(temp_path)

    def test_read_file_with_decimal_grades(self):
        """Тест чтения файла с десятичными оценками"""
        csv_content = """student_name,subject,teacher_name,date,grade
Иванов Иван,Математика,Петров Петр,2023-10-01,4.5
Сидоров Сидор,Физика,Иванова Анна,2023-10-02,3.7"""

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        ) as f:
            f.write(csv_content)
            f.flush()
            temp_path = f.name

        try:
            records = self.csv_reader.read_file(temp_path)

            assert records[0]["grade"] == 4.5
            assert records[1]["grade"] == 3.7

        finally:
            os.unlink(temp_path)

    def test_read_nonexistent_file(self):
        """Тест чтения несуществующего файла"""
        with pytest.raises(FileNotFoundError):
            self.csv_reader.read_file("nonexistent_file.csv")

    def test_invalid_grade_value(self):
        """Тест некорректного значения оценки"""
        csv_content = """student_name,subject,teacher_name,date,grade
Иванов Иван,Математика,Петров Петр,2023-10-01,abc"""

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        ) as f:
            f.write(csv_content)
            f.flush()
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Ошибка в строке 2"):
                self.csv_reader.read_file(temp_path)

        finally:
            os.unlink(temp_path)

    def test_grade_out_of_range(self):
        """Тест оценки вне диапазона 1-5"""
        csv_content = """student_name,subject,teacher_name,date,grade
Иванов Иван,Математика,Петров Петр,2023-10-01,6"""

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        ) as f:
            f.write(csv_content)
            f.flush()
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Ошибка в строке 2"):
                self.csv_reader.read_file(temp_path)

        finally:
            os.unlink(temp_path)

    def test_missing_columns(self):
        """Тест отсутствия необходимых колонок"""
        csv_content = """student_name,subject,date,grade
Иванов Иван,Математика,2023-10-01,5"""

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        ) as f:
            f.write(csv_content)
            f.flush()
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Отсутствуют необходимые колонки"):
                self.csv_reader.read_file(temp_path)

        finally:
            os.unlink(temp_path)

    def test_empty_required_field(self):
        """Тест пустого обязательного поля"""
        csv_content = """student_name,subject,teacher_name,date,grade
,Математика,Петров Петр,2023-10-01,5"""

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        ) as f:
            f.write(csv_content)
            f.flush()
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Ошибка в строке 2"):
                self.csv_reader.read_file(temp_path)

        finally:
            os.unlink(temp_path)

    def test_whitespace_handling(self):
        """Тест обработки пробелов в данных"""
        csv_content = """student_name,subject,teacher_name,date,grade
  Иванов Иван  ,  Математика  ,  Петров Петр  ,2023-10-01,  5  """

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        ) as f:
            f.write(csv_content)
            f.flush()
            temp_path = f.name

        try:
            records = self.csv_reader.read_file(temp_path)

            assert records[0]["student_name"] == "Иванов Иван"
            assert records[0]["subject"] == "Математика"
            assert records[0]["teacher_name"] == "Петров Петр"
            assert records[0]["grade"] == 5.0

        finally:
            os.unlink(temp_path)
