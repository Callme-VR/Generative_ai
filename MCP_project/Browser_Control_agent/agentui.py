import asyncio
import streamlit as st

from agent import BrowserAgent
from dotenv import load_dotenv
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Browser Control Agent",
    page_icon="🌐",
    layout="wide"
)


# Header
st.title("🌐 Browser Control Agent")

st.markdown(
    """
Control a real browser using **AI + MCP + Playwright**.
"""
)


# Sidebar
with st.sidebar:

    st.header("Examples")

    st.markdown("""
**Navigation**

Go to github.com  
Open google.com  

**Interactions**

Click on mcp_ai_agents  
Scroll down to view content  

**Multi Step Tasks**

Navigate to github.com/Shubhamsaboo/awesome-llm-apps  
Scroll down and summarize the page
""")


# User Input
query = st.text_area(
    "Your Instruction to Control Browser",
    placeholder="Example: Go to github.com and summarize the page",
    height=120
)


# Session State
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


# Run Button
st.button(
    "🚀 Run Command",
    use_container_width=True,
    type="primary",
    disabled=st.session_state.running,
    on_click=start_run
)


# Execute Agent
if st.session_state.running:

    with st.spinner("Agent controlling browser..."):

        result = st.session_state.loop.run_until_complete(
            st.session_state.agent.run(query)
        )

    st.session_state.result = result
    st.session_state.running = False
    st.rerun()


# Response Display
if st.session_state.result:

    st.subheader("Response")

    st.markdown(st.session_state.result)


# Footer
st.markdown("---")
st.caption("Built with Streamlit • MCP-Agent • Playwright")
