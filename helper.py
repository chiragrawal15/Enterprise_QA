import string
import random

CREATE_TABLE_TEMPLATE = """ CREATE TABLE {table_name} ( {table_info} )"""
INSERT_VALUES_TEMPLATE = """ {COLUMN_LIST} \n 1 {row_1} \n 2 {row_2} \n 3 {row_3}"""
THRESHOLD = 4000


# Updates the create table query to include column/table level constraints like non-null/primary key/foreign key etc
def apply_table_constraints(schema_str):
    return schema_str


def trim_given_criteria(create_table_prompt):
    return create_table_prompt


def get_random_int():
    return 100


def get_random_str():
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for i in range(10))
    return random_str


def get_random_bool():
    return "true"


def token_length_checker(prompts):
    for table, prompt in prompts.items():
        if len(prompt[0]) > THRESHOLD:
            trimmed_prompt = trim_given_criteria(prompt[0])
            prompts[table] = trimmed_prompt
    return prompts


def column_and_type_info(column_family):
    schema_str = ""
    meta = ""
    for column_name, column_type in column_family.items():
        schema_str += f"{column_name} {column_type} {meta}"

    schema_str = apply_table_constraints(schema_str)
    return schema_str


def create_table_generator(dict_obj):
    prompts_output = {}
    for key, val in dict_obj.items():
        table_name = key
        table_info = column_and_type_info(val)
        list_of_columns = list(val.keys())

        prompts_output[table_name] = (table_info, list_of_columns)

    # Token length checker to ensure we create prompts within a limit and breakup things if needed
    cleaned_prompts = token_length_checker(prompts_output)

    all_create_table_st = [CREATE_TABLE_TEMPLATE.replace("table_name", key).replace("table_info", val[0]) for key, val in cleaned_prompts.items()]
    return all_create_table_st


def random_val_generate_given_type(data_type):
    switcher = {
        "INTEGER": get_random_int,
        "STRING": get_random_str,
        "BOOL": get_random_bool,
    }

    return switcher.get(data_type, get_random_str)


def random_data_generator(list_of_columns):

    column_list_str = " ".join(list_of_columns)
    rows = [column_list_str]
    for row_count in range(3):
        list_of_random_vals = []
        for col, col_type in list_of_columns.items():
            random_val = random_val_generate_given_type(col_type)()
            list_of_random_vals.append(random_val)
        row_str = [str(x) for x in list_of_random_vals]
        row_str = " ".join(row_str)
        rows.append(row_str)
    return rows