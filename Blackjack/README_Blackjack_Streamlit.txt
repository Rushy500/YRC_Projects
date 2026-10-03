# Blackjack - Streamlit

## Run in Visual Studio Code

1. Install Python 3.10+.
2. Open this folder in Visual Studio Code.
3. Open Terminal -> New Terminal.
4. Install Streamlit:

   pip install -r requirements.txt

   Or:

   python -m pip install streamlit

5. Run the game:

   python -m streamlit run blackjack_streamlit.py

6. Streamlit will open the game in your browser.

## Run in Visual Studio

Visual Studio (the full IDE, not Visual Studio Code) can also run a Streamlit project.

1. Install Python development support in Visual Studio.
2. Open the folder/project containing `blackjack_streamlit.py`.
3. Open View -> Terminal.
4. Run:

   python -m pip install streamlit

5. Then run:

   python -m streamlit run blackjack_streamlit.py

6. Open the local address shown in the terminal, normally something like:

   http://localhost:8501

Important:
Do not normally use the regular Visual Studio "Start" / F5 button for a Streamlit app. Streamlit starts its own web server, so running the Streamlit command in the terminal is the simplest method.

## Main improvements

- Converted the terminal input/output game into a Streamlit web app.
- Added clickable HIT, STAND, and NEW GAME buttons.
- Added visual playing cards.
- Added hidden dealer card while the round is active.
- Added proper Ace scoring (11 or 1).
- Added Blackjack detection.
- Added dealer logic (dealer draws below 17).
- Added session state so the game does not reset after every button click.
- Removed `os.system('clear')`, which is not reliable across Windows and web apps.
- Kept the original Blackjack rules and overall game idea.
