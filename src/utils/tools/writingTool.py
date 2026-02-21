from src.utils.state.stateDefinition import SwarmState

def write_refactored_code(state: SwarmState) -> dict:
    """Écrit le code refactorisé."""
    current_file = state["current_file"]
    refactored_code = state["refactored_code"]
    
    print(f"\n{'─'*80}")
    print(f"✍️  SAUVEGARDE DU CODE")
    print(f"{'─'*80}")
    print(f"\n💾 Écriture dans : {current_file.name if hasattr(current_file, 'name') else current_file}")
    
    try:
        if hasattr(current_file, 'write_text'):
            current_file.write_text(refactored_code, encoding="utf-8")
        else:
            with open(current_file, 'w', encoding='utf-8') as f:
                f.write(refactored_code)
        print(f"✅ Fichier sauvegardé avec succès")
        return {"status": "CODE_WRITTEN",
                "refactor_applied": True}
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return {"status": "WRITE_ERROR"
                , "refactor_applied": False}
    