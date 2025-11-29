from pydantic import BaseModel
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Tool(BaseModel):

    def get_name(self):
        return self.__class__.__name__ # TODO: fix case pascal->snake?

    def get_schema(self):
        return {
            "type": "function",
            "name": self.get_name(),
            "description": self._description,
            "parameters": self.model_json_schema()
        }

    def get_json_schema(self, indent=None):
        return json.dumps(self.get_schema(), indent=indent)

    def log(self):
        if hasattr(self, 'log_message'):
            logger.info(f"Calling {self.get_name()} with { self.log_message() }")
        else:
            logger.info(f"Calling {self.get_name()}")

    async def run(self):
        self.log()
        return await self.execute()

def schema(tool):
    return tool.model_construct().get_schema()
