from .base import schema
import json

class ToolBox:
    def __init__(self, tools):
        self.tools = {}
        for tool in tools:
            self.tools[tool.__name__] = tool

    def get_schemas(self):
        return list(map(lambda x: schema(x), self.tools.values()))

    def get_chat_declarations(self):
        declarations = []
        for tool in self.tools.values():
            tool_schema = schema(tool)
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

    def log(self, tool_call):
        tool_proto = self.tools[tool_call.name]
        args = json.loads(tool_call.arguments)
        tool = tool_proto.model_validate(args)
        tool.log()

    async def run(self, tool_call):
        tool_proto = self.tools[tool_call.name]
        args = json.loads(tool_call.arguments)
        tool = tool_proto.model_validate(args)
        id = tool_call.call_id
        result = await tool.run()
        return {
            "type": "function_call_output",
            "call_id": id,
            "output": result
        }

    async def run_chat(self, tool_call):
        """Run a tool given an OpenAI Chat Completions tool_call object."""
        name = tool_call.function.name
        args_json = tool_call.function.arguments
        tool_proto = self.tools[name]
        args = json.loads(args_json) if args_json else {}
        tool = tool_proto.model_validate(args)
        result = await tool.run()
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": name,
            "content": json.dumps(result),
        }
