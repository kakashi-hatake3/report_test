import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
import sys
import main


class TestMain:

    def test_parse_arguments_valid(self):
        """Тест корректного парсинга аргументов"""
        test_args = [
            "--files",
            "file1.csv",
            "file2.csv",
            "--report",
            "student-performance",
        ]

        with patch.object(sys, "argv", ["main.py"] + test_args):
            args = main.parse_arguments()

            assert args.files == ["file1.csv", "file2.csv"]
            assert args.report == "student-performance"

    def test_parse_arguments_missing_files(self):
        """Тест отсутствующего параметра --files"""
        test_args = ["--report", "student-performance"]

        with patch.object(sys, "argv", ["main.py"] + test_args):
            with pytest.raises(SystemExit):
                main.parse_arguments()

    def test_parse_arguments_missing_report(self):
        """Тест отсутствующего параметра --report"""
        test_args = ["--files", "file1.csv"]

        with patch.object(sys, "argv", ["main.py"] + test_args):
            with pytest.raises(SystemExit):
                main.parse_arguments()

    def test_parse_arguments_invalid_report(self):
        """Тест некорректного типа отчета"""
        test_args = ["--files", "file1.csv", "--report", "invalid-report"]

        with patch.object(sys, "argv", ["main.py"] + test_args):
            with pytest.raises(SystemExit):
                main.parse_arguments()

    @patch("main.StudentPerformanceReport")
    @patch("main.CSVReader")
    @patch("main.parse_arguments")
    def test_main_successful_execution(
        self, mock_parse_args, mock_csv_reader, mock_report
    ):
        """Тест успешного выполнения программы"""
        mock_args = MagicMock()
        mock_args.files = ["file1.csv"]
        mock_args.report = "student-performance"
        mock_parse_args.return_value = mock_args

        mock_reader_instance = MagicMock()
        mock_reader_instance.read_file.return_value = [
            {
                "student_name": "Тест",
                "subject": "Математика",
                "teacher_name": "Учитель",
                "date": "2023-10-01",
                "grade": 5.0,
            }
        ]
        mock_csv_reader.return_value = mock_reader_instance

        mock_report_instance = MagicMock()
        mock_report.return_value = mock_report_instance

        main.main()

        mock_reader_instance.read_file.assert_called_once_with("file1.csv")
        mock_report_instance.generate_report.assert_called_once()

    @patch("main.CSVReader")
    @patch("main.parse_arguments")
    def test_main_file_not_found(self, mock_parse_args, mock_csv_reader):
        """Тест обработки ошибки несуществующего файла"""
        mock_args = MagicMock()
        mock_args.files = ["nonexistent.csv"]
        mock_args.report = "student-performance"
        mock_parse_args.return_value = mock_args

        mock_reader_instance = MagicMock()
        mock_reader_instance.read_file.side_effect = FileNotFoundError("Файл не найден")
        mock_csv_reader.return_value = mock_reader_instance

        with pytest.raises(SystemExit) as exc_info:
            main.main()

        assert exc_info.value.code == 1

    @patch("main.CSVReader")
    @patch("main.parse_arguments")
    def test_main_multiple_files(self, mock_parse_args, mock_csv_reader):
        """Тест обработки нескольких файлов"""
        mock_args = MagicMock()
        mock_args.files = ["file1.csv", "file2.csv"]
        mock_args.report = "student-performance"
        mock_parse_args.return_value = mock_args

        mock_reader_instance = MagicMock()
        mock_reader_instance.read_file.side_effect = [
            [
                {
                    "student_name": "Студент1",
                    "subject": "Математика",
                    "teacher_name": "Учитель1",
                    "date": "2023-10-01",
                    "grade": 5.0,
                }
            ],
            [
                {
                    "student_name": "Студент2",
                    "subject": "Физика",
                    "teacher_name": "Учитель2",
                    "date": "2023-10-02",
                    "grade": 4.0,
                }
            ],
        ]
        mock_csv_reader.return_value = mock_reader_instance

        with patch("main.StudentPerformanceReport") as mock_report:
            mock_report_instance = MagicMock()
            mock_report.return_value = mock_report_instance

            main.main()

            assert mock_reader_instance.read_file.call_count == 2
            mock_reader_instance.read_file.assert_any_call("file1.csv")
            mock_reader_instance.read_file.assert_any_call("file2.csv")

            mock_report_instance.generate_report.assert_called_once()
            args, kwargs = mock_report_instance.generate_report.call_args
            assert len(args[0]) == 2

    @patch("main.parse_arguments")
    def test_main_keyboard_interrupt(self, mock_parse_args):
        """Тест обработки прерывания программы пользователем"""
        mock_parse_args.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit) as exc_info:
            main.main()

        assert exc_info.value.code == 1

    @patch("main.CSVReader")
    @patch("main.parse_arguments")
    def test_main_empty_records(self, mock_parse_args, mock_csv_reader):
        """Тест обработки файлов без данных"""
        mock_args = MagicMock()
        mock_args.files = ["empty.csv"]
        mock_args.report = "student-performance"
        mock_parse_args.return_value = mock_args

        mock_reader_instance = MagicMock()
        mock_reader_instance.read_file.return_value = []
        mock_csv_reader.return_value = mock_reader_instance

        with pytest.raises(SystemExit) as exc_info:
            main.main()

        assert exc_info.value.code == 1
