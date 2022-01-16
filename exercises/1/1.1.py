from res import RESOURCES_PATH
from exercises.utils import preprocess
import csv
from collections import Counter
import itertools


def initialize_dict():
    defs = {}
    defs.setdefault("courage", [])
    defs.setdefault("paper", [])
    defs.setdefault("apprehension", [])
    defs.setdefault("sharpener", [])
    return defs


def get_all_words_defs():
    defs = initialize_dict()
    defs_file = RESOURCES_PATH / "defs.csv"

    with open(defs_file) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            defs.get("courage").append(preprocess(row[1]))
            defs.get("paper").append(preprocess(row[2]))
            defs.get("apprehension").append(preprocess(row[3]))
            defs.get("sharpener").append(preprocess(row[4]))

    return defs


def normalize(values):
    return [(float(v) - min(values)) / (max(values) - min(values)) for v in values]


def get_words_counts(defs):
    joined = list(itertools.chain.from_iterable(defs))
    counter = Counter(joined)
    return counter


def similarity(definition, words_counts):
    freq_sum = sum(words_counts[word] for word in definition)
    return freq_sum / len(definition)


def average_similarity(defs):
    words_counts = get_words_counts(defs)
    similarities = [similarity(d, words_counts) for d in defs]
    similarities = normalize(similarities)
    return sum(similarities) / len(similarities)


def compute_similarities():
    results = initialize_dict()
    all_words_defs = get_all_words_defs()

    for word in ("courage", "paper", "apprehension", "sharpener"):
        single_word_defs = all_words_defs.get(word)
        results[word] = average_similarity(single_word_defs)

    return results


def compute_aggregations():
    similarities = compute_similarities()

    result = []

    aggregations = [
        ("abstract", "courage", "apprehension"),
        ("concrete", "paper", "sharpener"),
        ("generic", "courage", "paper"),
        ("specific", "apprehension", "sharpener")
    ]

    for aggregation in aggregations:
        mean_similarity = (similarities[aggregation[1]] + similarities[aggregation[2]]) / 2
        result.append((aggregation[0], mean_similarity))

    return similarities, result


def print_results():
    similarities, aggregations = compute_aggregations()

    print("------ SIMILARITIES ------")
    for word, similarity in similarities.items():
        print(word, similarity)

    print("\n")

    print("------ AGGREGATIONS ------")
    for aggregation, mean_similarity in aggregations:
        print(aggregation, mean_similarity)


if __name__ == "__main__":
    print_results()