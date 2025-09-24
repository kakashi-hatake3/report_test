from typing import List, Dict, Any
from collections import defaultdict
from tabulate import tabulate
from .base_report import BaseReport


class StudentPerformanceReport(BaseReport):
    """Класс для формирования отчета по успеваемости студентов"""

    def generate_report(self, records: List[Dict[str, Any]]) -> None:
        """
        Генерирует отчет по успеваемости студентов

        Args:
            records: Список записей с данными студентов
        """
        student_grades = defaultdict(list)

        for record in records:
            student_name = record["student_name"]
            grade = record["grade"]
            student_grades[student_name].append(grade)

        student_averages = []
        for student_name, grades in student_grades.items():
            average_grade = sum(grades) / len(grades)
            student_averages.append(
                {"student_name": student_name, "grade": round(average_grade, 1)}
            )

        student_averages.sort(key=lambda x: x["grade"], reverse=True)

        table_data = []
        for i, student_data in enumerate(student_averages, 1):
            table_data.append([i, student_data["student_name"], student_data["grade"]])

        headers = ["", "student_name", "grade"]
        table = tabulate(table_data, headers=headers, tablefmt="grid", floatfmt=".1f")
        print(table)
