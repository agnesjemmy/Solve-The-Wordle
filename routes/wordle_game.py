from flask import Blueprint, request, jsonify
import random

# Create a Blueprint
wordle_game_bp = Blueprint('wordle_game', __name__)

# Sample word list for Wordle
word_list = [
    "slate", "lucky", "maser", "gapes", "wages", "apple", "grape", "peach", "lemon", "berry",
    "crane", "table", "house", "money", "tiger", "green", "globe", "earth", "flame", "shark",
    "beach", "storm", "quiet", "music", "sword", "light", "drake", "phone", "chair", "brave",
    "grind", "power", "lodge", "creek", "frost", "fable", "grasp", "blaze", "hover", "cloud",
    "actor", "blend", "flair", "vivid", "stone", "steal", "pride", "quick", "knock", "rebel",
    "weary", "blend", "craft", "smoke", "frown", "mirth", "spade", "whale", "dried", "crook",
    "shiny", "plate", "bring", "dream", "lunar", "lance", "bloom", "grove", "shout", "thorn",
    "grain", "crawl", "brook", "leash", "crisp", "jolly", "grace", "speak", "stone", "vocal",
    "spike", "flock", "wheat", "piano", "solid", "creed", "wrath", "plume", "twist", "realm",
    "spool", "sleek", "split", "track", "forge", "glide", "slime", "crush", "spine", "sworn",
    "creep", "latch", "march", "flood", "spray", "swift", "quake", "slope", "brisk", "tease",
    "flash", "clash", "bluff", "flute", "trust", "quest", "batch", "feast", "mourn", "crane",
    "punch", "glint", "frost", "brave", "cloak", "tramp", "skate", "shift", "quill", "scout",
    "crack", "troop", "whirl", "gleam", "trout", "moist", "fluke", "scorn", "chill", "flair",
    "wound", "spear", "crisp", "glare", "hound", "lodge", "shrub", "grape", "stump", "flare",
    "chase", "cliff", "flame", "swarm", "swing", "broad", "flesh", "sharp", "spike", "scent",
    "trove", "brisk", "cloak", "shove", "plush", "drive", "pride", "trace", "click", "prune",
    "bland", "grove", "skirt", "patch", "trunk", "frown", "hasty", "scare", "glove", "bloom",
    "drift", "hover", "frank", "sneak", "crisp", "brace", "globe", "troop", "blaze", "drill",
    "plume", "froze", "latch", "glare", "split", "brine", "stout", "spray", "slash", "shiny",
    "twist", "flock", "clove", "grove", "prick", "flair", "shift", "stair", "crisp", "sleek",
    "frail", "plank", "split", "blame", "frisk", "smear", "crane", "grasp", "sworn", "crack",
    "flame", "stump", "track", "swipe", "plush", "bloat", "flame", "flash", "fluke", "prone"
]


def evaluate_guess(guess, answer):
    feedback = []
    for i in range(5):
        if guess[i] == answer[i]:
            feedback.append('O')  # Correct position
        elif guess[i] in answer:
            feedback.append('X')  # Wrong position
        else:
            feedback.append('-')  # Not in word
    return ''.join(feedback)

def get_next_guess(guess_history, evaluation_history):
    if not guess_history:
        return random.choice(word_list)

    possible_guesses = set(word_list)

    for guess, evaluation in zip(guess_history, evaluation_history):
        for i in range(5):
            if evaluation[i] == 'O':
                # Keep only words with the same letter at this position
                possible_guesses.intersection_update({word for word in possible_guesses if word[i] == guess[i]})
            elif evaluation[i] == 'X':
                # Keep only words that contain the letter, but not at this position
                possible_guesses.intersection_update({word for word in possible_guesses if guess[i] in word and word[i] != guess[i]})
            elif evaluation[i] == '-':
                # Remove words that contain this letter
                possible_guesses.difference_update({word for word in possible_guesses if guess[i] in word})

    return random.choice(list(possible_guesses)) if possible_guesses else random.choice(word_list)


@wordle_game_bp.route('/wordle-game', methods=['POST'])
def wordle_game():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    print("Received data:", data)  # Log the received data
    
    guess_history = data.get("guessHistory", [])
    evaluation_history = data.get("evaluationHistory", [])
    
    next_guess = get_next_guess(guess_history, evaluation_history)
    
    return jsonify({"guess": next_guess})
