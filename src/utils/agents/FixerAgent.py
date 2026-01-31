

import src.utils.state.stateDefinition as SwarmState
from src.utils.agents import agentTest
from src.utils.prompts.promptFixer import SYSTEM_PROMPT_FIXER,USER_PROMPT_FIXER
from langchain_core.messages import SystemMessage, HumanMessage
from src.utils.logger import log_experiment, ActionType



def fixer_agent_node(state : SwarmState.SwarmState) -> dict:
    """
    Agent Fixer qui lit le code original, applique les modifications et met à jour l'état.
    """
    current_file = state["current_file"]
    print(f"🔧 [Fixer] Génération du code refactorisé pour : {current_file}")
    
    # Lire le code original
    original_code = state["original_code"]
    refactor_plan = state["refactor_plan"]

    system_prompt = SYSTEM_PROMPT_FIXER
    user_prompt = USER_PROMPT_FIXER + f"\n\n{original_code}\n\nRefactor Plan:\n{refactor_plan}"

    llm = agentTest.model

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        refactored_code = response.content
        status = "SUCCESS"
        print(f"✅ [Fixer] Code refactorisé généré avec succès")
        print(f"\n{'='*60}")
        print("🔧 CODE REFACTORISÉ:")
        print(f"{'='*60}")
        print(refactored_code)
        print(f"{'='*60}\n")
    except Exception as e:
        refactored_code = f"Error generating audit: {str(e)}"
        status = "FAILURE"
        print(f"❌ [Fixer] Erreur lors de la génération : {str(e)}")

    # Logging de l'expérience
    log_experiment(
        agent_name="Fixer",
        model_used=agentTest.model.model,
        action=ActionType.FIX,
        details={
            "input_prompt": SYSTEM_PROMPT_FIXER + "\n" + user_prompt,
            "output_response": refactored_code
        },
        status=status
    )



    return {
        "refactored_code": refactored_code
    }

    
