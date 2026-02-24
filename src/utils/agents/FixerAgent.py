import src.utils.state.stateDefinition as SwarmState
from src.utils.agents import agentTest
from src.utils.prompts.promptFixer import SYSTEM_PROMPT_FIXER,USER_PROMPT_FIXER
from langchain_core.messages import SystemMessage, HumanMessage
from src.utils.logger import log_experiment, ActionType
from src.utils.agents import agentTest


def fixer_agent_node(state: SwarmState) -> dict:
    """Agent qui génère le code refactorisé."""
    refactor_plan = state["refactor_plan"]
    original_code = state["original_code"]
    current_file = state["current_file"]
    
    # Récupérer l'itération actuelle
    iteration = state["iteration_count"]
    test_analysis = state["test_analysis"]
    refactored_code = state.get("refactored_code", "")

    function_without_tests = state.get("functions_without_tests", [])
    function_list = state.get("function_list", [])
    
    print(f"\n{'─'*80}")
    print(f"🔧 ÉTAPE 4/6 : GÉNÉRATION DU CODE REFACTORISÉ")
    print(f"{'─'*80}")
    print(f"\n🔄 Itération n°{iteration + 1}")
    
    # === SI C'EST UNE CORRECTION (itération > 0) ===
    if iteration > 0 and test_analysis:
        print(f"⚠️  Mode : CORRECTION (basée sur les retours des tests)")
        user_prompt = f"""CORRECTION BASÉE SUR LES TESTS

CODE ACTUEL:
{refactored_code}

FEEDBACK DES TESTS:
{test_analysis}

PLAN DE REFACTORING ORIGINAL:
{refactor_plan}

Corrige le code en tenant compte du feedback des tests.
Garde les améliorations précédentes et corrige uniquement les erreurs détectées.
Retourne UNIQUEMENT le code Python corrigé, sans explications."""
    
    # === SINON, PREMIÈRE GÉNÉRATION ===
    else:
        print(f"✨ [Fixer] Première génération du code refactorisé")
        user_prompt = USER_PROMPT_FIXER + f"\n\n{original_code}\n\nRefactor Plan:\n{refactor_plan}"
    
    # Construire les messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_FIXER},
        {"role": "user", "content": user_prompt}
    ]
    
    # Appeler le LLM
    try:
        response = agentTest.model.invoke(messages)
        refactored_code = response.content
        status = "SUCCESS"
        
        print(f"\n✅ Code refactorisé généré")
        print(f"📊 Taille : {len(refactored_code)} caractères")
        
        input("\n[Appuyez sur Entrée pour écrire le code refactorisé...]")
    except Exception as e:
        refactored_code = f"Error generating refactored code: {str(e)}"
        status = "FAILURE"
        print(f"❌ [Fixer] Erreur lors de la génération : {str(e)}")
    
    # Logging de l'expérience
    action_type = ActionType.FIX if iteration > 0 else ActionType.GENERATION
    log_experiment(
        agent_name="Fixer",
        model_used=agentTest.model.model,
        action=action_type,
        details={
            "input_prompt": SYSTEM_PROMPT_FIXER + "\n" + user_prompt,
            "output_response": refactored_code
        },
        status=status
    )
    
    function_without_tests= []
    function_list= []

    return {
        "refactored_code": refactored_code,
        "iteration_count": iteration + 1,
        "status": "CODE_REFACTORED",
        "function_list": function_list,
        "function_without_tests": function_without_tests
       
    }
