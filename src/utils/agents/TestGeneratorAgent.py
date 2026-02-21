from src.utils.state.stateDefinition import SwarmState
from src.utils.prompts.promptTestGenerator import SYSTEM_PROMPT_TEST_GENERATOR, USER_PROMPT_TEST_GENERATOR
import src.utils.agents.agentTest as agentTest
from pathlib import Path
import os
from src.utils.logger import log_experiment, ActionType


def test_generator_agent_node(state: SwarmState) -> dict:
    """Génère des tests unitaires pour les fonctions sans tests."""
    current_file = Path(state["current_file"])
    refactored_code = state.get("refactored_code", "")
    functions_without_tests = state.get("function_without_tests", [])
    sandbox_dir = Path(state["sandbox_dir"])
    
    print(f"\n{'─'*80}")
    print(f"🔬 GÉNÉRATION DE TESTS UNITAIRES")
    print(f"{'─'*80}")
    print(f"\n📋 Fonctions à tester : {', '.join(functions_without_tests) if functions_without_tests else 'Aucune'}")
    
    # Forcer la génération même si la liste est vide (pour debug)
    if not functions_without_tests:
        print("⚠️  Aucune fonction détectée, génération forcée")
        functions_without_tests = ["all_functions"]
    
    # Construire le prompt
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_TEST_GENERATOR},
        {"role": "user", "content": USER_PROMPT_TEST_GENERATOR.format(
            file_name=current_file.name,
            code=refactored_code if refactored_code else "# No code provided",
            functions_without_tests=", ".join(functions_without_tests)
        )}
    ]
    
    print(f"\n🤖 Appel du LLM pour générer les tests...")
    
    # Construire le user_prompt pour le logging
    user_prompt = USER_PROMPT_TEST_GENERATOR.format(
        file_name=current_file.name,
        code=refactored_code if refactored_code else "# No code provided",
        functions_without_tests=", ".join(functions_without_tests)
    )
    
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
    
    # Créer le dossier tests/ (chemin absolu)
    tests_dir = sandbox_dir / "tests"
    
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
    print(f"\n💾 Écriture du fichier de test : {test_file.name}")
    
    try:
        # Écrire le fichier
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