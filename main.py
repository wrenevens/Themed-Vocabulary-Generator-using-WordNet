import nltk
from nltk.corpus import wordnet as wn
import json
depth = 2

def extractTokens(word):
    result = []
    try:
        result = wn.synsets(word)[0].definition().split(" ")
    except:
        result = []
    return result

def giveTokens(related : list, token):
    procTokens = extractTokens(token)
    for tok in procTokens:
        related.append(tok)
"""
tokens = [0, 1, 2, 3]
tokens_ = [[4, 5], [6, 7], [8, 9], [10, 11]]
"""
def recursive(related : list, tokens, depthCount = 0):
    if (depthCount == depth):
        return
    for token in tokens:
        related.append(
            json.dumps({"word" : token,
             "depth" : depthCount}, indent=4, sort_keys=True)
        )
        recursive(related=related, tokens=extractTokens(token), depthCount=depthCount + 1)

def main():
    jobRelated = []
    tokens = extractTokens("job")
    recursive(jobRelated, tokens)
    with open("result.json", "w") as file:
        for token in jobRelated:
            file.write(token)


        
        
    print("Hello from generate-themed-vocab!")


if __name__ == "__main__":
    main()
