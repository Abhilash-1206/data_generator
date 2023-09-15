# importing all the required packages

import pandas as pd
import random
import string
from datetime import datetime, timedelta
from faker import Faker
import json
import names

# Creating object to the Faker class
fake = Faker()


# Generate data for different data types based on the is_null and is_empty parameters
def is_null_and_is_empty_func(col_type, column, num_rows, data, is_yes_no):
    if col_type == "number" or col_type == 'int':
        data[column] = [random.choice(random.randint(1, 10000), "", "NULL") for _ in range(num_rows)]

    elif col_type == "text" or col_type == 'varchar':
        data[column] = [random.choice(["NULL", "", fake.word()]) for _ in
                        range(num_rows)]

    elif col_type == "double":
        data[column] = [random.choice(round(random.uniform(30000, 100000), 2), "", "NULL") for _ in range(num_rows)]

    elif col_type == "boolean" or col_type == "bool":
        if is_yes_no:
            data[column] = [random.choice(["yes", "no", "NULL", ""]) for _ in range(num_rows)]
        else:
            data[column] = [random.choice([True, False, "NULL", ""]) for _ in range(num_rows)]


# Generate data for different data types based on the is_null parameter
def is_null_func(col_type, column, num_rows, data, is_yes_no):
    if col_type == "number" or col_type == 'int':
        data[column] = [random.choice(random.randint(1, 10000), "NULL") for _ in range(num_rows)]

    elif col_type == "text" or col_type == 'varchar':
        data[column] = [random.choice(["NULL", fake.word()]) for _ in
                        range(num_rows)]

    elif col_type == "double":
        data[column] = [random.choice(round(random.uniform(30000, 100000), 2), "NULL") for _ in range(num_rows)]

    elif col_type == "boolean" or col_type == "bool":
        if is_yes_no:
            data[column] = [random.choice(["yes", "no", "NULL"]) for _ in range(num_rows)]
        else:
            data[column] = [random.choice([True, False, "NULL"]) for _ in range(num_rows)]


# Generate data for different data types based on the is_empty parameter
def is_empty_func(col_type, column, num_rows, data, is_yes_no):
    if col_type == "number" or col_type == 'int':
        data[column] = [random.choice(random.randint(1, 10000), "") for _ in range(num_rows)]

    elif col_type == "text" or col_type == 'varchar':
        data[column] = [random.choice(["", fake.word()]) for _ in
                        range(num_rows)]

    elif col_type == "double":
        data[column] = [random.choice(round(random.uniform(30000, 100000), 2), "") for _ in range(num_rows)]

    elif col_type == "boolean" or col_type == "bool":
        if is_yes_no:
            data[column] = [random.choice(["yes", "no", ""]) for _ in range(num_rows)]
        else:
            data[column] = [random.choice([True, False, ""]) for _ in range(num_rows)]


