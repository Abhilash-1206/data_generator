import pandas as pd
import random
import string
from datetime import datetime, timedelta, date
from faker import Faker
import json
import names
from random_word import RandomWords


fake = Faker()


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


def generate_random_data(schema, num_rows):
    data = {}
    r = RandomWords()
    for column, col_type in schema.items():
        column_type = col_type['type'].lower()
        column = column.lower()
        Is_Unique = str(col_type.get("is_unique")).lower()
        IS_Null = str(col_type.get("is_null")).lower()
        Is_Empty = str(col_type.get("is_empty")).lower()
        Min_Value = col_type.get("minvalue")
        Max_Value = col_type.get("maxvalue")
        is_yes_no = col_type.get("is_yes_no")

        if column_type == 'date':
            start_date = datetime(1950, 1, 1)
            end_date = datetime.now()
            random_dates = [start_date + timedelta(days=random.randint(1, (end_date - start_date).days)) for _ in
                            range(num_rows)]
            data[column] = [dt.strftime('%Y-%m-%d') for dt in random_dates]

        elif column_type == 'datetime':

            if column == 'segstart_utc':
                start_date = datetime(1950, 1, 1)
                end_date = datetime(2010, 1, 1)
                random_datetime = [start_date + timedelta(days=random.randint(1, (end_date - start_date).days),
                                                          seconds=random.randint(0, 86400)) for _ in range(num_rows)]
                data[column] = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in random_datetime]

            elif column == 'segstop_utc':
                start_dates = pd.to_datetime(data['segstart_utc'], format='%Y-%m-%d %H:%M:%S')
                end_dates = start_dates + pd.to_timedelta([random.randint(1, 4745) for _ in range(num_rows)], unit='D')
                data[column] = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in end_dates]

            else:
                start_date = datetime(1950, 1, 1)
                end_date = datetime.now()
                random_datetime = [start_date + timedelta(days=random.randint(1, (end_date - start_date).days),
                                                          seconds=random.randint(0, 86400)) for _ in range(num_rows)]
                data[column] = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in random_datetime]

        elif column_type == 'number' or column_type == 'int':

            if Is_Unique == 'yes' and IS_Null == 'no':
                primary_key = list(range(1, num_rows + 1))
                random.shuffle(primary_key)
                data[column] = primary_key

            elif Min_Value and Max_Value:
                data[column] = [random.randint(Min_Value, Max_Value) for _ in range(num_rows)]

            elif IS_Null == "yes" and Is_Empty == "yes":
                is_null_and_is_empty_func(column_type, column, num_rows, data, is_yes_no)

            elif IS_Null == "yes":
                is_null_func(column_type, column, num_rows, data, is_yes_no)

            elif Is_Empty == "yes":
                is_empty_func(column_type, column, num_rows, data, is_yes_no)

            else:
                data[column] = [random.randint(1, 10000) for _ in range(num_rows)]

        elif column_type == 'text' or column_type == 'varchar':

            if IS_Null == "yes" and Is_Empty == "yes":
                is_null_and_is_empty_func(column_type, column, num_rows, data, is_yes_no)

            elif IS_Null == "yes":
                is_null_func(column_type, column, num_rows, data, is_yes_no)

            elif Is_Empty == "yes":
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

            if IS_Null == "yes" and Is_Empty == 'yes':
                is_null_and_is_empty_func(column_type, column, num_rows, data, is_yes_no)

            elif IS_Null == "yes":
                is_null_func(column_type, column, num_rows, data, is_yes_no)

            elif Is_Empty == 'yes':
                is_empty_func(column_type, column, num_rows, data, is_yes_no)

            else:
                data[column] = [round(random.uniform(30000, 100000), 2) for _ in range(num_rows)]

        elif column_type == 'json':
            json_data = [{"key1": random.randint(1, 100), "key2": random.choice(["ASDFGH", "BNMZXCV", "CVBNMQWERTY"])}
                         for _ in
                         range(num_rows)]
            data[column] = [json.dumps(item) for item in json_data]

        elif column_type == 'boolean':

            if IS_Null == "yes" and Is_Empty == 'yes':
                is_null_and_is_empty_func(column_type, column, num_rows, data, is_yes_no)

            elif IS_Null == "yes":
                is_null_func(column_type, column, num_rows, data, is_yes_no)

            elif Is_Empty == 'yes':
                is_empty_func(column_type, column, num_rows, data, is_yes_no)

            else:
                if is_yes_no:
                    data[column] = [random.choice(["yes", "no"]) for _ in range(num_rows)]
                else:
                    data[column] = [random.choice([True, False]) for _ in range(num_rows)]

        elif column_type == 'list':
            data[column] = [[fake.phone_number(), names.get_first_name(), r.get_random_word()] for _ in range(num_rows)]

    return data
