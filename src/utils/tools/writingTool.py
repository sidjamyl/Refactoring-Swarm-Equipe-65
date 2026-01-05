from src.utils.state.stateDefinition import SwarmState

def write_refactored_code(state: SwarmState) -> dict:
    """Écrit le code refactorisé."""
    current_file = state["current_file"]
    refactored_code = state["refactored_code"]
    
    print(f"✍️ [WriteTool] Écriture du code refactorisé dans : {current_file}")
    try:
        current_file.write_text(refactored_code, encoding="utf-8")
        print(f"✅ [WriteTool] Fichier mis à jour avec succès")
        return {"status": "CODE_WRITTEN",
                "refactor_applied": True}
    except Exception as e:
        print(f"❌ [WriteTool] Erreur : {e}")
        return {"status": "WRITE_ERROR"
                , "refactor_applied": False}
    