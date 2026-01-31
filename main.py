import argparse
import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from src.utils.graph.graphDefinition import builder

load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Dossier {args.target_dir} introuvable.")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
    
    # Récupérer tous les fichiers .py
    python_files = list(Path(args.target_dir).rglob("*.py"))
    if not python_files:
        print(f"❌ Aucun fichier .py trouvé dans {args.target_dir}")
        sys.exit(1)
    else:
        print(f"🔍 Fichiers .py trouvés : {len(python_files)} fichiers")
        for f in python_files:
            print(f"   - {f}")
    
    # Compiler le graph
    graph = builder.compile()
    
    # Traiter chaque fichier individuellement
    for idx, python_file in enumerate(python_files, 1):
        print(f"\n{'='*60}")
        print(f"📝 Traitement du fichier {idx}/{len(python_files)}: {python_file}")
        print(f"{'='*60}\n")
        
        # Créer un state initial pour ce fichier
        initial_state = {
            "target_dir": args.target_dir,
            "sandbox_dir": os.path.join(args.target_dir, "..", "sandbox"),
            "current_file": python_file,
            "iteration_count": 0,
            "max_iterations": 5,
            "pylint_reports": (0, ""),
            "refactor_plan": None,
            "raw_test_output": "",
            "test_exit_code": 0,
            "test_analysis": "",
            "tests_passed": False,
            "status": "INIT"
        }
        
        try:
            # Exécuter le workflow pour ce fichier
            result = graph.invoke(initial_state)
            
            # Afficher les résultats
            print(f"\n✅ Analyse terminée pour {python_file}")
            print(f"   Status: {result.get('status', 'UNKNOWN')}")
            
            # Afficher le rapport Pylint
            if result.get("pylint_reports"):
                code, output = result["pylint_reports"]
                print(f"   Pylint exit code: {code}")
            
            # Afficher le plan de refactoring (rapport de l'auditeur)
            if result.get("refactor_plan"):
                print(f"\n📋 Rapport de l'Auditeur:")
                for plan in result["refactor_plan"]:
                    print(plan)
            
        except Exception as e:
            print(f"❌ Erreur lors du traitement de {python_file}: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\n{'='*60}")
    print("✅ MISSION_COMPLETE - Tous les fichiers ont été traités")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()