
from langchain_mistralai.chat_models import ChatMistralAI
from dotenv import load_dotenv
import getpass
import os
from src.utils.tools.pylintTool import run_pylint_on_file
import src.utils.tools.pylintTool as pylintTool


load_dotenv()

if "MISTRAL_API_KEY" not in os.environ:
    os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter your Mistral API key: ")

model = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.1,
)
