from langchain_core.messages import SystemMessage, HumanMessage
from src.utils.logger import log_experiment, ActionType
from src.utils.state.stateDefinition import SwarmState
from src.utils.agents import agentTest # Assure-toi que l'import match ton projet

def auditor_agent_node(state: SwarmState) -> dict:
    """
    Agent Auditeur : Analyse la sortie brute de Pylint et génère un rapport structuré.
    """
    
    # 1. Récupération des données du State (déposées par le noeud précédent 'pylint_tool_node')
    current_file = state["current_file"]
    raw_pylint_output = state["pylint_reports"][1]
    
    print(f"🕵️ [Auditor] Analyse du rapport Pylint pour : {current_file}")

    # 2. Construction du Prompt (Basé sur ton ancien script)
    # Note : On ne demande plus d'utiliser le tool, car le tool a DÉJÀ été exécuté juste avant.
    system_prompt = """You are the Auditor Agent in a 'Refactoring Swarm'.
Your goal is not just to report errors, but to create a detailed, executable **REFACTORING PLAN** for the Fixer Agent.

The Fixer Agent is blind to the Pylint output; it will relies ENTIRELY on your instructions to modify the code.

Analyze the provided Pylint output and generate a plan following these rules:
1. **Be Imperative**: Use action verbs (e.g., "Add docstring", "Rename variable", "Remove import").
2. **Be Specific**: Don't say "Fix style issues". Say "Rename variable 'X' to 'x_coord' at line 12".
3. **Cover All Issues**: Ensure every Pylint error/warning is addressed in the plan.

Format your response exactly as follows:

# REFACTORING PLAN FOR: {filename}
## SUMMARY
Current Pylint Score: X.XX/10
Primary Focus: [Documentation | Bug Fixes | Cleanup]

## ACTION ITEMS
1. [DOCS] (C0111) Add a module docstring at the top of the file describing its purpose.
2. [IMPORT] (W0611) Remove unused import 'sys'.
3. [NAMING] (C0103) Rename function 'run' to 'run_process' to be more descriptive.
4. [STYLE] (C0301) Break line 45 to respect the 80-character limit.
...

(List all necessary actions to reach a score of 10/10)"""

    user_prompt = f"Target File: {current_file}\n\nRAW PYLINT OUTPUT:\n{raw_pylint_output}"

    # 3. Appel du LLM
    llm = agentTest.model
    
    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        audit_content = response.content
        status = "SUCCESS"
    except Exception as e:
        audit_content = f"Error generating audit: {str(e)}"
        status = "FAILURE"

    
    return {
        "refactor_plan": [audit_content]
    }