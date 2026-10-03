import random
import streamlit as st
import streamlit.components.v1 as components


# ---------------------------------------------------------
# Blackjack - Streamlit Version
# Based on the original terminal Blackjack program.
# ---------------------------------------------------------

st.set_page_config(
    page_title="Blackjack",
    page_icon="🃏",
    layout="centered"
)


# -----------------------------
# Deck and card functions
# -----------------------------

def create_deck():
    """Create and shuffle a standard 52-card deck."""
    suits = {
        "Spades": "♠",
        "Hearts": "♥",
        "Clubs": "♣",
        "Diamonds": "♦"
    }

    card_values = {
        "A": 11,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10
    }

    deck = []

    for suit_name, suit_symbol in suits.items():
        for rank, value in card_values.items():
            deck.append({
                "rank": rank,
                "value": value,
                "suit": suit_name,
                "symbol": suit_symbol
            })

    random.shuffle(deck)
    return deck


def deal_card():
    """Remove and return one card from the deck."""
    if not st.session_state.deck:
        return None

    return st.session_state.deck.pop()


def calculate_score(cards):
    """
    Calculate Blackjack score.

    Aces start as 11 and are changed to 1 when the
    total would otherwise be greater than 21.
    """
    score = sum(card["value"] for card in cards)
    aces = sum(1 for card in cards if card["rank"] == "A")

    while score > 21 and aces > 0:
        score -= 10
        aces -= 1

    return score


def is_blackjack(cards):
    """Return True if the hand is a natural Blackjack."""
    return len(cards) == 2 and calculate_score(cards) == 21


def card_html(card, hidden=False):
    """Create HTML for one playing card."""
    if hidden:
        return """
        <div class="playing-card hidden-card">
            <div class="card-back">🂠</div>
        </div>
        """

    rank = card["rank"]
    symbol = card["symbol"]
    suit_class = "red-card" if card["suit"] in ("Hearts", "Diamonds") else ""

    return f"""
    <div class="playing-card {suit_class}">
        <div class="card-top">{rank}{symbol}</div>
        <div class="card-center">{symbol}</div>
        <div class="card-bottom">{rank}{symbol}</div>
    </div>
    """


def display_cards(cards, hide_first=False):
    """Display every card as a visual playing card.

    Streamlit Markdown can sometimes interpret multi-line HTML as
    source code. Using components.html() gives the card HTML its own
    browser renderer, so every card is displayed correctly.
    """
    cards_html = ""

    for index, card in enumerate(cards):
        if hide_first and index == 0:
            cards_html += card_html(card, hidden=True)
        else:
            cards_html += card_html(card)

    html = f"""
    <style>
        body {{
            margin: 0;
            padding: 4px;
            background: transparent;
            font-family: Arial, sans-serif;
        }}

        .cards-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
            align-items: center;
        }}

        .playing-card {{
            width: 105px;
            height: 150px;
            border: 2px solid #222;
            border-radius: 12px;
            background: white;
            color: #111;
            padding: 8px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 3px 4px 9px rgba(0,0,0,.30);
            flex-shrink: 0;
        }}

        .red-card {{ color: #d00000; }}

        .card-top, .card-bottom {{
            font-size: 21px;
            font-weight: bold;
            line-height: 1;
        }}

        .card-top {{ text-align: left; }}
        .card-bottom {{ text-align: right; transform: rotate(180deg); }}

        .card-center {{
            font-size: 54px;
            text-align: center;
            line-height: 1;
        }}

        .hidden-card {{
            background: repeating-linear-gradient(45deg, #173b73, #173b73 8px, #244f91 8px, #244f91 16px);
            color: white;
            border-color: #0d2344;
        }}

        .hidden-card .card-back {{
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 55px;
        }}
    </style>

    <div class="cards-container">
        {cards_html}
    </div>
    """

    # Give the component enough room for a hand of cards.
    height = 180 if len(cards) <= 5 else 350
    components.html(html, height=height, scrolling=False)


# -----------------------------
# Game functions
# -----------------------------

def start_game():
    """Start or restart a Blackjack game."""
    st.session_state.deck = create_deck()

    # Deal alternating cards: Player, Dealer, Player, Dealer
    st.session_state.player_cards = []
    st.session_state.dealer_cards = []
    
    st.session_state.player_cards.append(deal_card())
    st.session_state.dealer_cards.append(deal_card())
    st.session_state.player_cards.append(deal_card())
    st.session_state.dealer_cards.append(deal_card())

    st.session_state.game_over = False
    st.session_state.player_stands = False
    st.session_state.result = ""
    st.session_state.message = ""


def dealer_play():
    """Let the dealer draw until reaching at least 17."""
    while calculate_score(st.session_state.dealer_cards) < 17:
        st.session_state.dealer_cards.append(deal_card())


def finish_game():
    """Compare player and dealer hands and determine the result."""
    player_score = calculate_score(st.session_state.player_cards)
    dealer_score = calculate_score(st.session_state.dealer_cards)

    if player_score > 21:
        st.session_state.result = "Dealer Wins"
        st.session_state.message = "💥 You busted!"
    elif dealer_score > 21:
        st.session_state.result = "You Win"
        st.session_state.message = "🎉 Dealer busted!"
    elif player_score > dealer_score:
        st.session_state.result = "You Win"
        st.session_state.message = "🎉 Your score is higher."
    elif player_score < dealer_score:
        st.session_state.result = "Dealer Wins"
        st.session_state.message = "Dealer has the higher score."
    else:
        st.session_state.result = "Tie"
        st.session_state.message = "🤝 It's a tie!"

    st.session_state.game_over = True


