import subprocess
from pathlib import Path
from typing import Tuple
from langchain_core.tools import tool 
from src.utils.state.stateDefinition import SwarmState


def run_pylint_on_file(state: SwarmState) -> dict:
    """
    Lance pylint sur un fichier et renvoie (code_retour, texte_rapport).
    - code_retour : code de sortie de pylint (0 si tout va bien, >0 sinon).
    - texte_rapport : sortie complète de pylint (stdout + stderr).
    """
    path = Path(state["current_file"])

    if not path.is_file():
       return {"pylint_reports": (1, f"File not found: {state['current_file']}")}

    try:
        result = subprocess.run(
            ["pylint", str(path)],
            capture_output=True,
            text=True
        )
        output = result.stdout + "\n" + result.stderr

        return {
            "pylint_reports": (result.returncode, output)
        }

        
    except FileNotFoundError:
        # pylint n'est pas trouvé dans l'environnement
        return {"pylint_reports": (1, "Error: pylint not found")}