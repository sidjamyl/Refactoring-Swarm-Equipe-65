import subprocess
from pathlib import Path
from typing import Tuple
from langchain_core.tools import tool 

@tool
def run_pylint_on_file(file_path: str) -> Tuple[int, str]:
    """
    Lance pylint sur un fichier et renvoie (code_retour, texte_rapport).
    - code_retour : code de sortie de pylint (0 si tout va bien, >0 sinon).
    - texte_rapport : sortie complète de pylint (stdout + stderr).
    """
    path = Path(file_path)

    if not path.is_file():
        return 1, f"File not found: {file_path}"

    try:
        result = subprocess.run(
            ["pylint", str(path)],
            capture_output=True,
            text=True
        )
        output = result.stdout + "\n" + result.stderr
        return result.returncode, output
    except FileNotFoundError:
        # pylint n'est pas trouvé dans l'environnement
        return 1, "Error: pylint command not found. Is it installed in your venv?"