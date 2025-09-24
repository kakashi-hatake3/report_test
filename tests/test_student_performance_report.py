import pytest
from io import StringIO
import sys
from reports.student_performance_report import StudentPerformanceReport


class TestStudentPerformanceReport:

    def setup_method(self):
        """Настройка для каждого теста"""
        self.report = StudentPerformanceReport()

    def test_generate_report_single_student(self, capsys):
        """Тест генерации отчета для одного студента"""
        records = [
            {
                "student_name": "Иванов Иван",
                "subject": "Математика",
                "teacher_name": "Петров",
                "date": "2023-10-01",
                "grade": 5.0,
            },
            {
                "student_name": "Иванов Иван",
                "subject": "Физика",
                "teacher_name": "Сидоров",
                "date": "2023-10-02",
                "grade": 4.0,
            },
        ]

        self.report.generate_report(records)

        captured = capsys.readouterr()
        output = captured.out

        assert "Иванов Иван" in output
        assert "4.5" in output

    def test_generate_report_multiple_students(self, capsys):
        """Тест генерации отчета для нескольких студентов"""
        records = [
            {
                "student_name": "Иванов Иван",
                "subject": "Математика",
                "teacher_name": "Петров",
                "date": "2023-10-01",
                "grade": 5.0,
            },
            {
                "student_name": "Сидоров Сидор",
                "subject": "Физика",
                "teacher_name": "Иванов",
                "date": "2023-10-02",
                "grade": 3.0,
            },
            {
                "student_name": "Иванов Иван",
                "subject": "Химия",
                "teacher_name": "Петрова",
                "date": "2023-10-03",
                "grade": 4.0,
            },
        ]

        self.report.generate_report(records)

        captured = capsys.readouterr()
        output = captured.out

        assert "Иванов Иван" in output
        assert "Сидоров Сидор" in output
        assert "4.5" in output
        assert "3.0" in output

    def test_generate_report_sorting(self, capsys):
        """Тест сортировки студентов по убыванию средней оценки"""
        records = [
            {
                "student_name": "Плохой Студент",
                "subject": "Математика",
                "teacher_name": "Петров",
                "date": "2023-10-01",
                "grade": 2.0,
            },
            {
                "student_name": "Отличник",
                "subject": "Физика",
                "teacher_name": "Иванов",
                "date": "2023-10-02",
                "grade": 5.0,
            },
            {
                "student_name": "Хорошист",
                "subject": "Химия",
                "teacher_name": "Петрова",
                "date": "2023-10-03",
                "grade": 4.0,
            },
        ]

        self.report.generate_report(records)

        captured = capsys.readouterr()
        output = captured.out
        lines = output.split("\n")

        student_lines = [
            line
            for line in lines
            if any(name in line for name in ["Отличник", "Хорошист", "Плохой Студент"])
        ]

        assert len(student_lines) == 3
        assert "Отличник" in student_lines[0]
        assert "Хорошист" in student_lines[1]
        assert "Плохой Студент" in student_lines[2]

    def test_generate_report_empty_records(self, capsys):
        """Тест генерации отчета для пустого списка записей"""
        records = []

        self.report.generate_report(records)

        captured = capsys.readouterr()
        output = captured.out

        assert "student_name" in output
        assert "grade" in output

    def test_generate_report_decimal_rounding(self, capsys):
        """Тест округления десятичных значений в отчете"""
        records = [
            {
                "student_name": "Студент",
                "subject": "Математика",
                "teacher_name": "Петров",
                "date": "2023-10-01",
                "grade": 4.0,
            },
            {
                "student_name": "Студент",
                "subject": "Физика",
                "teacher_name": "Иванов",
                "date": "2023-10-02",
                "grade": 5.0,
            },
            {
                "student_name": "Студент",
                "subject": "Химия",
                "teacher_name": "Сидоров",
                "date": "2023-10-03",
                "grade": 4.0,
            },
        ]

        self.report.generate_report(records)

        captured = capsys.readouterr()
        output = captured.out

        assert "4.3" in output

    def test_generate_report_same_grades(self, capsys):
        """Тест для студентов с одинаковыми средними оценками"""
        records = [
            {
                "student_name": "Студент А",
                "subject": "Математика",
                "teacher_name": "Петров",
                "date": "2023-10-01",
                "grade": 4.0,
            },
            {
                "student_name": "Студент Б",
                "subject": "Физика",
                "teacher_name": "Иванов",
                "date": "2023-10-02",
                "grade": 4.0,
            },
        ]

        self.report.generate_report(records)

        captured = capsys.readouterr()
        output = captured.out

        assert "Студент А" in output
        assert "Студент Б" in output
        assert output.count("4.0") == 2
