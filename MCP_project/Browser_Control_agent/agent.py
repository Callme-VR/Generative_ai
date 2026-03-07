from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_google import GoogleAugmentedLLM
from mcp_agent.agents.agent import Agent
from mcp_agent.app import MCPApp
import os
from dotenv import load_dotenv
load_dotenv()


class BrowserAgent:

    def __init__(self):

        self.initialized = False

        self.mcp_app = MCPApp(
            name="MCPA_AGENT",
            description="Browser Control Agent"
        )

        self.mcp_context = None
        self.mcp_agent_app = None
        self.mcp_browser_agent = None
        self.llm = None

    async def setup_agent(self):

        if not self.initialized:

            try:

                self.mcp_context = self.mcp_app.run()
                self.mcp_agent_app = await self.mcp_context.__aenter__()

                # Browser Agent
                self.mcp_browser_agent = Agent(
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

                await self.mcp_browser_agent.initialize()

                self.llm = await self.mcp_browser_agent.attach_llm(
                    GoogleAugmentedLLM
                )

                logger = self.mcp_agent_app.logger

                tools = await self.mcp_browser_agent.list_tools()

                logger.info("Tools is Available", data=tools)

                self.initialized = True

            except Exception as e:
                raise Exception(f"Error during Agent Setup: {e}")

    async def run(self, message):

        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY is not set")

        await self.setup_agent()

        result = await self.llm.generate_str(
            message=message,
            request_params=RequestParams(
                use_history=True,
                maxTokens=10000,
            )
        )

        return result
