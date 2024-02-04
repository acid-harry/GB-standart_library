#Модифицированный код с улучшением логирования и запуском из командной строки

import logging
import argparse

class InvalidNameError(Exception):
    pass

class InvalidAgeError(Exception):
    pass

class InvalidIdError(Exception):
    pass

# Настройка логирования
logging.basicConfig(filename='person_and_employee_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Person:
    def __init__(self, last_name, first_name, middle_name, age):
        try:
            self.set_last_name(last_name)
            self.set_first_name(first_name)
            self.set_middle_name(middle_name)
            self.set_age(age)
        except (InvalidNameError, InvalidAgeError) as e:
            logger.error(f"Error while creating Person: {e}")
            raise

    def set_last_name(self, last_name):
        if not last_name or not isinstance(last_name, str):
            raise InvalidNameError("Invalid last name")
        self.last_name = last_name

    def set_first_name(self, first_name):
        if not first_name or not isinstance(first_name, str):
            raise InvalidNameError("Invalid first name")
        self.first_name = first_name

    def set_middle_name(self, middle_name):
        if not middle_name or not isinstance(middle_name, str):
            raise InvalidNameError("Invalid middle name")
        self.middle_name = middle_name

    def set_age(self, age):
        if not isinstance(age, int) or age <= 0:
            raise InvalidAgeError("Invalid age")
        self.age = age

    def birthday(self):
        self.age += 1

class Employee(Person):
    def __init__(self, last_name, first_name, middle_name, age, employee_id):
        try:
            super().__init__(last_name, first_name, middle_name, age)
            self.set_employee_id(employee_id)
        except InvalidIdError as e:
            logger.error(f"Error while creating Employee: {e}")
            raise

    def set_employee_id(self, employee_id):
        if not isinstance(employee_id, int) or not (100000 <= employee_id <= 999999):
            raise InvalidIdError("Invalid employee ID")
        self.employee_id = employee_id

    def get_level(self):
        return sum(int(digit) for digit in str(self.employee_id)) % 7

def main():
    parser = argparse.ArgumentParser(description="Create Person and Employee objects with given parameters.")
    parser.add_argument("--last_name", required=True, help="Last name of the person.")
    parser.add_argument("--first_name", required=True, help="First name of the person.")
    parser.add_argument("--middle_name", required=True, help="Middle name of the person.")
    parser.add_argument("--age", type=int, required=True, help="Age of the person.")
    parser.add_argument("--employee_id", type=int, help="Employee ID (for Employee objects).")

    args = parser.parse_args()

    try:
        if args.employee_id:
            employee = Employee(args.last_name, args.first_name, args.middle_name, args.age, args.employee_id)
            logger.info(f"Employee created: {employee.first_name} {employee.last_name}, ID: {employee.employee_id}, Level: {employee.get_level()}")
        else:
            person = Person(args.last_name, args.first_name, args.middle_name, args.age)
            logger.info(f"Person created: {person.first_name} {person.last_name}, Age: {person.age}")

    except (InvalidNameError, InvalidAgeError, InvalidIdError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
