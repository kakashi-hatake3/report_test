import argparse
import sys
from typing import List
from reports.student_performance_report import StudentPerformanceReport
from data.csv_reader import CSVReader


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Анализ успеваемости студентов")
    parser.add_argument(
        "--files",
        required=True,
        nargs="+",
        help="Пути к CSV файлам с данными о студентах",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=["student-performance"],
        help="Тип отчета для формирования",
    )
    return parser.parse_args()


def main():
    """Основная функция программы"""
    try:
        args = parse_arguments()

        csv_reader = CSVReader()
        all_records = []

        for file_path in args.files:
            try:
                records = csv_reader.read_file(file_path)
                all_records.extend(records)
            except FileNotFoundError:
                print(f"Ошибка: Файл {file_path} не найден", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Ошибка при чтении файла {file_path}: {e}", file=sys.stderr)
                sys.exit(1)

        if not all_records:
            print("Ошибка: Не найдено данных для обработки", file=sys.stderr)
            sys.exit(1)

        if args.report == "student-performance":
            report = StudentPerformanceReport()
            report.generate_report(all_records)

    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
