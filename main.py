import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import json

# Download required corpora
nltk.download('wordnet')
nltk.download('stopwords')

SEEDS = ["job", "education", "entertainment"]
MAX_DEPTH = 2
STOP_WORDS = set(stopwords.words('english'))

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

def main():
    vocabulary_result = []

    # Generate related words for each seed
    for seed in SEEDS:
        seed_related_words = []
        seed_tokens = extract_definition_tokens(seed)
        visited_tokens = set()
        visited_tokens.add(seed)
        build_related_words(seed_related_words, seed_tokens, visited=visited_tokens)
        vocabulary_result.append({"seed": seed, "related": seed_related_words})

    # Save result to JSON
    with open("result.json", "w") as file:
        json.dump(vocabulary_result, file, indent=4, sort_keys=True)

    print("Vocabulary generation complete! Output saved to result.json")

    # CLI interface
    current_seed = SEEDS[0]
    is_running = True
    while is_running:
        print(f'Current seed = "{current_seed}"')
        user_input = input("1. Set seed, 2. View related, 3. Check related, 4. Exit: ")
        match user_input:
            case "1":
                print("Available seeds: ", end="")
                for seed in SEEDS:
                    print(f'"{seed}"', end=', ')
                print()
                new_seed = input("Set seed: ")
                while new_seed not in SEEDS:
                    new_seed = input("Set seed: ")
                current_seed = new_seed
            case "2":
                for seed_entry in vocabulary_result:
                    if seed_entry["seed"] != current_seed:
                        continue
                    for token_entry in seed_entry["related"]:
                        print(f'- "{token_entry["word"]}"')
                    print(f"Total related words: {len(seed_entry['related'])}")
            case "3":
                for seed_entry in vocabulary_result:
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
                is_running = False

    print("Goodbye!")

if __name__ == "__main__":
    main()
