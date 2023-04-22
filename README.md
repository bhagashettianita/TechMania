# TechMania

Search Engine designed to search all the Technology News and Articles from 2013 - Present and
to find Document Similarity between 2 articles. 

## **Dataset**:

* Reuters.csv
    * Scraped from [Reuters](https://www.reuters.com/news/archive/technologynews?view=page&page=1&pageSize=10)

## Libraries to Install

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Scikitlearn, nltk.

```bash
pip install scikitlearn
pip install nltk
```
```python
nltk.download(stopwords = 'english')
```

## Usage

Go to Folder search and Type these commands in Command Prompt for Ranked Retrival

```bash
python preprocessing.py
python trie.py
python indexing.py
python ranked_retreival.py
```
Go to Folder search and Type these commands in Command Prompt for Document Similarity

```bash
python DocSim.py
python relevantdocs.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
