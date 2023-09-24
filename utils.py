import openai
import pandas as pd

def read_csv(path):
    return pd.read_csv(path)

def write_csv(path, data, header=None, create_folder=True):
    if create_folder:
        path.parent.mkdir(parents=True, exist_ok=True)

    if type(data) == pd.DataFrame:
        data.to_csv(path, index=False)
    elif type(data) == str:
        with open(path, 'w') as f:
            if header is not None:
                f.write(",".join(header) + "\n")
            f.write(data)

def get_completion(prompt, model="gpt-3.5-turbo-0613", temperature=0): 
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message["content"]

def string_func_to_func(func_str, func_name):
    namespace = {}
    exec(func_str, globals(), namespace)
    convert_data_row = lambda x: namespace[func_name](x)
    return convert_data_row
