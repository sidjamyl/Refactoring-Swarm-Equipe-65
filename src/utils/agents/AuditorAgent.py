from langchain_core.messages import SystemMessage, HumanMessage
from src.utils.logger import log_experiment, ActionType
from src.utils.state.stateDefinition import SwarmState
from src.utils.agents import agentTest # Assure-toi que l'import match ton projet
from src.utils.prompts.promptAuditor import AUDITOR_SYSTEM_PROMPT

def auditor_agent_node(state: SwarmState) -> dict:

    """
    Agent Auditeur : Analyse la sortie brute de Pylint et génère un rapport structuré.
    """

   
    current_file = state["current_file"]
    raw_pylint_output = state["pylint_reports"][1]
    
    print(f"🕵️ [Auditor] Analyse du rapport Pylint pour : {current_file}")
    system_prompt = AUDITOR_SYSTEM_PROMPT

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
        print(f"✅ [Auditor] Plan de refactoring généré avec succès")
        print(f"\n{'='*60}")
        print("📋 PLAN DE REFACTORING:")
        print(f"{'='*60}")
        print(audit_content)
        print(f"{'='*60}\n")
    except Exception as e:
        audit_content = f"Error generating audit: {str(e)}"
        status = "FAILURE"
        print(f"❌ [Auditor] Erreur lors de la génération : {str(e)}")

    # 4. Logging de l'expérience
    
    log_experiment(
        agent_name="Auditor",
        model_used=agentTest.model.model,
        action=ActionType.ANALYSIS,
        details={
            "input_prompt": AUDITOR_SYSTEM_PROMPT + "\n" + user_prompt,
            "output_response": audit_content
        },
        status=status
    )


    
    return {
        "refactor_plan": [audit_content]
    }

    