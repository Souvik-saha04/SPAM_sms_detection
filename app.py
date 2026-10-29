import streamlit as st
from components.model_predictor import predict

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="🛡️",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Theme: dark charcoal, rounded cards, teal input, glowing blue button
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    :root {
        --bg: #1a1a1a;
        --card: #262833;
        --card-border: #3a3d4d;
        --text: #f1f3f8;
        --muted: #9aa0b4;
        --blue: #8ab4f8;
        --teal-bg: #173a3a;
        --teal-border: #2f6b66;
        --teal-text: #dffaf4;
        --lavender: #e6e6fa;
        --ink: #1f2230;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
        color: var(--text);
    }
    .stApp { background: var(--bg); }
    header[data-testid="stHeader"] { background: transparent; }
    header[data-testid="stHeader"] * { color: #cfd3dc !important; }
    #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 760px; padding-top: 3rem; padding-bottom: 3rem; }

    /* ---------- Header card ---------- */
    .app-header {
        max-width: 92%;
        margin: 0 auto 24px auto;
        background: var(--card);
        border: 1px solid var(--card-border);
        border-radius: 24px;
        padding: 22px 32px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }
    .app-header h1 {
        margin: 0 0 4px 0;
        padding: 0;
        font-size: 1.9rem;
        font-weight: 700;
        color: var(--blue);
    }
    .app-header p { margin: 0; color: var(--text); font-size: 1rem; }

    /* ---------- Main card (st.container with key="main_card") ---------- */
    .st-key-main_card {
        background: var(--card);
        border: 1px solid var(--card-border);
        border-radius: 28px;
        padding: 28px 32px 24px 32px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }
    .card-title { font-size: 1.25rem; font-weight: 700; margin: 0 0 12px 0; color: var(--text); }

    /* ---------- Text area ---------- */
    .stTextArea label { display: none; }
    div[data-baseweb="textarea"] {
        background: var(--teal-bg) !important;
        border: 1px solid var(--teal-border) !important;
        border-radius: 24px !important;
        overflow: hidden;
    }
    div[data-baseweb="textarea"] > div { background: transparent !important; }
    div[data-baseweb="textarea"] textarea {
        background: transparent !important;
        color: var(--teal-text) !important;
        font-family: 'Roboto', sans-serif;
        font-size: 1rem;
        padding: 16px 20px;
    }
    div[data-baseweb="textarea"] textarea::placeholder { color: #bfe3dc; opacity: 0.85; }
    div[data-baseweb="textarea"]:focus-within {
        border-color: #3fd3c4 !important;
        box-shadow: 0 0 0 3px rgba(63, 211, 196, 0.25);
    }

    [data-testid="stCaptionContainer"] { color: var(--blue); }

    /* ---------- Button ---------- */
    .stButton > button {
        border: none;
        border-radius: 999px;
        padding: 0.65rem 1.9rem;
        font-weight: 700;
        font-size: 1rem;
        color: #ffffff;
        background: linear-gradient(90deg, #2563ff 0%, #22d3c5 100%);
        box-shadow: 0 0 18px rgba(34, 211, 238, 0.55);
        transition: box-shadow 0.15s ease, transform 0.15s ease;
    }
    .stButton > button:hover {
        color: #ffffff;
        border: none;
        box-shadow: 0 0 26px rgba(34, 211, 238, 0.85);
        transform: translateY(-1px);
    }
    .stButton > button:active { transform: translateY(0); color: #ffffff; }
    .stButton > button:focus:not(:active) { color: #ffffff; border: none; }

    /* ---------- Result box ---------- */
    .result-box {
        border-radius: 20px;
        padding: 18px 22px;
        margin-top: 18px;
        color: var(--ink);
    }
    .result-box .r-label { font-weight: 700; margin: 0 0 4px 0; }
    .result-box .r-text  { margin: 0; }
    .result-box.empty { background: var(--lavender); border: 2px dashed #8c8fb8; }
    .result-box.ham   { background: #d8f5e6; border: 2px solid #3cb878; }
    .result-box.spam  { background: #fde1e1; border: 2px solid #e05a5a; }
    .result-box.ham  .r-label { color: #146c43; }
    .result-box.spam .r-label { color: #a32424; }

    /* ---------- Confidence bars ---------- */
    .conf { margin-top: 18px; }
    .conf-row { margin-bottom: 12px; }
    .conf-head {
        display: flex;
        justify-content: space-between;
        font-size: 0.95rem;
        margin-bottom: 6px;
        color: var(--text);
    }
    .conf-track { height: 12px; border-radius: 999px; background: #1a1c25; overflow: hidden; }
    .conf-fill-ham  { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #22d3c5, #3cb878); }
    .conf-fill-spam { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #f59e0b, #ef4444); }

    .foot { color: var(--muted); font-size: 0.78rem; margin-top: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <h1>SMS Spam Detector</h1>
        <p>Paste a text message and check whether it is spam or a normal message.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Main card
# ---------------------------------------------------------------------------
with st.container(key="main_card"):
    st.markdown('<p class="card-title">Message</p>', unsafe_allow_html=True)

    text = st.text_area(
        "Message",
        placeholder=(
            "Paste the full text of the SMS you want to check.\n"
            "E.g., Congrats! You won a gift card. Click the link to claim."
        ),
        height=150,
        label_visibility="collapsed",
    )
    st.caption(f"{len(text)} characters")

    analyze = st.button("Analyze message")

    if not analyze:
        st.markdown(
            """
            <div class="result-box empty">
                <p class="r-label">Result:</p>
                <p class="r-text">No result yet. Enter a message and select Analyze message.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif not text.strip():
        st.markdown(
            """
            <div class="result-box empty">
                <p class="r-label">Nothing to analyze:</p>
                <p class="r-text">Enter a message above, then select Analyze message.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        with st.spinner("Analyzing message..."):
            predic, prob = predict(text=text)

        ham_pct = float(prob[0][0]) * 100
        spam_pct = float(prob[0][1]) * 100

        if predic == 0:
            st.markdown(
                """
                <div class="result-box ham">
                    <p class="r-label">Ham message</p>
                    <p class="r-text">This looks like a normal message.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="result-box spam">
                    <p class="r-label">Spam message</p>
                    <p class="r-text">Do not click links or reply with personal details.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="conf">
                <div class="conf-row">
                    <div class="conf-head"><span>Ham</span><span>{ham_pct:.2f}%</span></div>
                    <div class="conf-track"><div class="conf-fill-ham" style="width:{ham_pct:.2f}%"></div></div>
                </div>
                <div class="conf-row">
                    <div class="conf-head"><span>Spam</span><span>{spam_pct:.2f}%</span></div>
                    <div class="conf-track"><div class="conf-fill-spam" style="width:{spam_pct:.2f}%"></div></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<p class="foot">Predictions come from a trained model and can be wrong. '
        "Treat unexpected links with caution either way.</p>",
        unsafe_allow_html=True,
    )