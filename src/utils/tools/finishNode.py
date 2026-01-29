
from src.utils.state.stateDefinition import SwarmState


def finish_node(state: SwarmState) -> dict:
    """Node final du workflow."""
    print(f"\n{'╔'+'═'*78+'╗'}")
    print(f"║{' '*25}🏁 WORKFLOW TERMINÉ{' '*26}║")
    print(f"{'╚'+'═'*78+'╝'}")
    return {"status": "WORKFLOW_COMPLETED"}