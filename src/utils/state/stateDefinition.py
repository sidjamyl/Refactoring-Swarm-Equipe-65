from typing import  List, Optional, Annotated, Tuple
from typing_extensions import TypedDict
import typing
from langchain_core.messages import BaseMessage
from pathlib import Path


class SwarmState(TypedDict):
    target_dir: str
    sandbox_dir: str
    current_file: Path
    # --- Champs existants --


    iteration_count: int
    max_iterations: int
    
    # Données de navigation
    pylint_reports: Tuple[int, str]  # Rapport pylint pour le fichier analysé
    refactor_plan: Optional[str]


    original_code: Optional[str]      # ← Ajoutez
    refactored_code: Optional[str]    # ← Ajoutez

    function_list: Optional[List[str]]  # ← Ajoutez
    function_without_tests: Optional[List[str]]  # ← Ajoutez

    refactor_applied: bool    
    refactor_finished: bool        
    
    import_error: Optional[bool]  # ← Ajoutez
    failed_test_files: Optional[List[str]]  # Fichiers tests avec ImportError à ignorer

    # --- Nouveaux champs pour la séparation Test/Juge ---
    raw_test_output: str       # Logs bruts de pytest (Sortie du Tool)
    test_exit_code: int        # Code de retour de la commande (0=OK, 1=Err)
    
    test_analysis: str         # Analyse faite par l'Agent Juge (Feedback pour le Fixer)
    tests_passed: bool         # Verdict final (Succès/Echec)
    
    status: str