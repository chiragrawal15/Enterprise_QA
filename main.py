# Setting up Prompts for initilization of LLMs to provide Text-to-SQL across different categories.
# As a more nuanced step, explore if it can also join b/w two different categories of information

from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain import hub
from langchain.prompts import PromptTemplate
import helper as ph
import json
import os

os.environ["OPENAI_API_KEY"] = ""

# Assumes availability of such mapping information which captures the kind of API endpoints and objects there are for a given category
unified_api_json = json.load(open("metadata/unified_api_schema.json",))

CUSTOM_PROMPT_FOR_SQL_GEN = hub.pull("rlm/text-to-sql")

class CategoryLevelPromptGeneration:

    def __init__(self, category_key):
        self.category = category_key
        # Get the right configuration from json body
        self.schema_details = unified_api_json[category_key]
        return

    def prompt_gen(self):
        create_table_prompts = ph.create_table_generator(self.schema_details)

        # Generate a SQL file for creation of DB using the create table prompts
        self.generate_sql_file_to_create_tables(create_table_prompts)

        # Generate random data for all these create table prompts
        final_prompt = {}
        for table, details in create_table_prompts.items():
            final_prompt[table] = details[0] + ph.random_data_generator(details[1])
        return final_prompt

    def generate_sql_file_to_create_tables(self, create_table_prompts):
        for table, prompt in create_table_prompts.items():
            file = open(f"create_table_{self.category}_table.sql", "w")
            create_table_prompts_str = prompt[0]
            file.write(create_table_prompts_str)
        return

    def get_all_prompts(self):
        CUSTOM_PROMPT = PromptTemplate(
            input_variables=["input", "few_shot_examples", "table_info", "dialect"], template=CUSTOM_PROMPT_FOR_SQL_GEN
        )
        return CUSTOM_PROMPT


if __name__ == "__main__":

    db = SQLDatabase.from_uri("sqlite:///Chinook.db")
    llm = OpenAI(temperature=0, verbose=True)
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

    # Get the list of all applicable categories and iterate to generate prompts

    for keys, json_body in unified_api_json.items():
        prompt_gen_obj = CategoryLevelPromptGeneration(keys)

        all_prompts = prompt_gen_obj.get_all_prompts()

        # TODO: Execution of all these prompts and verifying the working