# Generates random data for all the data types
def generate_random_data(schema, num_rows):
    data = {}
    for column, col_type in schema.items():
        column_type = col_type['type'].lower()
        column = column.lower()
        is_unique = str(col_type.get("is_unique")).lower()
        is_null = str(col_type.get("is_null")).lower()
        is_empty = str(col_type.get("is_empty")).lower()
        min_value = col_type.get("minvalue")
        max_value = col_type.get("maxvalue")
        is_yes_no = col_type.get("is_yes_no")   # parameter that decides whether to use True or yes for boolean values

        if column_type == 'number' or column_type == 'int':

            if is_unique == 'yes' and is_null == 'no':
                primary_key = list(range(1, num_rows + 1))
                random.shuffle(primary_key)
                data[column] = primary_key

            elif min_value and max_value:
                data[column] = [random.randint(min_value, max_value) for _ in range(num_rows)]

            elif is_null == "yes" and is_empty == "yes":
                is_null_and_is_empty_func(column_type, column, num_rows, data, is_yes_no)

            elif is_null == "yes":
                is_null_func(column_type, column, num_rows, data, is_yes_no)

            elif is_empty == "yes":
                is_empty_func(column_type, column, num_rows, data, is_yes_no)

            else:
                data[column] = [random.randint(1, 10000) for _ in range(num_rows)]

        elif column_type == 'date':
            start_date = datetime(1950, 1, 1)
            end_date = datetime.now()
            random_dates = [start_date + timedelta(days=random.randint(1, (end_date - start_date).days)) for _ in
                            range(num_rows)]
            data[column] = [dt.strftime('%Y-%m-%d') for dt in random_dates]

        elif column_type == 'datetime':

            if column == 'start_time':
                start_date = datetime(1950, 1, 1)
                end_date = datetime(2010, 1, 1)
                random_datetime = [start_date + timedelta(days=random.randint(1, (end_date - start_date).days),
                                                          seconds=random.randint(0, 86400)) for _ in range(num_rows)]
                data[column] = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in random_datetime]

            elif column == 'end_time':
                start_dates = pd.to_datetime(data['start_time'], format='%Y-%m-%d %H:%M:%S')
                end_dates = start_dates + pd.to_timedelta([random.randint(1, 4745) for _ in range(num_rows)], unit='D')
                data[column] = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in end_dates]

            else:
                start_date = datetime(1950, 1, 1)
                end_date = datetime.now()
                random_datetime = [start_date + timedelta(days=random.randint(1, (end_date - start_date).days),
                                                          seconds=random.randint(0, 86400)) for _ in range(num_rows)]
                data[column] = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in random_datetime]

        elif column_type == 'text' or column_type == 'varchar':

            if is_null == "yes" and is_empty == "yes":
                is_null_and_is_empty_func(column_type, column, num_rows, data, is_yes_no)

            elif is_null == "yes":
                is_null_func(column_type, column, num_rows, data, is_yes_no)

            elif is_empty == "yes":
                is_empty_func(column_type, column, num_rows, data, is_yes_no)

            elif column == 'gender':
                data[column] = [random.choice(['Male', 'Female']) for _ in range(num_rows)]

            elif column == 'address':
                data[column] = [fake.address().replace("\n", ",") for _ in range(num_rows)]

            elif column == 'name':
                data[column] = [(names.get_full_name()) for _ in range(num_rows)]

            else:
                data[column] = [random.choice(string.ascii_uppercase) + random.choice(string.ascii_lowercase) + str(
                    random.randint(100, 999)) for _ in
                                range(num_rows)]

        elif column_type == 'double':

            if is_null == "yes" and is_empty == 'yes':
                is_null_and_is_empty_func(column_type, column, num_rows, data, is_yes_no)

            elif is_null == "yes":
                is_null_func(column_type, column, num_rows, data, is_yes_no)

            elif is_empty == 'yes':
                is_empty_func(column_type, column, num_rows, data, is_yes_no)

            else:
                data[column] = [round(random.uniform(30000, 100000), 2) for _ in range(num_rows)]

        elif column_type == 'json':
            json_data = [{"key1": random.randint(1, 100), "key2": random.choice(["ASDFGH", "BNMZXCV", "CVBNMQWERTY"])}
                         for _ in
                         range(num_rows)]
            data[column] = [json.dumps(item) for item in json_data]

        elif column_type == 'boolean':

            if is_null == "yes" and is_empty == 'yes':
                is_null_and_is_empty_func(column_type, column, num_rows, data, is_yes_no)

            elif is_null == "yes":
                is_null_func(column_type, column, num_rows, data, is_yes_no)

            elif is_empty == 'yes':
                is_empty_func(column_type, column, num_rows, data, is_yes_no)

            else:
                if is_yes_no:
                    data[column] = [random.choice(["yes", "no"]) for _ in range(num_rows)]
                else:
                    data[column] = [random.choice([True, False]) for _ in range(num_rows)]

        elif column_type == 'list':
            data[column] = [[fake.phone_number(), names.get_first_name()] for _ in range(num_rows)]

    return data
