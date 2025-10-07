import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import json

depth = 2

def isInBound(val : int, minv : int, maxv :int) -> bool:
    return (val <= maxv and val >= minv)

def removeSpecialsLower(token: str) -> str:
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
        if token in stopwords.words('english'):
            continue
        if token in visited:
            continue
        visited.add(token)
        extractedTokens = extractTokens(token)
        if (not extractedTokens):
            continue
        related.append({"word": token, "depth": depthCount})
        recursive(related, extractedTokens, depthCount + 1, visited)

def main():
    jobRelated = []
    tokens = extractTokens("job")
    recursive(jobRelated, tokens)
    with open("result.json", "w") as file:
        json.dump(jobRelated, file, indent=4, sort_keys=True)
    print("Hello from generate-themed-vocab!")

if __name__ == "__main__":
    main()
