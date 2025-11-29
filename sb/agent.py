from .client import client
from .tools import ToolBox

async def stop():
    from .client import stop as client_stop
    await client_stop()

class Agent:
    def __init__(self, prompt, model="gpt-5.1", tools=[], log=print):
        self.model = model
        self.tools = ToolBox(tools)
        self.prompt = prompt
        self.reset()

    def reset(self):
        self.messages = [{"role": "system", "content": self.prompt}]

    async def query(self, message=None):
        if message is not None:
            self.messages.append({"role": "user", "content": message})
        res = await client.responses.create(
            input=self.messages,
            model=self.model,
            tools=self.tools.get_schemas(),
        )

        executed_tools = False
        for message in res.output:
            self.messages.append(message)
            if message.type == 'function_call':
                result = await self.tools.run(message)
                self.messages.append(result)
                executed_tools = True
            elif message.type == 'message':
                pass
            else:
                self.log(f"Unknown message type: {message.type}")

        if executed_tools:
            return await self.query()
        else:
            return res.output_text
