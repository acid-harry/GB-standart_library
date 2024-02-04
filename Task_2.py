#Модифицировано логирование и добавлен запуск из строки.

import csv
import json
import random
import logging
import argparse

# Настройка логирования
logging.basicConfig(filename='generate_and_find_roots_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Генерация CSV-файла
def generate_csv_file(file_name, rows):
    try:
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = ['a', 'b', 'c']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for _ in range(rows):
                a, b, c = random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)
                writer.writerow({'a': a, 'b': b, 'c': c})

        logger.info(f"CSV file '{file_name}' generated successfully with {rows} rows.")
    except Exception as e:
        logger.error(f"Error while generating CSV file: {e}")

# Нахождение корней квадратного уравнения
def find_roots(a, b, c):
    try:
        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            return None
        elif discriminant == 0:
            root = -b / (2*a)
            return root
        else:
            root1 = (-b + discriminant**0.5) / (2*a)
            root2 = (-b - discriminant**0.5) / (2*a)
            return root1, root2
    except Exception as e:
        logger.error(f"Error while finding roots: {e}")

# Декоратор для сохранения в JSON
def save_to_json(func):
    def wrapper(*args, **kwargs):
        input_file = args[0]
        results = []

        try:
            with open(input_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    a, b, c = int(row['a']), int(row['b']), int(row['c'])
                    roots = func(a, b, c)
                    results.append({'parameters': [a, b, c], 'result': roots})

            with open('results.json', 'w') as json_file:
                json.dump(results, json_file, indent=2)
            logger.info("Results saved to JSON file 'results.json'.")
        except Exception as e:
            logger.error(f"Error while saving results to JSON: {e}")

    return wrapper

# Применение декоратора к функции find_roots
@save_to_json
def find_roots(a, b, c):
    try:
        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            return None
        elif discriminant == 0:
            root = -b / (2*a)
            return root
        else:
            root1 = (-b + discriminant**0.5) / (2*a)
            root2 = (-b - discriminant**0.5) / (2*a)
            return root1, root2
    except Exception as e:
        logger.error(f"Error while finding roots: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate CSV file and find roots of quadratic equations.")
    parser.add_argument("rows", type=int, help="Number of rows in the CSV file.")
    parser.add_argument("--csv", help="CSV output file name.", default="input_data.csv")

    args = parser.parse_args()

    rows = args.rows
    csv_output_file = args.csv

    generate_csv_file(csv_output_file, rows)
    find_roots(csv_output_file)

    with open("results.json", 'r') as f:
        data = json.load(f)

    if 100 <= len(data) <= 1000:
        print(True)
    else:
        print(f"Количество строк в файле не находится в диапазоне от 100 до 1000.")

    print(len(data) == rows)

if __name__ == "__main__":
    main()
