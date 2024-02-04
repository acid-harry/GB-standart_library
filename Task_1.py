#Модифицированный код с улучшением логирования и запуском из командной строки

import os
import json
import csv
import pickle
import logging
import argparse

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dir_size(directory):
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
    except Exception as e:
        logger.error(f"Error while getting directory size: {e}")
    return total_size

def traverse_directory(directory):
    results = []

    try:
        for root, dirs, files in os.walk(directory):
            for name in files:
                path = os.path.join(root, name)
                size = os.path.getsize(path)
                results.append({'Path': path, 'Type': 'File', 'Size': size})

            for name in dirs:
                path = os.path.join(root, name)
                size = get_dir_size(path)
                results.append({'Path': path, 'Type': 'Directory', 'Size': size})
    except Exception as e:
        logger.error(f"Error while traversing directory: {e}")

    return results

def save_results_to_json(results, output_file):
    try:
        with open(output_file, 'w') as json_file:
            json.dump(results, json_file, indent=2)
        logger.info(f"Results saved to JSON file: {output_file}")
    except Exception as e:
        logger.error(f"Error while saving results to JSON: {e}")

def save_results_to_csv(results, output_file):
    try:
        with open(output_file, 'w', newline='') as csv_file:
            fieldnames = ['Path', 'Type', 'Size']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        logger.info(f"Results saved to CSV file: {output_file}")
    except Exception as e:
        logger.error(f"Error while saving results to CSV: {e}")

def save_results_to_pickle(results, output_file):
    try:
        with open(output_file, 'wb') as pickle_file:
            pickle.dump(results, pickle_file)
        logger.info(f"Results saved to Pickle file: {output_file}")
    except Exception as e:
        logger.error(f"Error while saving results to Pickle: {e}")

def main():
    parser = argparse.ArgumentParser(description="Traverse directory and save results to JSON, CSV, and Pickle.")
    parser.add_argument("directory", help="The directory to traverse.")
    parser.add_argument("--json", help="JSON output file name.", default="results.json")
    parser.add_argument("--csv", help="CSV output file name.", default="results.csv")
    parser.add_argument("--pickle", help="Pickle output file name.", default="results.pkl")

    args = parser.parse_args()

    directory_to_traverse = args.directory
    json_output_file = args.json
    csv_output_file = args.csv
    pickle_output_file = args.pickle

    results = traverse_directory(directory_to_traverse)

    save_results_to_json(results, json_output_file)
    save_results_to_csv(results, csv_output_file)
    save_results_to_pickle(results, pickle_output_file)

if __name__ == "__main__":
    main()
