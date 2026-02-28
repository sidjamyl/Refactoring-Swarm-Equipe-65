
from src.utils.state.stateDefinition import SwarmState
from src.utils.prompts.promptJudge import SYSTEM_PROMPT_JUDGE, USER_PROMPT_JUDGE
import src.utils.agents.agentTest as agentTest
from src.utils.logger import log_experiment, ActionType
# Initialiser le modèle


def judge_agent_node(state: SwarmState) -> dict:
    """Analyse les résultats des tests et génère un verdict."""
    raw_output = state["raw_test_output"]
    exit_code = state["test_exit_code"]
    
    
    
    # Si exit_code = 0, tests réussis
    if exit_code == 0:
        print(f"\n{'─'*80}")
        print(f"⚖️  ÉTAPE 6/6 : VERDICT FINAL")
        print(f"{'─'*80}")
        print(f"\n{'╔'+'═'*78+'╗'}")
        print(f"║{' '*20}✅ TOUS LES TESTS SONT RÉUSSIS{' '*19}║")
        print(f"{'╚'+'═'*78+'╝'}")
        print(f"\n🎉 Code de retour : {exit_code} (Succès)")
        
        # Logging de l'expérience (pas d'appel LLM mais on enregistre la décision)
        log_experiment(
            agent_name="Judge",
            model_used="rule-based",  # Pas de LLM pour exit_code = 0
            action=ActionType.DEBUG,
            details={
                "input_prompt": f"Exit code: {exit_code}\nOutput: {raw_output}",
                "output_response": "Tous les tests passent avec succès."
            },
            status="SUCCESS"
        )
        
        return {
            "tests_passed": True,
            "test_analysis": "Tous les tests passent avec succès.",
            "status": "TESTS_PASSED",
            "refactor_finished": True
        }
    
    # Sinon, analyser avec le LLM
    user_prompt = USER_PROMPT_JUDGE.format(
        exit_code=exit_code,
        output=raw_output
    )
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_JUDGE},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        response = agentTest.model.invoke(messages)
        analysis = response.content
        status = "SUCCESS"
        
        print(f"\n{'─'*80}")
        print(f"⚖️  ÉTAPE 6/6 : VERDICT FINAL")
        print(f"{'─'*80}")
        
        # Parser le verdict
        tests_passed = "VERDICT: PASS" in analysis
        
        if tests_passed:
            print(f"\n{'╔'+'═'*78+'╗'}")
            print(f"║{' '*28}✅ TESTS RÉUSSIS{' '*28}║")
            print(f"{'╚'+'═'*78+'╝'}")
        else:
            print(f"\n{'╔'+'═'*78+'╗'}")
            print(f"║{' '*26}❌ TESTS EN ÉCHEC{' '*27}║")
            print(f"{'╚'+'═'*78+'╝'}")
            print(f"\n📋 Analyse (extrait) :")
            print(f"{analysis[:5000]}...")
            
        # input("\n[Appuyez sur Entrée pour continuer...]")
    except Exception as e:
        analysis = f"Error analyzing tests: {str(e)}"
        tests_passed = False
        status = "FAILURE"
        print(f"❌ [Judge] Erreur lors de l'analyse : {str(e)}")
    
    # Logging de l'expérience
    log_experiment(
        agent_name="Judge",
        model_used=agentTest.model.model,
        action=ActionType.DEBUG,
        details={
            "input_prompt": SYSTEM_PROMPT_JUDGE + "\n" + user_prompt,
            "output_response": analysis
        },
        status=status
    )
    
    return {
        "tests_passed": tests_passed,
        "test_analysis": analysis,
        "status": "TESTS_ANALYZED",
        "refactor_finished": tests_passed
    }