from langgraph.graph import StateGraph
from src.utils.state.stateDefinition import SwarmState
from src.utils.agents.AuditorAgent import auditor_agent_node
from src.utils.tools.SetupNode import setup_node
from src.utils.tools.pylintTool import run_pylint_on_file
from src.utils.agents.FixerAgent import fixer_agent_node
from src.utils.tools.writingTool import write_refactored_code
from src.utils.tools.readingTool import read_file
from src.utils.tools.testingTool import run_pytest_tool
from src.utils.agents.TestGeneratorAgent import test_generator_agent_node
from src.utils.agents.JudgeAgent import judge_agent_node
from src.utils.graph.conditions.testExist import check_tests_exist
from src.utils.graph.conditions.nextActions import decide_next_action
from src.utils.tools.finishNode import finish_node
from src.utils.tools.listFunctionsTool import list_functions_in_code


builder = StateGraph(SwarmState)
    
   
builder.add_node("setup_node", setup_node)
builder.add_node("auditor_agent_node", auditor_agent_node)
builder.add_node("run_pylint_on_file", run_pylint_on_file)
builder.add_node("fixer_agent_node", fixer_agent_node)
builder.add_node("write_refactored_code", write_refactored_code)
builder.add_node("read_file", read_file)
builder.add_node("run_pytest_tool", run_pytest_tool)
builder.add_node("list_functions_in_code_tool", list_functions_in_code)
builder.add_node("test_generator_agent_node", test_generator_agent_node)
builder.add_node("judge_agent_node", judge_agent_node)
builder.add_node("finish_node", finish_node)



builder.set_entry_point("setup_node")
builder.add_edge("setup_node", "run_pylint_on_file")
builder.add_edge("run_pylint_on_file", "auditor_agent_node")
builder.add_edge("auditor_agent_node", "read_file")
builder.add_edge("read_file", "fixer_agent_node")
builder.add_edge("fixer_agent_node", "write_refactored_code")
builder.add_edge("write_refactored_code", "list_functions_in_code_tool")
builder.add_edge("list_functions_in_code_tool", "run_pytest_tool")
    
builder.add_conditional_edges(
        "run_pytest_tool",
        check_tests_exist,
        {
            "tests_exist": "judge_agent_node",
            "tests_do_not_exist": "test_generator_agent_node"
        }
    )
    
builder.add_edge("test_generator_agent_node", "run_pytest_tool")
        
builder.add_conditional_edges(
    "judge_agent_node",
    decide_next_action,
    {
        "finish": "finish_node",
        "retry": "fixer_agent_node"
    }
)
    
builder.set_finish_point("finish_node")

builder.compile()