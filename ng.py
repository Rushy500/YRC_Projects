import random
import json
import os
import streamlit as st

HISTORY_FILE = "player_history.json"

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                data = json.load(f)
                for player, record in data.items():
                    if isinstance(record, int):  
                        data[player] = {"wins": record, "losses": 0}
                return data
    except (json.JSONDecodeError, IOError):
        st.warning("Player history file is corrupted. Starting fresh.")
    return {}

def save_history(history):
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f)
    except IOError:
        st.error("Failed to save history. Please check file permissions.")

player_history = load_history()

st.title("Guess the Number Game!")
st.write("I am thinking of a number between 1 and 500. Can you guess it?")

name = st.text_input("Enter your name:", "", key="name_input")

if name:
    if name not in player_history or not isinstance(player_history[name], dict):
        player_history[name] = {"wins": 0, "losses": 0}

    if 'number' not in st.session_state:
        st.session_state.number = random.randint(1, 500)
    if 'guessesTaken' not in st.session_state:
        st.session_state.guessesTaken = 0

    guess = st.number_input("Enter your guess:", min_value=1, max_value=500, step=1, key="guess_input")

    if st.button("Submit Guess"):
        if st.session_state.guessesTaken >= 12:
            st.write(f"Game over! You've reached the maximum number of guesses. The number was {st.session_state.number}.")
            player_history[name]["losses"] += 1  
            save_history(player_history) 
            st.session_state.number = random.randint(1, 500)  
            st.session_state.guessesTaken = 0  
        else:
            st.session_state.guessesTaken += 1
            if guess < st.session_state.number:
                st.write("The guess is too low.")
            elif guess > st.session_state.number:
                st.write("The guess is too high.")
            else:
                st.write(f"Good job, {name}! You guessed the number in {st.session_state.guessesTaken} guesses!")
                player_history[name]["wins"] += 1  
                save_history(player_history)  
                st.session_state.number = random.randint(1, 500)  
                st.session_state.guessesTaken = 0  

    remaining_guesses = 12 - st.session_state.guessesTaken
    st.write(f"Guesses Taken: {st.session_state.guessesTaken}/12 (Remaining: {remaining_guesses})")

    if st.button("Show History"):
        st.write("Game History:")
        for player, record in player_history.items():
            st.write(f"{player}: {record['wins']} win(s), {record['losses']} loss(es)")

save_history(player_history)