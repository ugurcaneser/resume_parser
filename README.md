
# Resume Parser

In this project, I created a Python code with which we can easily extract important key information from a Resume file provided in PDF format. Just provide your Resume file as PDF and get the important information inside in JSON format.


## Installation

Necessary Python libraries:

```bash
  pip install spacy PyPDF2 docx2txt regex
  python -m spacy download en_core_web_sm
  
```
    

## Usage/Examples

You'll only need to change output_path to your Resume file path. That's all!

```javascript
parser.save_to_json(parsed_data, output_path="parsed_resume.json")
```

