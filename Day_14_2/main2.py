from collections import Counter

N = 40

with open("input.txt", "r") as f:
    template = f.readline().strip()
    f.readline()  # skip empty line
    insertions = dict(line.strip().split(" -> ") for line in f.readlines())

# first find all tuples of consecutive characters - we'll call these `codes`.
codes = [template[i:i+2] for i in range(len(template)-1)]


def resolve(codes_counter, insertions):
    """
    We don't actually need to count single letters - we can instead just
    directly operate on our codes: on each step take e.g. one CH out and
    add one CB and BH in - so resolve each code to it's two replacement
    codes.
    """
    new_counter = codes_counter.copy()
    for code, count in codes_counter.items():
        if count <= 0:
            continue
        new_counter[code] -= count
        inserted = insertions[code]
        left_code = f"{code[0]}{inserted}"
        right_code = f"{inserted}{code[1]}"
        new_counter[left_code] += count
        new_counter[right_code] += count
    return new_counter


if __name__ == "__main__":

    # start off by iteratively resolving each code into it's replacement parts
    c = Counter(codes)
    for _ in range(N):
        c = resolve(c, insertions)

    # we now count how often all the letters come up in the code
    letter_counter = Counter()
    letters = set("".join(c.keys()))
    for letter in letters:
        for code, count in c.items():
            if letter in code:
                letter_counter[letter] += count
            if f"{letter}{letter}" == code:
                letter_counter[letter] += count
    # at this point there should be two letters in our counter
    # with an odd number of occurences: since any two letters ab
    # get resolved into a code ac cb we'll count all the c's twice.
    # So to find the number of actual occurences we first increase
    # the counts for the first and last letter (a and b) by one.
    letter_counter[template[0]] += 1
    letter_counter[template[-1]] += 1
    # And then divide them by two.
    for key in letter_counter:
        letter_counter[key] = letter_counter[key] // 2
    # print(f"After {N} steps we have")
    # print(letter_counter)

    print("Difference between most and least common =",
          letter_counter.most_common()[0][1] - letter_counter.most_common()[-1][1])
