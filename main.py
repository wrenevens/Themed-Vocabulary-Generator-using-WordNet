import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import os
import csv

# Download required corpora
nltk.download('wordnet')
nltk.download('stopwords')

SEEDS = ["job", "education", "entertainment"]
MAX_DEPTH = 2
STOP_WORDS = set(stopwords.words('english'))

def is_meaningful_word(word : str) -> bool:
    return len(wn.synsets(word)) != 0

def clean_lowercase(token: str) -> str:
    """Remove non-lowercase letters and convert to lowercase."""
    token = token.lower()
    return "".join(c for c in token if c.islower())

def extract_definition_tokens(word: str) -> list[str]:
    """Extract tokens from all WordNet definitions of a word."""
    tokens = []
    for syn in wn.synsets(word):
        tokens.extend(syn.definition().split())
    return tokens

def build_related_words(related_words: list, tokens: list, depth_count=0, visited=None):
    """Recursively build related words from tokens."""
    if visited is None:
        visited = set()
    if depth_count == MAX_DEPTH:
        return
    for token in tokens:
        token = clean_lowercase(token)
        if not token or token in STOP_WORDS or token in visited:
            continue
        visited.add(token)
        token_tokens = extract_definition_tokens(token)
        if token_tokens:
            related_words.append({"word": token, "depth": depth_count})
            build_related_words(related_words, token_tokens, depth_count + 1, visited)

def fetch_seeds_from_file(file_name: str) -> list[str]:
    """Read seed words from a file, one per line, and return as a list of strings."""
    with open(file_name, "r", encoding="utf-8") as file:
        # Strip whitespace and ignore empty lines
        seeds = [line.strip() for line in file if line.strip()]
    return seeds


def extract_vocabulary(vocabulary_result : list, seeds : list):
    # Generate related words for each seed
    for seed in seeds:
        seed_related_words = []
        seed_tokens = extract_definition_tokens(seed)
        visited_tokens = set()
        visited_tokens.add(seed)
        build_related_words(seed_related_words, seed_tokens, visited=visited_tokens)
        vocabulary_result.append({"seed": seed, "related": seed_related_words})

def save_seeds_to_csv(seeds: list[str], file_name: str):
    """
    Append seed words to a CSV file, one per row.
    
    Args:
        seeds (list[str]): List of seed words to save.
        file_name (str): CSV file path.
    """
    file_exists = os.path.isfile(file_name)
    
    with open(file_name, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header if file is new
        if not file_exists or os.path.getsize(file_name) == 0:
            writer.writerow(["seed"])
        
        for seed in seeds:
            writer.writerow([seed])


def append_result_to_csv(vocabulary_result: list, file_name: str):
    """
    Append vocabulary results to a CSV file.
    
    CSV columns: seed, word, depth
    """
    # Open file in append mode
    with open(file_name, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Write header if file is empty
        if csvfile.tell() == 0:
            writer.writerow(["seed", "word", "depth"])
        for seed_entry in vocabulary_result:
            seed = seed_entry["seed"]
            for token_entry in seed_entry["related"]:
                writer.writerow([seed, token_entry["word"], token_entry["depth"]])


def main():
    file_seeds = fetch_seeds_from_file("seed.csv")
    file_vocabulary_result = []
    extract_vocabulary(file_vocabulary_result, file_seeds)
    # CLI interface
    session_seeds = []
    session_vocabulary_result = []
    current_seed = file_seeds[0] if file_seeds else ""
    is_running = True
    while is_running:
        print(f'Current seed = "{current_seed}"')
        user_input = input("1. Set seed, 2. View related, 3. Check related, 4. Add seed, 5. Run data process,6. Exit: ")
        match user_input:
            case "1":
                print("Available seeds: ", end="")
                for seed in file_seeds:
                    print(f'"{seed}"', end=', ')
                print()
                new_seed = input("Set seed: ")
                while new_seed not in file_seeds:
                    new_seed = input("Set seed: ")
                current_seed = new_seed
            case "2":
                for seed_entry in file_vocabulary_result:
                    if seed_entry["seed"] != current_seed:
                        continue
                    for token_entry in seed_entry["related"]:
                        print(f'- "{token_entry["word"]}"')
                    print(f"Total related words: {len(seed_entry['related'])}")
            case "3":
                for seed_entry in file_vocabulary_result:
                    if seed_entry["seed"] != current_seed:
                        continue
                    word_to_check = clean_lowercase(input("Word to check: ").strip())
                    related_dict = {t["word"]: t for t in seed_entry["related"]}
                    if word_to_check in related_dict:
                        word_info = related_dict[word_to_check]
                        print(f'Your word is related! Word: "{word_info["word"]}", Depth: {word_info["depth"]}')
                    else:
                        print("Your word is not related.")
            case "4":
                new_seed_input = clean_lowercase(input("New seed: ").strip())
                while not is_meaningful_word(new_seed_input):
                    print("Not meaningful word!")
                    new_seed_input = clean_lowercase(input("New seed: ").strip())
                session_seeds.append(new_seed_input)
                file_seeds.append(new_seed_input)

            case "5":
                extract_vocabulary(session_vocabulary_result, session_seeds)
                file_vocabulary_result.extend(session_vocabulary_result)
                print("Vocabulary generated")

            case "6":
                is_running = False

    print("Goodbye!")
    append_result_to_csv(session_vocabulary_result, "result.csv")
    save_seeds_to_csv(session_seeds, "seed.csv")


if __name__ == "__main__":
    main()
