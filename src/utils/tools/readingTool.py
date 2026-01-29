
from src.utils.state.stateDefinition import SwarmState

def read_file(state  : SwarmState) -> dict:
    """
    Lit le contenu du fichier spécifié dans l'état et le renvoie sous forme de chaîne.
    """
    file_path = state["current_file"]
    
    print(f"\n{'─'*80}")
    print(f"📖 ÉTAPE 3/6 : LECTURE DU CODE SOURCE")
    print(f"{'─'*80}")
    print(f"\n📂 Fichier : {file_path.name if hasattr(file_path, 'name') else file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        lines = len(content.split('\n'))
        print(f"✅ Lecture réussie")
        print(f"📊 Statistiques : {len(content)} caractères, {lines} lignes")
        return  {"original_code": content}
    except Exception as e:
        print(f"❌ Erreur de lecture : {e}")
        return {"original_code": f"Error reading file: {e}"}    