from langgraph.graph import StateGraph
from src.utils.state.stateDefinition import SwarmState
from src.utils.agents.AuditorAgent import auditor_agent_node
from src.utils.tools.SetupNode import setup_node
from src.utils.tools.pylintTool import run_pylint_on_file


builder = StateGraph(SwarmState)


builder.add_node("setup_node", setup_node)
builder.add_node("auditor_agent_node", auditor_agent_node)
builder.add_node("run_pylint_on_file", run_pylint_on_file)


builder.set_entry_point("setup_node")
builder.add_edge("setup_node", "run_pylint_on_file")
builder.add_edge("run_pylint_on_file", "auditor_agent_node")
builder.set_finish_point("auditor_agent_node")
