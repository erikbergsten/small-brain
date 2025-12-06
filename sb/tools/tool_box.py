import json

class ToolBox:
    def __init__(self, tools):
        self.tools = {}
        for tool in tools:
            self.tools[tool.name] = tool

    def get_schemas(self):
        return list(map(lambda x: x.get_schema(), self.tools.values()))

    def get_chat_declarations(self):
        declarations = []
        for tool in self.tools.values():
            tool_schema = tool.get_schema()
            parameters = tool_schema.get("parameters", {})
            parameters['additionalProperties'] = False
            declaration = {
                "type": "function",
                "function": {
                    "name": tool_schema["name"],
                    "description": tool_schema.get("description", ""),
                    "parameters": parameters,
                    "strict": True,
                },
            }
            declarations.append(declaration)
        return declarations

    async def run(self, tool_call):
        """Run a tool given an OpenAI Responses tool_call object."""
        tool = self.tools[tool_call.name]
        result = await tool.run(tool_call)
        return result

    async def run_chat(self, tool_call):
        """Run a tool given an OpenAI Chat Completions tool_call object."""
        tool = self.tools[tool_call.function.name]
        result = await tool.run_chat(tool_call)
        return result
