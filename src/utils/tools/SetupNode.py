import shutil
import os
from src.utils.logger import log_experiment, ActionType
from src.utils.state.stateDefinition import SwarmState

def setup_node(state: SwarmState) -> SwarmState:
    """Prépare l'environnement sandbox."""
    target = state["target_dir"]
    sandbox = state["sandbox_dir"]
    
    # Nettoyage et copie
    if os.path.exists(sandbox):
        shutil.rmtree(sandbox)
    shutil.copytree(target, sandbox)
    
    print(f"📁 [Setup] Code copié de {target} vers {sandbox}")
    
    # On initialise le compteur
    return {"iteration_count": 0, "tests_passed": False, "status": "RUNNING"}

