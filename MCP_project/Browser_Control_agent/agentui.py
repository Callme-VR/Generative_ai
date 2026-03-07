import asyncio
import streamlit as st

from agent import BrowserAgent
from dotenv import load_dotenv
load_dotenv()


st.set_page_config(
    page_title="Autonomous Browser Agent",
    page_icon="🌐",
    layout="wide"
)


st.title("🌐 Autonomous Browser Agent")

st.markdown(
    """
AI agent that can **plan tasks, control a browser, and execute multi-step actions automatically**.
"""
)


with st.sidebar:

    st.header("Example Tasks")

    st.markdown("""
Open github.com and summarize the homepage

Go to wikipedia.org and search Artificial Intelligence

Navigate to github.com/Shubhamsaboo/awesome-llm-apps and explain the project
""")


query = st.text_area(
    "Task",
    placeholder="Example: Open github.com and summarize the homepage",
    height=120
)


if "agent" not in st.session_state:
    st.session_state.agent = BrowserAgent()

if "loop" not in st.session_state:
    st.session_state.loop = asyncio.new_event_loop()

if "result" not in st.session_state:
    st.session_state.result = None

if "running" not in st.session_state:
    st.session_state.running = False


def start_run():
    st.session_state.running = True


st.button(
    "🚀 Run Autonomous Task",
    use_container_width=True,
    type="primary",
    disabled=st.session_state.running,
    on_click=start_run
)


if st.session_state.running:

    with st.spinner("Agent planning and controlling browser..."):

        result = st.session_state.loop.run_until_complete(
            st.session_state.agent.run(query)
        )

    st.session_state.result = result
    st.session_state.running = False
    st.rerun()


if st.session_state.result:

    st.subheader("Agent Result")

    st.markdown(st.session_state.result)


st.markdown("---")
st.caption("Powered by MCP • Playwright • Google LLM")
