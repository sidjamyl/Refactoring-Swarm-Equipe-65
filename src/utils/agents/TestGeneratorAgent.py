from src.utils.state.stateDefinition import SwarmState
from src.utils.prompts.promptTestGenerator import SYSTEM_PROMPT_TEST_GENERATOR, USER_PROMPT_TEST_GENERATOR, USER_PROMPT_TEST_GENERATOR_APPEND
import src.utils.agents.agentTest as agentTest
from pathlib import Path
import os
from src.utils.logger import log_experiment, ActionType


def test_generator_agent_node(state: SwarmState) -> dict:
    """Génère des tests unitaires pour les fonctions sans tests."""
    current_file = Path(state["current_file"]).resolve()
    refactored_code = state.get("refactored_code", "")
    functions_without_tests = state.get("function_without_tests", [])
    target_dir = Path(state["target_dir"]).resolve()
    
    print(f"\n{'─'*80}")
    print(f"🔬 GÉNÉRATION DE TESTS UNITAIRES")
    print(f"{'─'*80}")
    print(f"\n📋 Fonctions à tester : {', '.join(functions_without_tests) if functions_without_tests else 'Aucune'}")
    
    # Forcer la génération même si la liste est vide (pour debug)
    if not functions_without_tests:
        print("⚠️  Aucune fonction détectée, génération forcée")
        functions_without_tests = ["all_functions"]
    
    # Construire le prompt
    test_file = (target_dir / "tests" / f"test_{current_file.stem}.py")
    existing_tests_content = ""
    is_append_mode = test_file.exists() and test_file.stat().st_size > 0

    # Calculer le module_name comme chemin relatif avec des points (ex: services.validators)
    module_name = current_file.relative_to(target_dir).with_suffix('').as_posix().replace('/', '.')

    if is_append_mode:
        try:
            existing_tests_content = test_file.read_text(encoding="utf-8")
            print(f"📎 Mode AJOUT : {test_file.name} existe déjà ({len(existing_tests_content)} chars)")
        except Exception:
            is_append_mode = False

    if is_append_mode:
        user_prompt = USER_PROMPT_TEST_GENERATOR_APPEND.format(
            file_name=current_file.name,
            code=refactored_code if refactored_code else "# No code provided",
            functions_without_tests=", ".join(functions_without_tests),
            existing_tests=existing_tests_content,
            module_name=module_name
        )
    else:
        user_prompt = USER_PROMPT_TEST_GENERATOR.format(
            file_name=current_file.name,
            code=refactored_code if refactored_code else "# No code provided",
            functions_without_tests=", ".join(functions_without_tests),
            module_name=module_name
        )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_TEST_GENERATOR},
        {"role": "user", "content": user_prompt}
    ]
    
    print(f"\n🤖 Appel du LLM pour générer les tests...")
    
    # Appeler le LLM
    try:
        response = agentTest.model.invoke(messages)
        generated_tests = response.content
        status = "SUCCESS"
        print(f"✅ Tests générés ({len(generated_tests)} caractères)")
    except Exception as e:
        print(f"❌ [TestGenerator] Erreur LLM: {e}")
        generated_tests = f"Error generating tests: {str(e)}"
        status = "FAILURE"
        
        # Logging de l'erreur
        log_experiment(
            agent_name="TestGenerator",
            model_used=agentTest.model.model,
            action=ActionType.GENERATION,
            details={
                "input_prompt": SYSTEM_PROMPT_TEST_GENERATOR + "\n" + user_prompt,
                "output_response": generated_tests
            },
            status=status
        )
        return {"status": "LLM_ERROR"}
    
    # Nettoyer le code généré
    if "```python" in generated_tests:
        generated_tests = generated_tests.split("```python")[1].split("```")[0].strip()
    elif "```" in generated_tests:
        generated_tests = generated_tests.split("```")[1].split("```")[0].strip()
    
    # Créer le dossier tests/ dans target_dir (à côté des fichiers source)
    tests_dir = target_dir / "tests"
    
    try:
        tests_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"❌ [TestGenerator] Erreur création dossier: {e}")
        return {"status": "FOLDER_CREATION_ERROR"}
    
    # Créer __init__.py pour que ce soit un package Python
    init_file = tests_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")
    
    # Créer le fichier de test
    test_file = tests_dir / f"test_{current_file.stem}.py"
    print(f"\n💾 {'Ajout au' if is_append_mode else 'Création du'} fichier de test : {test_file.name}")
    
    try:
        if is_append_mode:
            # Séparer les imports des tests dans le code généré
            new_lines = generated_tests.splitlines()
            new_import_lines = []
            new_test_lines = []
            for line in new_lines:
                stripped = line.strip()
                # Ne garder que les imports au niveau top-level (pas indentés)
                if (stripped.startswith("import ") or stripped.startswith("from ")) and not line[0:1].isspace():
                    new_import_lines.append(stripped)  # Toujours stocker la version sans indentation
                else:
                    new_test_lines.append(line)
            
            # Retirer les lignes vides en tête des tests
            while new_test_lines and not new_test_lines[0].strip():
                new_test_lines.pop(0)
            
            # Fusionner les imports manquants dans le fichier existant
            if new_import_lines:
                # Dédupliquer les imports entre eux aussi
                seen = set()
                unique_imports = []
                for imp in new_import_lines:
                    if imp not in seen:
                        seen.add(imp)
                        unique_imports.append(imp)
                missing_imports = [
                    imp for imp in unique_imports
                    if imp and imp not in existing_tests_content
                ]
                if missing_imports:
                    # Insérer après le dernier import du fichier existant
                    existing_lines = existing_tests_content.splitlines()
                    last_import_idx = 0
                    for i, line in enumerate(existing_lines):
                        stripped = line.strip()
                        if stripped.startswith("import ") or stripped.startswith("from "):
                            last_import_idx = i
                    # Insérer les nouveaux imports juste après le dernier import existant
                    insert_at = last_import_idx + 1
                    existing_lines[insert_at:insert_at] = missing_imports
                    with open(test_file, "w", encoding="utf-8") as f:
                        f.write("\n".join(existing_lines) + "\n")
                    print(f"📥 {len(missing_imports)} import(s) ajouté(s) : {[i.strip() for i in missing_imports]}")
            
            # Ajouter les nouveaux tests à la fin
            test_code_to_append = "\n".join(new_test_lines).strip()
            if test_code_to_append:
                with open(test_file, "a", encoding="utf-8") as f:
                    f.write("\n\n\n# --- Tests générés automatiquement ---\n")
                    f.write(test_code_to_append)
                    f.write("\n")
            print(f"✅ Tests ajoutés avec succès")
        else:
            # Créer un nouveau fichier
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(generated_tests)
        
        # Vérifier que le fichier existe et a du contenu
        if test_file.exists():
            file_size = os.path.getsize(test_file)
            print(f"✅ Fichier créé avec succès ({file_size} bytes)")
            write_status = "SUCCESS"
        else:
            print(f"❌ Échec de création du fichier")
            write_status = "FAILURE"
        
        # Logging de l'expérience
        log_experiment(
            agent_name="TestGenerator",
            model_used=agentTest.model.model,
            action=ActionType.GENERATION,
            details={
                "input_prompt": SYSTEM_PROMPT_TEST_GENERATOR + "\n" + user_prompt,
                "output_response": generated_tests
            },
            status=write_status
        )
        
        return {
            "status": "TESTS_GENERATED",
            "function_without_tests": [],
        }
    except Exception as e:
        print(f"❌ [TestGenerator] Erreur écriture fichier: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "TEST_GENERATION_FAILED",
            "function_without_tests": functions_without_tests
        }