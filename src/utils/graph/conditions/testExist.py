from src.utils.state.stateDefinition import SwarmState

def check_tests_exist(state: SwarmState) -> dict:
    """Vérifie si des tests existent pour les fonctions listées."""
    function_list = state.get("function_list", [])
    functions_without_tests = state.get("function_without_tests", [])
    
    if not function_list:
        print("\n⚠️  Aucune fonction à vérifier")
        return "tests_do_not_exist"
    
    if not functions_without_tests:
        print("\n✅ Tests détectés pour toutes les fonctions")
        return "tests_exist"
    else:
       print(f"\n❌ {len(functions_without_tests)} fonction(s) sans tests : {', '.join(functions_without_tests)}")
       return "tests_do_not_exist"