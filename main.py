import argparse
import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
import src.utils.agents.agentTest as agentTest
from src.utils.tools.pylintTool import run_pylint_on_file

load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Dossier {args.target_dir} introuvable.")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
    
    python_files = list(Path(args.target_dir).rglob("*.py"))
    if not python_files:
        print(f"❌ Aucun fichier .py trouvé dans {args.target_dir}")
        sys.exit(1)
    else:
        print(f"🔍 Fichiers .py trouvés : {[str(f) for f in python_files]}")

    for file_to_analyze in python_files:
        print(f"🔎 Fichier analysé par l'Auditor : {file_to_analyze}")
       
        messages = [
            SystemMessage(content=(
                "You are a code quality analyzer. You MUST use the run_pylint_on_file tool to analyze Python files.\n"
                "After calling the tool, respond ONLY with:\n"
                "1. The file name\n"
                "2. The exact pylint score from the tool output\n"
                "Example format:\n"
                "file.py - Score: 8.5/10"
            )),
            HumanMessage(content=f"Use the run_pylint_on_file tool to analyze: {file_to_analyze}")
        ]
        
        agent = agentTest.model.bind_tools([run_pylint_on_file])
        ai_msg = agent.invoke(messages)
        messages.append(ai_msg)

        # Execute tools and append ToolMessage objects
        for tool_call in ai_msg.tool_calls:
            tool_result = run_pylint_on_file.invoke(tool_call['args'])
            tool_msg = ToolMessage(  # [!code ++]
                content=str(tool_result),
                tool_call_id=tool_call['id']  # [!code ++]
            )
            messages.append(tool_msg)

        # Final model call with tool results
        final_response = agent.invoke(messages)
        
        print(f"📝 Rapport de l'agent: {final_response.content}")

    print("✅ MISSION_COMPLETE")

if __name__ == "__main__":
    main()