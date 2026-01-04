import shutil
import os
from pathlib import Path
from src.utils.logger import log_experiment, ActionType
from src.utils.state.stateDefinition import SwarmState

def setup_node(state: SwarmState) -> SwarmState:
    """Prépare l'environnement sandbox."""
    target = state["target_dir"]
    sandbox = state["sandbox_dir"]
    current_file = Path(state["current_file"])
    
    # Nettoyage et copie
    if os.path.exists(sandbox):
        shutil.rmtree(sandbox)
    shutil.copytree(target, sandbox)
    
    # Calculer le chemin du fichier dans le sandbox
    relative_path = current_file.relative_to(target)
    sandbox_file = Path(sandbox) / relative_path
    
    print(f"📁 [Setup] Code copié de {target} vers {sandbox}")
    print(f"📁 [Setup] Fichier cible dans sandbox : {sandbox_file}")
    
    # On initialise le compteur et on met à jour current_file vers le sandbox
    return {
        "current_file": sandbox_file,
        "iteration_count": 0, 
        "tests_passed": False, 
        "status": "RUNNING"
    }

