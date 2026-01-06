
from src.utils.state.stateDefinition import SwarmState

def read_file(state  : SwarmState) -> dict:
    """
    Lit le contenu du fichier spécifié dans l'état et le renvoie sous forme de chaîne.
    """
    file_path = state["current_file"]
    print(f"📖 [ReadTool] Lecture du fichier : {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        print(f"✅ [ReadTool] Fichier lu avec succès ({len(content)} caractères)")
        print(f"\n{'='*60}")
        print("📄 CODE ORIGINAL LU:")
        print(f"{'='*60}")
        print(content)
        print(f"{'='*60}\n")
        return  {"original_code": content}
    except Exception as e:
        print(f"❌ [ReadTool] Erreur de lecture : {e}")
        return {"original_code": f"Error reading file: {e}"}    