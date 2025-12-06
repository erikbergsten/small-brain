import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Tool():

    def __init__(self, param_class):
        self.param_class = param_class

    def get_name(self):
        return self.__class__.__name__ # TODO: fix case pascal->snake?

    def get_schema(self):
        return {
            "type": "function",
            "name": self.get_name(),
            "description": self.__class__.__doc__,
            "parameters": self.param_class.model_json_schema()
        }

    def get_json_schema(self, indent=None):
        return json.dumps(self.get_schema(), indent=indent)

    def log(self, args):
        logger.info(f"Calling {self.name}")

    async def run(self, tool_call):
        args = self.param_class.model_validate_json(tool_call.arguments)
        self.log(args)
        result = await self.execute(args)
        id = tool_call.call_id
        if result == None:
            result = "no return value"
        return {
            "type": "function_call_output",
            "call_id": id,
            "output": result
        }

    async def run_chat(self, tool_call):
        args = self.param_class.model_validate_json(tool_call.function.arguments)
        self.log(args)
        result = await self.execute(args)
        if result == None:
            result = "no return value"
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": json.dumps(result),
        }
