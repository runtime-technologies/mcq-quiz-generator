# MCQ Question Generator

## Prerequisites

- Python 3.6 or greater
- Pip
- Virtual Environments

## Install Instructions

- Create a virtual environment using ```python -m venv ./env```
- Activate the virtual environment using
  - Windows: ```env\Scripts\activate```
  - Linux / Mac: ```source env/bin/activate```
- Install the requirements using ```pip install -r requirements.txt```

## Running the page scraper

- List out the question topics in `topics.txt` with each topic on a new line
- Run ```python ./scripts/scraper.py```

## Running the temp generator

- Run ```python driver.py```
- Output will be stored in questions.txt

## To Do

- [ ] Implement simple question generator
- [ ] Test output formats
- [ ] Test [MCQ Generator](https://github.com/KristiyanVachev/Question-Generation)
- [ ] Create script to automate setup

## References

- [BERT Wordnet Conceptnet](https://towardsdatascience.com/practical-ai-automatically-generate-multiple-choice-questions-mcqs-from-any-content-with-bert-2140d53a9bf5)
- []