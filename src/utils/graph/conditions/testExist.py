from src.utils.state.stateDefinition import SwarmState

# Compteur de tentatives de génération de tests (par fichier)
_test_gen_attempts = {}

def check_tests_exist(state: SwarmState) -> str:
    """Vérifie si des tests existent pour les fonctions listées."""
    function_list = state.get("function_list", [])
    functions_without_tests = state.get("function_without_tests", [])
    current_file = str(state.get("current_file", ""))
    max_test_gen_retries = 2  # Maximum de tentatives de génération de tests
    
    if not function_list:
        print("\n⚠️  Aucune fonction détectée (code source invalide ?), passage au verdict")
        return "tests_exist"  # Pas de fonctions = rien à tester, on passe au Judge
    
    if not functions_without_tests:
        print("\n✅ Tests détectés pour toutes les fonctions")
        # Reset du compteur pour ce fichier
        _test_gen_attempts[current_file] = 0
        return "tests_exist"
    else:
        # Incrémenter le compteur de tentatives
        _test_gen_attempts[current_file] = _test_gen_attempts.get(current_file, 0) + 1
        attempts = _test_gen_attempts[current_file]
        
        print(f"\n❌ {len(functions_without_tests)} fonction(s) sans tests : {', '.join(functions_without_tests)}")
        
        if attempts > max_test_gen_retries:
            print(f"\n⚠️  Limite de {max_test_gen_retries} tentatives de génération atteinte, on continue sans tests complets.")
            _test_gen_attempts[current_file] = 0
            return "tests_exist"  # Forcer le passage au Judge
        
        print(f"🔄 Tentative de génération {attempts}/{max_test_gen_retries}")
        return "tests_do_not_exist"