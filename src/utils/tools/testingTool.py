import subprocess
from pathlib import Path
from src.utils.state.stateDefinition import SwarmState

def run_pytest_tool(state: SwarmState) -> dict:
    """ lance pytest -k avec le nom des fonctions a tester de function_list dans current_file
        et renvoie (code_retour, texte_rapport).
        - code_retour : code de sortie de pytest (0 si tout va bien, >0 sinon).
        - texte_rapport : sortie complète de pytest (stdout + stderr).
    """
    file_path = Path(state["current_file"]).resolve()    

    function_list = state.get("function_list", [])
    # Filtrer les dunder methods (__init__, __str__, etc.) qui n'ont jamais de tests
    function_list = [f for f in function_list if not (f.startswith("__") and f.endswith("__"))]
    target_dir = Path(state["target_dir"]).resolve()
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
        # Déterminer le fichier de test correspondant au fichier source en cours
        test_file = target_dir / "tests" / f"test_{file_path.stem}.py"
        
        # Cibler UNIQUEMENT le fichier test correspondant au module source
        if test_file.exists():
            test_target = str(test_file)
        else:
            # Pas de fichier test → toutes les fonctions sont sans tests
            print(f"\n{'─'*80}")
            print(f"🧪 ÉTAPE 5/6 : EXÉCUTION DES TESTS")
            print(f"{'─'*80}")
            print(f"\n📊 Résultat : Aucun fichier test trouvé ({test_file.name})")
            print(f"⚠️  {len(function_list)} fonction(s) sans tests : {', '.join(function_list)}")
            return {
                "raw_test_output": (5, f"No test file found: {test_file.name}"),
                "test_exit_code": 5,
                "function_without_tests": list(function_list),
                "import_error": False,
                "failed_test_files": failed_test_files
            }
        
        if function_list:
            k_expression = " or ".join(function_list)
            cmd = ["pytest", test_target, "-k", k_expression, "-v", "--collect-only"]
        else:
            cmd = ["pytest", test_target, "-v"]
        
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
            cwd=target_dir.parent
        )
        
        # Combiner stdout et stderr
        full_output = result.stdout + "\n" + result.stderr
        
        # Vérifier les erreurs d'import ou de syntaxe
        has_import_error = "ImportError" in full_output or "ModuleNotFoundError" in full_output
        has_syntax_error = "SyntaxError" in full_output or "IndentationError" in full_output
        
        # Si le fichier de test a une erreur de collection (code 2), le supprimer
        # pour qu'il soit régénéré proprement au prochain passage
        if result.returncode == 2 and test_file.exists():
            if has_import_error or has_syntax_error or "ERROR collecting" in full_output:
                print(f"\n🗑️  Fichier test corrompu détecté ({test_file.name}), suppression pour régénération")
                try:
                    test_file.unlink()
                    print(f"   ✅ {test_file.name} supprimé")
                except Exception as e:
                    print(f"   ⚠️  Impossible de supprimer: {e}")
        
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