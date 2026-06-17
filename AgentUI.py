from urllib.parse import urlparse

import streamlit as st

from Youtube_analyzer import youtube_agent


st.set_page_config(
    page_title="  YouTube Video Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
        :root {
            --page: #020711;
            --surface: rgba(8, 16, 30, 0.82);
            --surface-soft: rgba(15, 27, 47, 0.88);
            --ink: #edf7ff;
            --muted: #a9bfd2;
            --accent: #8bd3ff;
            --accent-strong: #cfefff;
            --line: rgba(139, 211, 255, 0.22);
        }

        .block-container {
            max-width: 1180px;
            padding-top: 3.25rem;
            padding-bottom: 3rem;
        }

        html, body, [class*="css"] {
            font-family: Twklausanne, Tahoma, Verdana, Arial, sans-serif;
        }

        div[data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 50% 12%, rgba(75, 176, 255, 0.20), transparent 22rem),
                radial-gradient(circle at 18% 80%, rgba(59, 130, 246, 0.12), transparent 18rem),
                linear-gradient(180deg, #020711 0%, #050b16 52%, #020711 100%);
            color: var(--ink);
        }

        header[data-testid="stHeader"] {
            background: rgba(2, 7, 17, 0.92);
            border-bottom: 1px solid var(--line);
        }

        .app-shell {
            border: 1px solid var(--line);
            background: linear-gradient(180deg, rgba(5, 12, 24, 0.90), rgba(3, 8, 18, 0.78));
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 28px 90px rgba(0, 0, 0, 0.36);
            backdrop-filter: blur(14px);
        }

        .hero {
            text-align: center;
            padding: 2rem 0 2.25rem;
            border-bottom: 1px solid var(--line);
        }

        .hero h1 {
            color: var(--accent);
            font-size: clamp(2rem, 5.2vw, 4.05rem);
            line-height: 1.03;
            letter-spacing: 0;
            margin: 0;
            font-family: Twklausanne, Tahoma, Verdana, Arial, sans-serif;
            font-weight: 500;
            text-shadow: 0 0 28px rgba(139, 211, 255, 0.42);
        }

        .hero p {
            color: var(--accent-strong);
            font-size: 1.08rem;
            margin: 1.2rem auto 0;
            max-width: 720px;
            font-weight: 650;
        }

        .status-pill {
            display: inline-block;
            border: 1px solid var(--line);
            background: rgba(139, 211, 255, 0.08);
             color: var(--accent-strong);
            border-radius: 8px;
            padding: 0.7rem 1rem;
            font-size: 0.88rem;
            font-weight: 800;
            margin-top: 1.4rem;
        }

        .section-title {
            color: var(--ink);
            font-size: 1.02rem;
            font-weight: 800;
            margin: 0 0 0.4rem;
        }

        .muted {
            color: var(--muted);
            font-size: 0.92rem;
            margin: 0 0 1rem;
        }

        .metric-row {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
            margin-top: 1rem;
        }

        .metric {
            background: var(--surface-soft);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem;
        }

        .metric strong {
            display: block;
            color: var(--ink);
            font-size: 0.95rem;
        }

        .metric span {
            color: var(--muted);
            font-size: 0.82rem;
        }

        div[data-testid="column"] {
            padding-top: 1.4rem;
        }

        div[data-testid="stTextInput"] input {
            border-radius: 8px;
            min-height: 3rem;
            background: rgba(2, 7, 17, 0.88);
            border: 1px solid var(--line);
            color: var(--ink);
            font-weight: 650;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 0.16rem rgba(139, 211, 255, 0.18);
        }

        textarea {
            background: rgba(2, 7, 17, 0.88) !important;
            border: 1px solid var(--line) !important;
            color: var(--ink) !important;
            border-radius: 8px !important;
            font-family: "Cascadia Code", Consolas, monospace !important;
        }

        div[data-testid="stButton"] button,
        div[data-testid="stFormSubmitButton"] button,
        div[data-testid="stDownloadButton"] button {
            border-radius: 8px;
            min-height: 3rem;
            font-weight: 800;
        }

        div[data-testid="stButton"] button,
        div[data-testid="stFormSubmitButton"] button {
            background: #e7f5ff;
            color: #020711 !important;
            border: 1px solid var(--accent);
            box-shadow: 0 0 30px rgba(139, 211, 255, 0.12);
        }

        div[data-testid="stButton"] button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {
            background: var(--accent);
            border-color: var(--accent);
            color: #020711 !important;
            box-shadow: 0 0 34px rgba(139, 211, 255, 0.34);
        }

        div[data-testid="stButton"] button *,
        div[data-testid="stFormSubmitButton"] button * {
            color: #020711 !important;
        }

        div[data-testid="stDownloadButton"] button {
            background: transparent;
            color: var(--accent-strong);
            border: 1px solid var(--line);
        }

        div[data-testid="stDownloadButton"] button:hover {
            background: rgba(139, 211, 255, 0.10);
            color: var(--ink);
            border-color: var(--accent);
        }

        .result-frame {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: rgba(2, 7, 17, 0.76);
            padding: 1.25rem;
        }

        div[data-testid="stExpander"] {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: rgba(139, 211, 255, 0.05);
        }

        div[data-testid="stExpander"] summary {
            color: var(--ink);
            font-weight: 750;
        }

        div[data-testid="stCodeBlock"] {
            border: 1px solid var(--line);
            border-radius: 8px;
        }

        hr {
            border-color: var(--line);
            margin: 1.6rem 0;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.35rem;
            border-bottom: 1px solid var(--line);
        }

        .stTabs [data-baseweb="tab"] {
            color: var(--muted);
            font-weight: 750;
        }

        .stTabs [aria-selected="true"] {
            color: var(--accent) !important;
        }

        div[data-testid="stAlert"] {
            background: rgba(139, 211, 255, 0.08);
            color: var(--ink);
            border: 1px solid var(--line);
        }

        .stMarkdown, .stText, p, li, label {
            color: var(--muted);
        }

        h1, h2, h3, h4, strong {
            color: var(--ink);
        }

        @media (max-width: 760px) {
            .hero {
                display: block;
                text-align: left;
            }

            .status-pill {
                display: inline-block;
                margin-top: 1rem;
            }

            .metric-row {
                grid-template-columns: 1fr;
            }

            .app-shell {
                padding: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def get_agent():
    return youtube_agent()


def is_youtube_url(value: str) -> bool:
    if not value:
        return False

    parsed = urlparse(value.strip())
    host = parsed.netloc.lower().removeprefix("www.")
    return parsed.scheme in {"http", "https"} and host in {
        "youtube.com",
        "youtu.be",
        "m.youtube.com",
        "music.youtube.com",
    }


def run_analysis(video_url: str):
    agent = get_agent()
    return agent.run(f"Analyze this video {video_url}")


if "report" not in st.session_state:
    st.session_state.report = ""
if "last_url" not in st.session_state:
    st.session_state.last_url = ""


st.markdown('<div class="app-shell">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="hero">
        <div>
            <h1>YouTube Video Analyzer</h1>
            <p>
                Turn long videos into a structured briefing with overview,
                timestamps, key moments, learning points, and practical notes.
            </p>
        </div>
        <div class="status-pill">Agent powered analysis</div>
    </div>
    """,
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([1.6, 1], gap="large")

with left_col:
    st.markdown('<p class="section-title">Analyze a video</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="muted">Paste a public YouTube URL and the agent will build a readable report.</p>',
        unsafe_allow_html=True,
    )

    with st.form("analysis_form", clear_on_submit=False):
        video_url = st.text_input(
            "YouTube video URL",
            value=st.session_state.last_url,
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Analyze Video", use_container_width=True)

    if submitted:
        clean_url = video_url.strip()

        if not is_youtube_url(clean_url):
            st.error("Please enter a valid YouTube link before running the analysis.")
        else:
            st.session_state.last_url = clean_url
            with st.spinner("Watching the video context and building the report..."):
                response = run_analysis(clean_url)
                st.session_state.report = response.content

with right_col:
    st.markdown('<p class="section-title">What you will get</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="metric-row">
            <div class="metric">
                <strong>Overview</strong>
                <span>Video type, structure, and context.</span>
            </div>
            <div class="metric">
                <strong>Timestamps</strong>
                <span>Topic shifts and notable moments.</span>
            </div>
            <div class="metric">
                <strong>Insights</strong>
                <span>Learning points and references.</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Example links to try"):
        st.code("https://www.youtube.com/watch?v=LPZh9BOjkQs", language="text")
        st.code("https://youtu.be/LPZh9BOjkQs", language="text")

st.divider()

if st.session_state.report:
    st.markdown('<p class="section-title">Analysis report</p>', unsafe_allow_html=True)

    report_tab, source_tab = st.tabs(["Formatted Report", "Source"])
    with report_tab:
        st.markdown('<div class="result-frame">', unsafe_allow_html=True)
        st.markdown(st.session_state.report)
        st.markdown("</div>", unsafe_allow_html=True)

    with source_tab:
        st.text_area(
            "Markdown report",
            st.session_state.report,
            height=420,
            label_visibility="collapsed",
        )

    st.download_button(
        "Download Report",
        data=st.session_state.report,
        file_name="youtube_analysis_report.md",
        mime="text/markdown",
        use_container_width=True,
    )
elif not submitted:
    st.info("Paste a YouTube link above to generate your first report.")

st.markdown("</div>", unsafe_allow_html=True)
