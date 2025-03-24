import random

def mad_libs():
    print("Welcome to the Mad Libs Game!\n")

    while True:
        adjective = input("Enter an adjective: ").strip()
        noun = input("Enter a noun: ").strip()
        verb = input("Enter a verb: ").strip()
        adverb = input("Enter an adverb: ").strip()
        place = input("Enter a place: ").strip()
        emotion = input("Enter an emotion: ").strip()

        if not all([adjective, noun, verb, adverb, place, emotion]):
            print("\nPlease fill in all the fields!\n")
            continue

        stories = [
            f"Once upon a time, there was a {adjective} {noun} that loved to {verb} {adverb}.",
            f"One day, a {adjective} {noun} went to {place} and felt very {emotion}.",
            f"In a {adjective} world, a {noun} decided to {verb} {adverb} near {place}.",
            f"A {noun} who was very {adjective} tried to {verb} {adverb} but ended up in {place}, feeling {emotion}."
        ]

        story = random.choice(stories)

        print("\nHere is your story:")
        print(story)

        play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            print("\nThanks for playing! Goodbye.")
            break

mad_libs()
