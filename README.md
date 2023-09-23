# Table conversion to template
This repository contains script for conversion of sorce table to template using LLM. More specifically, OpenAI api.

## Setup
Install requirements
```bash
python3 -m pip install requirements.txt
```

## Runing
To run the script on specify sorce, template and target csv files
```bash
convert_table.py —-source <source CSV> —-template <template CSV> —-target <target CSV>
```