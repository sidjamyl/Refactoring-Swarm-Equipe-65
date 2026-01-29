import ast

from src.utils.state.stateDefinition import SwarmState

def list_functions_in_code(state: SwarmState) -> dict:
    """Liste robuste via AST (Abstract Syntax Tree)."""
    refactored_code = state["refactored_code"]
    function_list = []
    
    try:
        tree = ast.parse(refactored_code)
        for node in ast.walk(tree):
            # Capture les fonctions et les méthodes (async inclus)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_list.append(node.name)
    except SyntaxError:
        # Si le code est trop "messy" et ne compile pas, on retourne une liste vide
        # ou on laisse l'Auditeur gérer l'erreur de syntaxe avant.
        print("❌ Syntaxe invalide détectée par AST")
        pass

    print(f"\n{'─'*80}")
    print(f"📋 IDENTIFICATION DES FONCTIONS")
    print(f"{'─'*80}")
    print(f"\n✅ {len(function_list)} fonction(s) trouvée(s) : {', '.join(function_list) if function_list else 'Aucune'}")
    
    return {"function_list": function_list}