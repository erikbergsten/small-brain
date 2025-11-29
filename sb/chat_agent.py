from .client import client
from .tools import ToolBox

async def stop():
    from .client import stop as client_stop
    await client_stop()


class ChatAgent:
    """Agent implementation that uses the Chat Completions API
    instead of the Responses API, mirroring the interface and
    behavior of Agent in agent.py."""

    def __init__(self, prompt, model="gpt-4.1", tools=[]):
        self.model = model
        self.tools = ToolBox(tools)
        self.prompt = prompt
        self.reset()

    def reset(self):
        self.messages = [{"role": "system", "content": self.prompt}]

    async def query(self, message=None):
        # Append user message if provided
        if message is not None:
            self.messages.append({"role": "user", "content": message})

        # Call chat completions API with tools
        tool_declarations = self.tools.get_chat_declarations()

        res = await client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=tool_declarations or None,
            tool_choice="auto" if tool_declarations else None,
        )

        choice = res.choices[0]
        msg = choice.message

        # Build assistant message to append to history
        assistant_message = {
            "role": msg.role,
            "content": msg.content,
        }

        # Only include tool_calls if there are any
        if msg.tool_calls:
            assistant_message["tool_calls"] = [
                tc.model_dump() for tc in msg.tool_calls
            ]

        self.messages.append(assistant_message)

        executed_tools = False

        # Handle tool calls
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                result_message = await self.tools.run_chat(tool_call)
                self.messages.append(result_message)
                executed_tools = True

        # If tools were executed, recursively query again so the model can use results
        if executed_tools:
            return await self.query()
        else:
            return msg.content
