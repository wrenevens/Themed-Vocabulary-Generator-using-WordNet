
# Vocabulary Generator using WordNet

This Python project generates themed vocabulary lists based on seed words using WordNet. It recursively extracts related words from the definitions of each seed word, filters out stopwords, and allows you to interactively explore and check word relationships.

## Features

* Generate related words for a list of seed words.
* Filter out common stopwords automatically.
* Remove non-alphabetic characters and normalize words to lowercase.
* Recursively explore WordNet definitions up to a configurable depth.
* Interactive command-line interface (CLI) to:

  * Switch between seed words.
  * View related words for the current seed.
  * Check if a specific word is related to the current seed.
* Save the generated vocabulary to a JSON file (`result.json`).

## Requirements

* Python 3.8+
* NLTK library

Install the required packages using **uv**:

```bash
uv add nltk
```

## Setup

1. Clone or download this repository.
2. Run the script to download necessary NLTK data:

```python
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
```

## Usage

Run the Python script using uv:

```bash
uv run python generate_vocab.py
```

Follow the CLI prompts:

1. **Set seed**: Switch between different seed words.
2. **View related**: List all related words for the current seed.
3. **Check related**: Enter a word to check if it's related to the current seed.
4. **Exit**: Quit the CLI.

### Example CLI

```
Current seed = "job"
1. Set seed, 2. View related, 3. Check related, 4. Exit: 2
- "work"
- "employment"
Total related words: 25
```

## Configuration

* `SEEDS`: List of seed words.
* `MAX_DEPTH`: Maximum depth for recursive token extraction.
* `STOP_WORDS`: Words to ignore (from NLTK's stopwords corpus).

## Output

The generated vocabulary is saved in `result.json` in the following format:

```json
[
    {
        "seed": "job",
        "related": [
            {"word": "employment", "depth": 0},
            {"word": "work", "depth": 1}
        ]
    },
    {
        "seed": "education",
        "related": [
            {"word": "learning", "depth": 0}
        ]
    }
]
```

## License

This project is released under the MIT License.
