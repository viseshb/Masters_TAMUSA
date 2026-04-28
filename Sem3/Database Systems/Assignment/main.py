from functools import reduce

text = "One a penny, two a penny, hot cross buns."
words = text.lower().replace(",", "").replace(".", "").split()
mapped = list(map(lambda w: (w, 1), words))
print("Map Output:", mapped)


def reducer(acc, pair):
    word, count = pair
    acc[word] = acc.get(word, 0) + count
    return acc

reduced = reduce(reducer, mapped, {})

print("Reduce Output:", reduced)
