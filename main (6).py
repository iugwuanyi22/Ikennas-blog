import random
import string

# Use your uploaded word bank file
WORD_BANK_FILE= "word_bank.txt"  
MAX_INCORRECT_GUESSES = 6


def load_word_bank(filename):
    """
    Reads words from the given filename.
    Returns a list of lowercase words, skipping blank lines.
    """
    words = []
    try:
        with open(filename, "r") as f:
            for line in f:
                word = line.strip()
                if word:
                    words.append(word.lower())
    except FileNotFoundError:
        print(f"Error: Could not find the file '{filename}'.")
        return []

    if not words:
        print(f"Error: The file '{filename}' does not contain any words.")
    return words


def choose_secret_word(words):
    """Return a random word from the word list."""
    return random.choice(words)


def display_current_state(secret_word, guessed_letters, incorrect_guesses):
    """
    Show the word with underscores for unguessed letters and
    the number of incorrect guesses remaining.
    Example: _ p p _ e   4/6 remaining
    """
    display_chars = []
    for ch in secret_word:
        if ch in guessed_letters:
            display_chars.append(ch)
        else:
            display_chars.append("_")

    display_word = " ".join(display_chars)
    remaining = MAX_INCORRECT_GUESSES - incorrect_guesses

    print("\nWord:", display_word)
    print(f"Incorrect guesses remaining: {remaining}/{MAX_INCORRECT_GUESSES}")
    if guessed_letters:
        print("Guessed letters:", " ".join(sorted(guessed_letters)))
    else:
        print("Guessed letters: (none yet)")


def get_valid_guess(already_guessed):
    """
    Prompt the user for a single letter guess.
    Ensures:
      - exactly one character
      - alphabetic
      - not already guessed
    Returns a lowercase letter.
    """
    while True:
        guess = input("Enter a letter: ").strip().lower()

        if len(guess) != 1 or guess not in string.ascii_lowercase:
            print("Invalid input. Please enter a single letter (a-z).")
            continue

        if guess in already_guessed:
            print(f"You already guessed '{guess}'. Try a different letter.")
            continue

        return guess


def play_single_game(words):
    """
    Play one game of Hangman with a randomly chosen word.
    """
    secret_word = choose_secret_word(words)
    guessed_letters = set()
    correct_letters = set()
    incorrect_guesses = 0

    unique_letters = set(secret_word)

    print("\n=== New Game of Hangman! ===")
    print(f"The word has {len(secret_word)} letters.")

    while incorrect_guesses < MAX_INCORRECT_GUESSES and correct_letters != unique_letters:
        display_current_state(secret_word, guessed_letters, incorrect_guesses)
        guess = get_valid_guess(guessed_letters)

        guessed_letters.add(guess)

        if guess in unique_letters:
            print(f"Nice! '{guess}' is in the word.")
            correct_letters.add(guess)
        else:
            incorrect_guesses += 1
            print(f"Sorry, '{guess}' is not in the word.")

    # End of game
    if correct_letters == unique_letters:
        display_current_state(secret_word, guessed_letters, incorrect_guesses)
        print("\n🎉 You guessed the word!")
        print(f"The word was: {secret_word}")
    else:
        print("\n😢 You're out of guesses.")
        print(f"The correct word was: {secret_word}")


def ask_play_again():
    """
    Ask the user if they want to play again.
    Returns True if yes, False if no.
    """
    while True:
        answer = input("\nPlay again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter 'y' for yes or 'n' for no.")


def main():
    words = load_word_bank(WORD_BANK_FILE)
    if not words:
        return  # Cannot play without words

    print("Welcome to Hangman!")

    while True:
        play_single_game(words)
        if not ask_play_again():
            break

    print("\nThanks for playing! Goodbye.")


if __name__ == "__main__":
    main()
