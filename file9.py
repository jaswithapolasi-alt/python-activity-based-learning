
# Repeated Word and Phrase Detection

def detect_repeated_words(paragraph):
    # Normalize letter case
    paragraph = paragraph.lower()

    # Replace common punctuation with spaces
    punctuation = ".,!?;:()[]{}\"'"
    for symbol in punctuation:
        paragraph = paragraph.replace(symbol, " ")

    # Split paragraph into words
    words = paragraph.split()

    # Store unique words and their positions
    word_list = []
    word_counts = []
    word_positions = []

    for index in range(len(words)):
        word = words[index]

        if word in word_list:
            position = word_list.index(word)
            word_counts[position] += 1
            word_positions[position].append(index + 1)
        else:
            word_list.append(word)
            word_counts.append(1)
            word_positions.append([index + 1])

    # Display all word occurrences
    print("\nWord Occurrence Report")
    print("-" * 45)

    for i in range(len(word_list)):
        print(
            word_list[i],
            "-> Count:", word_counts[i],
            "| Positions:", word_positions[i]
        )

    # Display repeated words
    print("\nRepeated Words")
    print("-" * 45)

    found = False

    for i in range(len(word_list)):
        if word_counts[i] > 1:
            print(
                word_list[i],
                "appears", word_counts[i],
                "times at positions",
                word_positions[i]
            )
            found = True

    if not found:
        print("No repeated words found.")


def detect_repeated_phrases(paragraph, phrase_length):
    # Normalize case and punctuation
    paragraph = paragraph.lower()

    punctuation = ".,!?;:()[]{}\"'"
    for symbol in punctuation:
        paragraph = paragraph.replace(symbol, " ")

    words = paragraph.split()
    phrases = []
    phrase_counts = []
    phrase_positions = []

    if phrase_length <= 0:
        print("Phrase length must be greater than zero.")
        return

    if phrase_length > len(words):
        print("Phrase length exceeds the number of words.")
        return

    # Generate consecutive phrases
    for i in range(len(words) - phrase_length + 1):
        phrase = " ".join(words[i:i + phrase_length])

        if phrase in phrases:
            position = phrases.index(phrase)
            phrase_counts[position] += 1
            phrase_positions[position].append(i + 1)
        else:
            phrases.append(phrase)
            phrase_counts.append(1)
            phrase_positions.append([i + 1])

    print("\nRepeated Phrases")
    print("-" * 45)

    found = False

    for i in range(len(phrases)):
        if phrase_counts[i] > 1:
            print(
                "'" + phrases[i] + "'",
                "appears", phrase_counts[i],
                "times at starting positions",
                phrase_positions[i]
            )
            found = True

    if not found:
        print("No repeated phrases found.")


# Main program
print("=" * 45)
print("REPEATED WORD AND PHRASE DETECTION")
print("=" * 45)

text = input("\nEnter a paragraph:\n")

detect_repeated_words(text)

try:
    length = int(
        input("\nEnter phrase length in words (e.g., 2): ")
    )
    detect_repeated_phrases(text, length)
except ValueError:
    print("Please enter a valid integer for phrase length.")
