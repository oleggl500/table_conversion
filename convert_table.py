import argparse
import openai
from dotenv import load_dotenv
from pathlib import Path
import os
import json
import pandas as pd
import sys
from utils import read_csv, write_csv, get_completion, string_func_to_func

FUNCTION_NAME = 'convert_source_to_template'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('./test_data/table_B.csv'), help='source CSV')
    parser.add_argument('--template', type=Path, default=Path('./test_data/template.csv'), help='template CSV')
    parser.add_argument('--target', type=Path, default=Path('./output/result_B.csv'), help='target CSV')

    return parser.parse_args()

def is_values_close(source,template,source_col_name,template_col_name):
    example_srring = ''
    for feature_name in template.columns:
        example_srring += f'{feature_name}: {template.head()[feature_name].to_list()} \n'
    prompt = f'''
{example_srring}
What is the coulumn name of the feature values? Take into account that format of features may differ. Please just output the name of the column.
{source.head()[source_col_name].to_list()}
    '''
    # print(prompt, len(prompt))
    response = get_completion(prompt)
    # print(response)
    return template_col_name in response

def get_column_mapping(source,template):
    output_dict_template = "{" + ", ".join([f'"{key}": [<list of column names>]' for key in template.columns]) + "}"

    prompt = f'''
    Write python dict for mapping template columns to source columns. 
    source:
    {source.head().to_csv(index=False)}
    template:
    {template.head().to_csv(index=False)}
    Do the following steps:
    1. For each column name in the template, provide a list of most similar column names in source table, if column type is the same
    2. If column type is not the same, remove it from the list of similar column names.
    3. Do not output any other text execept for the python dictionary.
    The output should be in a format:
    {output_dict_template}
    '''
    # print(prompt, len(prompt))
    response = get_completion(prompt)
    # print(response)

    mapping_dict = json.loads(response)
    source2template = {}
    for template_col, source_cols in mapping_dict.items():
        for source_col in source_cols:
            if is_values_close(source,template,source_col,template_col):
                source2template[source_col]= template_col
                break
    return source2template

def change_columns_format(source,template):
    prompt = f'''
    Write python code that convert source feature format to template feature format 
    source:
    {source.head(3).to_csv(index=False)}
    template:
    {template.head(3).to_csv(index=False)}
    Do the following steps:
    1. Write code that convert source feature format to template feature format.
    2. Do not merge the columns.
    3. Do not output any other text execept for the python code.
    The output should be in a format:
    def {FUNCTION_NAME}(source):
        <code here>
        return result
    '''
    # print(prompt, len(prompt))
    response = get_completion(prompt)
    # print(response)
    func = string_func_to_func(response, FUNCTION_NAME)
    try:
        result = func(source.to_csv(index=False))
    except:
        print("Python function failed to execute")
        sys.exit(1)
    return result

def main(args,source,template,):
    try:
        print("Generating column mapping")
        mapping_dict = get_column_mapping(source,template)
        print("Mapping generated")

        if len(mapping_dict) < len(template.columns):
            print("Not all columns are mapped")
            raise Exception("Not all columns are mapped")

        # Remove columns that are not in template
        source = source[mapping_dict.keys()]
        
        # Rename columns to template
        source = source.rename(columns=mapping_dict)
        
        print("Converting table")
        result = change_columns_format(source,template)
        print("Table converted")
        
        # print("\n".join(result))
        
        print(f"Writing result to {args.target}")
        write_csv(args.target,result,header=None)
    except Exception as e:
        print(f"Error caught: {e}")
        sys.exit(1)

if __name__ == '__main__':
    args = parse_args()
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    source = read_csv(args.source)
    template = read_csv(args.template)
    main(args,source,template)