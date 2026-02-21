from src.utils.state.stateDefinition import SwarmState

def ImportFinishNode(state: SwarmState) -> dict:
    """Node final du workflow après import."""
    print("🏁 [ImportFinishNode] Workflow d'importation terminé")

    return {"status": "IMPORT_WORKFLOW_COMPLETED"}