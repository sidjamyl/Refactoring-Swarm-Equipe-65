from src.utils.state.stateDefinition import SwarmState

def decide_next_action(state: SwarmState) -> str:
        """Décide de la suite en fonction des tests."""
        tests_passed = state["tests_passed"]
        iteration = state["iteration_count"]
        max_iter = state["max_iterations"]
        
        if tests_passed:
            return "finish"
        elif iteration >= max_iter:
            print(f"\n⚠️  Limite d'itérations atteinte ({max_iter})")
            print(f"🏁 Fin du processus")
            return "finish"
        else:
            print(f"\n🔄 Nouvelle tentative... (Itération {iteration + 1}/{max_iter})")
            input("\n[Appuyez sur Entrée pour continuer...]\n")
            return "retry"