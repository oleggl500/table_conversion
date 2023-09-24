# Table conversion to template
This repository contains script for conversion of sorce table to template using LLM. More specifically, OpenAI api.

## Setup
Install requirements
```bash
python3 -m pip install requirements.txt
```

## Runing
The script uses openai API before running the script specify ether as enviroment variable or in .env file the OPENAI_API_KEY
```bash
export OPENAI_API_KEY=<your key>
```
or 
```bash
echo "OPENAI_API_KEY=<your key>" > .env
```

To run the script on specify sorce, template and target csv files
```bash
convert_table.py —-source <source CSV> —-template <template CSV> —-target <target CSV>
```
# Thoughts on edge cases
The script relies on LLM directly generating code. This means that it is not garanteed that the output will be as we expected. Threre may be errors in generated code. For instance, some columns can be very similar like last name and full name. Knowing data types of the collumns and data patterns will be very helpfull. If we provide them to LLMs and check the output for better accuracy of our conversion. 
|Edge case|Thoughts|
| ------------ | ------------ |
| Column is absent in source | LLM probably provide wrong mapping. Check the data type and patterns  |
| Column has similar name but different values  | Check the data type and patterns  |
|The mapping was incorrect but undetected| The code generation may fail, as a solution to this I would provide llm with more patterns that it can face and, thus, avoid errors|