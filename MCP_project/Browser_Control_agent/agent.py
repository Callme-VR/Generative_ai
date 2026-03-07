from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_google import GoogleAugmentedLLM
from mcp_agent.agents.agent import Agent
from mcp_agent.app import MCPApp
import os
import json
from dotenv import load_dotenv
load_dotenv()


class BrowserAgent:

    def __init__(self):

        self.initialized = False
        self.memory = []

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

            self.mcp_context = self.mcp_app.run()
            self.mcp_agent_app = await self.mcp_context.__aenter__()

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

            tools = await self.mcp_browser_agent.list_tools()

            logger = self.mcp_agent_app.logger
            logger.info("Tools is Available", data=tools)

            self.initialized = True

    async def plan(self, task):

        prompt = f"""
Break the following task into ordered browser steps.

Task:
{task}

Return JSON list of steps.
"""

        response = await self.llm.generate_str(
            message=prompt,
            request_params=RequestParams(max_tokens=1000)
        )

        try:
            # Clean up response if it contains markdown code blocks
            clean_response = response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
            steps = json.loads(clean_response.strip())
        except:
            steps = [task]

        return steps

    async def execute_step(self, step):

        result = await self.llm.generate_str(
            message=step,
            request_params=RequestParams(
                use_history=True,
                max_tokens=3000
            )
        )

        self.memory.append({
            "step": step,
            "result": result
        })

        return result

    async def run(self, task):

        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY is not set")

        await self.setup_agent()

        steps = await self.plan(task)

        results = []

        for step in steps:

            retry = 0
            success = False

            while retry < 2 and not success:

                try:

                    result = await self.execute_step(step)

                    results.append(result)
                    success = True

                except Exception:

                    retry += 1

        final_result = "\n\n".join(results)

        return final_result
