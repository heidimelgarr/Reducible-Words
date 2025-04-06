"""
Student information for this assignment:

Replace <FULL NAME> with your name.
On my/our honor, Heidi Melgar, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID 1: he3839
"""
import sys

# the constant used to calculate the step size
STEP_SIZE_CONSTANT = 3


# DO NOT modify this function.
def is_prime(n):
    """
    Determines if a number is prime.

    pre: n is a positive integer.
    post: Returns True if n is prime, otherwise returns False.
    """
    if n == 1:
        return False

    limit = int(n**0.5) + 1
    div = 2
    while div < limit:
        if n % div == 0:
            return False
        div += 1
    return True

# DO NOT modify this function.
def hash_word(s, size):
    """
    Hashes a lowercase string to an index in a hash table.

    pre: s is a lowercase string, and size is a positive integer representing either
         hash table size or the constant for double hashing.
    post: Returns an integer index in the range [0, size - 1] where the string hashes to.
    """
    hash_idx = 0
    for c in s:
        letter = ord(c) - 96
        hash_idx = (hash_idx * 26 + letter) % size
    return hash_idx


# TO DO
def step_size(s):
    """
    Calculates step size for double hashing using STEP_SIZE_CONSTANT.

    pre: s is a lowercase string.
    post: Returns the calculated step size as an integer based on the provided string.
    """
    length = len(s)

    # If the str length is less than or equal to 3
    if length <= 3:
        return 2

    # If the str length is divisible by 3
    if length % 3 == 0 or length % 7 == 0:
        return 3
    return 1


# TO DO
def insert_word(s, hash_table):
    """
    Inserts a string into the hash table using double hashing for collision resolution.
    No duplicates are allowed.

    pre: s is a string, and hash_table is a list representing the hash table.
    post: Inserts s into hash_table at the correct index; resolves any collisions
          by double hashing.
    """
    first_index = hash(s) % len(hash_table)

    # Double hashing
    remainder = hash(s) % (len(hash_table) - 1)
    second_index = 1 + remainder

    # Handle collision using double hashing
    index = first_index
    while hash_table[index] != "" and hash_table[index] != s:
        index = (index + second_index) % len(hash_table)

    hash_table[index] = s


# TO DO
def find_word(s, hash_table):
    """
    Searches for a string in the hash table.
    Note: using the `in` operator is incorrect as that will be O(N). We want
          an O(1) time average time complexity using hashing.

    pre: s is a string, and hash_table is a list representing the hash table.
    post: Returns True if s is found in hash_table, otherwise returns False.
    """
    first_index = hash(s) % len(hash_table)
    # Double hashing
    remainder = hash(s) % (len(hash_table) - 1)
    second_index = 1 + remainder

    # Start checking from the calculated index
    index = first_index
    while hash_table[index] != "":
        if hash_table[index] == s:
            return True
        index = (index + second_index) % len(hash_table)
    return False


# TO DO
def is_reducible(s, hash_table, hash_memo):
    """
    Determines if a string is reducible using a recursive check.

    pre: s is a lowercase string, hash_table is a list representing the hash table,
         and hash_memo is a list representing the hash table
         for memoization.
    post: Returns True if s is reducible (also updates hash_memo by
          inserting s if reducible), otherwise returns False.
    """
    # word alr seen
    if s in hash_memo:
        return hash_memo[s]

    # already in the hash table
    if find_word(s, hash_table):
        hash_memo[s] = True
        return True

    # single letter words
    if len(s) == 1:
        hash_memo[s] = False
        return False

    # removing one letter at a time
    for i in range(len(s)):
        reduced_word = s[:i] + s[i+1:]

        # if it is reducible
        check_word = find_word(reduced_word, hash_table)
        reducible = is_reducible(reduced_word, hash_table, hash_memo)

        if check_word and reducible:
            # Memoize the result for the current word
            hash_memo[reduced_word] = True
            hash_memo[s] = True
            return True

    hash_memo[s] = False
    return False

# TO DO
def get_longest_words(string_list):
    """
    Finds longest words from a list.

    pre: string_list is a list of lowercase strings.
    post: Returns a list of words in string_list that have the maximum length.
    """
    # Find the longest length
    max_length = 0
    for word in string_list:
        max_length = max(max_length, len(word))

    # Collect all words with that length
    longest_words = []
    for word in string_list:
        if len(word) == max_length:
            longest_words.append(word)

    return longest_words


# TO DO
def main():
    """The main function that calculates the longest reducible words"""
    # create an empty word_list
    # read words using input redirection
    # where each line read from input()
    # should be a single word. Append to word_list
    # ensure each word has no trailing white space.
    word_list = []
    for line in sys.stdin:
        line = line.strip()  # Remove any trailing whitespace
        if line:
            word_list.append(line)

    # find length of word_list
    # determine prime number N that is greater than twice
    # the length of the word_list
    guess = 2 * len(word_list)
    while not is_prime(guess):
        guess = guess + 1
    n = guess # prime

    # create an empty hash_list
    # populate the hash_list with N blank strings
    # hash each word in word_list into hash_list
    # for collisions use double hashing
    hash_list = [""] * n
    for word in word_list:
        insert_word(word, hash_list)

    # create an empty hash_memo of size M
    # we do not know a priori how many words will be reducible
    # let us assume it is 10 percent (fairly safe) of the words
    # then M is a prime number that is slightly greater than
    # 0.2 * size of word_list
    m = int(0.2 * len(word_list)) + 1

    while is_prime(m) is False:
        m += 1
    hash_memo = [None] * m

    # populate the hash_memo with M blank strings
    reducible_words = []
    for word in word_list:
        if is_reducible(word, hash_list, hash_memo):
            reducible_words.append(word)

    # create an empty list reducible_words
     # for each word in the word_list recursively determine
    # if it is reducible, if it is, add it to reducible_words
    # as you recursively remove one letter at a time check
    # first if the sub-word exists in the hash_memo. if it does
    # then the word is reducible and you do not have to test
    # any further. add the word to the hash_memo.

    # find the largest reducible words in reducible_words
    longest_words = get_longest_words(reducible_words)
    # print the reducible words in alphabetical order
    # one word per line
    ordered_words = sorted(longest_words)

    for word in ordered_words:
        print(word)

if __name__ == "__main__":
    main()
