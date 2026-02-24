import subprocess
from pathlib import Path
from src.utils.state.stateDefinition import SwarmState

def run_pytest_tool(state: SwarmState) -> dict:
    """ lance pytest -k avec le nom des fonctions a tester de function_list dans current_file
        et renvoie (code_retour, texte_rapport).
        - code_retour : code de sortie de pytest (0 si tout va bien, >0 sinon).
        - texte_rapport : sortie complète de pytest (stdout + stderr).
    """
    file_path = Path(state["current_file"])    

    function_list = state.get("function_list", [])
    sandbox_dir = Path(state["sandbox_dir"])
    failed_test_files = state.get("failed_test_files", [])

    if not file_path.is_file():
        return {
            "raw_test_output": (1, f"File not found: {state['current_file']}"),
            "test_exit_code": 1,
            "function_without_tests": [],
            "import_error": False,
            "failed_test_files": failed_test_files
        }
    
    try:
        # Construire la commande de base
        if function_list:
            k_expression = " or ".join(function_list)
            cmd = ["pytest", str(sandbox_dir), "-k", k_expression, "-v","--collect-only"]
        else:
            # Si pas de fonctions spécifiques, tester tout le sandbox
            cmd = ["pytest", str(sandbox_dir), "-v"]
        
        # Ajouter --ignore pour chaque fichier test problématique
        if failed_test_files:
            print(f"\n🚫 Exclusion de {len(failed_test_files)} fichier(s) test problématique(s)")
            for failed_file in failed_test_files:
                cmd.extend(["--ignore", failed_file])
                print(f"   ➜ {failed_file}")
        
        # Exécuter pytest
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=sandbox_dir.parent
        )
        
        # Combiner stdout et stderr
        full_output = result.stdout + "\n" + result.stderr
        
        # Vérifier les erreurs d'import
        has_import_error = "ImportError" in full_output or "ModuleNotFoundError" in full_output
        
        print(f"\n{'─'*80}")
        print(f"🧪 ÉTAPE 5/6 : EXÉCUTION DES TESTS")
        print(f"{'─'*80}")
        
        # Identifier les fonctions sans tests
        functions_without_tests = []
        for func in function_list:
            if f"test_{func}" not in full_output and f"_{func}" not in full_output:
                functions_without_tests.append(func)
        
        print(f"\n📊 Résultat : Code retour = {result.returncode}")
        if functions_without_tests:
            print(f"⚠️  {len(functions_without_tests)} fonction(s) sans tests : {', '.join(functions_without_tests)}")
        else:
            print(f"✅ Toutes les fonctions ont des tests")
        
        return {
            "raw_test_output": (result.returncode, full_output),
            "test_exit_code": result.returncode,
            "function_without_tests": functions_without_tests,
            "import_error": has_import_error,
            "failed_test_files": failed_test_files
        }
    
    except Exception as e:
        print(f"❌ [TestingTool] Erreur: {str(e)}")
        return {
            "raw_test_output": (1, f"Error running pytest: {str(e)}"),
            "test_exit_code": 1,
            "function_without_tests": list(function_list) if function_list else [],
            "import_error": False,
            "failed_test_files": failed_test_files
        }