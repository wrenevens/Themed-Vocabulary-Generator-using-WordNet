import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import json

nltk.download('wordnet')
nltk.download('stopwords')

seeds = ["job", "education", "entertainment"]
depth = 2
stop_words = set(stopwords.words('english'))

def removeSpecialsLower(token: str) -> str:
    token = token.lower()
    return "".join(c for c in token if c.islower())

def extractTokens(word):
    tokens = []
    for syn in wn.synsets(word):
        tokens.extend(syn.definition().split())
    return tokens

def recursive(related: list, tokens, depthCount=0, visited=None):
    if visited is None:
        visited = set()
    if depthCount == depth:
        return
    for token in tokens:
        token = removeSpecialsLower(token)
        if not token or token in stop_words or token in visited:
            continue
        visited.add(token)
        extractedTokens = extractTokens(token)
        if extractedTokens:
            related.append({"word": token, "depth": depthCount})
            recursive(related, extractedTokens, depthCount + 1, visited)

def main():
    result = []
    for seed in seeds:
        seedRelated = []
        tokens = extractTokens(seed)
        visited = set()
        visited.add(seed)
        recursive(seedRelated, tokens, visited=visited)  # pass fresh visited per seed
        result.append({"seed": seed, "related": seedRelated})

    with open("result.json", "w") as file:
        json.dump(result, file, indent=4, sort_keys=True)

    print("Vocabulary generation complete! Output saved to result.json")

    currentSeed = seeds[0]
    isRunning = True
    while isRunning:
        print(f'currentSeed = "{currentSeed}"')
        userInput = input("1. Set seed, 2. View related, 3. Check related 4. exit: ")
        match userInput:
            case "1":
                print("Current seeds: ", end="")
                for seed in seeds:
                    print(f'"{seed}"', end=', ')
                print()
                currentSeedInput = input("Set seed: ")
                while currentSeedInput not in seeds:
                    currentSeedInput = input("Set seed: ")
                currentSeed = currentSeedInput
            case "2":
                for candidate in result:
                    if candidate["seed"] != currentSeed:
                        continue
                    for relatedToken in candidate["related"]:
                        print(f'- "{relatedToken["word"]}"')
                    print(f"Total: {len(candidate['related'])}")
            case "3":
                for candidate in result:
                    if candidate["seed"] != currentSeed:
                        continue
                    checkInput = removeSpecialsLower(input("Word want to check: ").strip())
                    related_dict = {t["word"]: t for t in candidate["related"]}
                    if checkInput in related_dict:
                        obj = related_dict[checkInput]
                        print(f"Your word is related! : {obj['word']}, depth: {obj['depth']}")
                    else:
                        print("Your word is not related")
            case "4":
                isRunning = False
    print("Goodbye!")




if __name__ == "__main__":
    main()
