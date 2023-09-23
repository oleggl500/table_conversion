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