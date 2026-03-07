import asyncio
import streamlit as st
import os
from textwrap import dedent

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_google import GoogleAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm import RequestParams

# Page configuration
st.set_page_config(
    page_title="Browser Control Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title("Browser Control Agent")

# Description
st.markdown("""
This is a simple browser control agent that can be used to control the browser using MCP.
""")

with st.sidebar:
    st.markdown("## Configuration")
    st.markdown("""
                ### Navigations
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

query = st.text_area(
    "Your Instruction to Control Browser",
    placeholder="Enter your instruction here"
)

# Initialize the app and agent that can control your browser
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.mcp_app = MCPApp(
        name="MCPA_AGENT", description="Browser Control Agent")
    st.session_state.mcp_context = None
    st.session_state.mcp_agent = None
    st.session_state.mcp_workflow = None
    st.session_state.mcp_browser_agent = None
    st.session_state.llm = None


async def setup_agent():
    if not st.session_state.initialized:
        try:
            st.session_state.mcp_context = st.session_state.mcp_app.run()
            st.session_state.mcp_agent_app = await st.session_state.mcp_context.__aenter__()

            # create and initialized the agent
            st.session_state.mcp_browser_agent = Agent(
                name="Browser Agent",
                instruction="""
                you are helpful web browsing assistant that can interact with websites using playwright
                -Navigate to websites and perform browser actions like (click,scroll,enter,exit,type)
                -extract information from websites and web pages
                -take screenshots of websites and web pages
                -provide concise summaries of web content using markdown format
                -follow the instruction sequences to complete tasks
                
                Respond back with status code updates completing the command and execution of instructions
                """,
                server_names=["playwright"],
            )

            st.session_state.initialized = True

        except Exception as e:
            raise e