def check_initial_blackjack():
    """Check for Blackjack immediately after the initial deal."""
    player_blackjack = is_blackjack(st.session_state.player_cards)
    dealer_blackjack = is_blackjack(st.session_state.dealer_cards)

    if player_blackjack or dealer_blackjack:
        st.session_state.game_over = True

        if player_blackjack and dealer_blackjack:
            st.session_state.result = "Tie"
            st.session_state.message = "🤝 Both you and the dealer have Blackjack."
        elif player_blackjack:
            st.session_state.result = "You Win"
            st.session_state.message = "🃏 Blackjack! You win!"
        else:
            st.session_state.result = "Dealer Wins"
            st.session_state.message = "🃏 Dealer has Blackjack."


def hit():
    """Give the player another card."""
    if st.session_state.game_over:
        return

    new_card = deal_card()

    if new_card is not None:
        st.session_state.player_cards.append(new_card)

    player_score = calculate_score(st.session_state.player_cards)

    if player_score > 21:
        finish_game()
    elif player_score == 21:
        stand()


def double_down():
    """Player doubles down: receives exactly one more card, then automatically stands."""
    if st.session_state.game_over:
        return

    new_card = deal_card()
    
    if new_card is not None:
        st.session_state.player_cards.append(new_card)

    player_score = calculate_score(st.session_state.player_cards)

    if player_score > 21:
        finish_game()
    else:
        stand()


def stand():
    """Player stands; dealer plays according to Blackjack rules."""
    if st.session_state.game_over:
        return

    st.session_state.player_stands = True
    dealer_play()
    finish_game()


# -----------------------------
# Session-state initialization
# -----------------------------

if "deck" not in st.session_state:
    start_game()


# -----------------------------
# Page styling
# -----------------------------

st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            font-size: 18px;
            margin-bottom: 25px;
        }

        .cards-container {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin: 15px 0 25px 0;
        }

        .playing-card {
            width: 105px;
            height: 150px;
            border: 2px solid #222;
            border-radius: 12px;
            background: white;
            color: #111;
            padding: 8px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.25);
        }

        .red-card {
            color: #d11;
        }

        .card-top {
            font-size: 22px;
            font-weight: bold;
            text-align: left;
        }

        .card-center {
            font-size: 45px;
            text-align: center;
        }

        .card-bottom {
            font-size: 22px;
            font-weight: bold;
            text-align: right;
            transform: rotate(180deg);
        }

        .hidden-card {
            background: #222;
            color: white;
            border-color: #111;
        }

        .card-back {
            font-size: 65px;
            text-align: center;
            margin-top: 30px;
        }

        .result-box {
            padding: 18px;
            border-radius: 12px;
            text-align: center;
            border: 2px solid #555;
            margin: 15px 0;
        }

        .score {
            font-size: 22px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------

st.markdown('<div class="main-title">🃏 Blackjack</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Try to get as close to 21 as possible without going over.</div>',
    unsafe_allow_html=True
)


# -----------------------------
# New Game button
# -----------------------------

if st.button("🔄 New Game", use_container_width=True):
    start_game()
    st.rerun()


# -----------------------------
# Initial Blackjack check
# -----------------------------

if not st.session_state.game_over and len(st.session_state.player_cards) == 2:
    check_initial_blackjack()


# -----------------------------
# Dealer section
# -----------------------------

st.subheader("🎩 Dealer")

if st.session_state.game_over:
    display_cards(st.session_state.dealer_cards)
    dealer_score = calculate_score(st.session_state.dealer_cards)
    st.markdown(
        f'<div class="score">Dealer Score: {dealer_score}</div>',
        unsafe_allow_html=True
    )
else:
    # Hide the dealer's first card while the game is active.
    display_cards(st.session_state.dealer_cards, hide_first=True)

    visible_dealer_score = calculate_score(
        st.session_state.dealer_cards[1:]
    )

    st.markdown(
        f'<div class="score">Visible Dealer Score: {visible_dealer_score}</div>',
        unsafe_allow_html=True
    )


# -----------------------------
# Player section
# -----------------------------

st.subheader("👤 Player")

display_cards(st.session_state.player_cards)

player_score = calculate_score(st.session_state.player_cards)

st.markdown(
    f'<div class="score">Player Score: {player_score}</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Result section
# -----------------------------

if st.session_state.game_over:
    st.markdown(
        f"""
        <div class="result-box">
            <h2>{st.session_state.result}</h2>
            <p>{st.session_state.message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Click **New Game** to play another round.")

else:
    # -------------------------
    # Player controls
    # -------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🃏 HIT", use_container_width=True):
            hit()
            st.rerun()

    with col2:
        if st.button("✋ STAND", use_container_width=True):
            stand()
            st.rerun()
            
    with col3:
        if len(st.session_state.player_cards) == 2:
            if st.button("⏬ DOUBLE", use_container_width=True):
                double_down()
                st.rerun()


# -----------------------------
# Game information
# -----------------------------

with st.expander("ℹ️ How to Play"):
    st.write(
        """
        - **Hit:** Draw another card.
        - **Stand:** Keep your current score and let the dealer play.
        - **Double:** Take exactly one more card and automatically stand (available only on your first two cards).
        - Number cards are worth their number.
        - J, Q and K are worth 10.
        - Ace is worth 11 or 1, whichever is better for the hand.
        - The dealer must draw until their score is at least 17.
        - Going above 21 means you bust.
        """
    )

st.caption(f"Cards remaining in deck: {len(st.session_state.deck)}")