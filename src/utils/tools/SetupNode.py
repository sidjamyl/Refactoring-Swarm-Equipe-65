import shutil
import os
from pathlib import Path
from src.utils.logger import log_experiment, ActionType
from src.utils.state.stateDefinition import SwarmState

def setup_node(state: SwarmState) -> SwarmState:
    """Prépare l'environnement sandbox."""
    current_file = Path(state["current_file"])
    sandbox = state["sandbox_dir"]
    
    print(f"\n{'╔'+'═'*78+'╗'}")
    print(f"║{' '*30}🚀 INITIALISATION{' '*30}║")
    print(f"{'╚'+'═'*78+'╝'}")
    print(f"\n📂 Répertoire de travail  : {sandbox}")
    print(f"📄 Fichier à analyser     : {current_file.name}")
    print(f"🔧 État initial           : Configuration terminée")
    
    input("\n[Appuyez sur Entrée pour démarrer l'analyse...]")
    
    # On initialise le compteur sans copier de fichiers
    return {
        "current_file": current_file,
        "iteration_count": 0, 
        "tests_passed": False, 
        "status": "RUNNING"
    }
