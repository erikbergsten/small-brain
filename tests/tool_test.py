from sb.tools import Tool
from pydantic import BaseModel

class GreeterArgs(BaseModel):
    message: str

class Greeter(Tool):
    """a tool for friendly greetings"""
    def __init__(self):
        super().__init__(GreeterArgs)
        self.calls = 0

    async def execute(self, args):
        print("Greeting:", args.message)

my_greeter = Greeter()

if __name__ == '__main__':
    from sb import Agent, ChatAgent, stop
    import asyncio
    agent = Agent("You are a helpful assistant.", tools=[my_greeter])

    result = asyncio.run(agent.query("greet the world!"))
    print("got:", agent.messages)
    asyncio.run(stop())
