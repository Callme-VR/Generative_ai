import asyncio
import streamlit as st
import os
from textwrap import dedent

from mcp_agent.app import MCPApp
from mcp_agent.workflows.llm.augmented_llm_google import GoogleAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm import RequestParams


# page configuration
st.page_config(
    page_title="Browser Control Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# title
st.title("Browser Control Agent")

# description
st.markdown("""
This is a simple browser control agent that can be used to control the browser.
""")

with st.sidebar:
    st.markdown("## Configuration")
    st.markdown("""
                Navigations
    """)
    st.markdown("**Interactions**")
    st.markdown("- click on mcp_ai_agents")
    st.markdown("- Scroll down to view more content")

    st.markdown("**Multi-step Tasks**")
    st.markdown(
        "- Navigate to github.com/Shubhamsaboo/awesome-llm-apps, scroll down, and report details")
    st.markdown("- Scroll down and summarize the github readme")

    st.markdown("---")
    st.caption("Note: The agent uses Playwright to control a real browser.")
