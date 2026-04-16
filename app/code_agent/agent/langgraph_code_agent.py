import asyncio
import sys
try:
    import readline
except ImportError:
    pass  # readline is not available on all platforms (e.g., Windows without pyreadline)

from langchain_core.messages import convert_to_messages
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

from app.code_agent.tools.file_tools_wrapper import file_tools
from app.code_agent.model.qwen import llm_qwen
from app.code_agent.tools.shell_tools import get_stdio_shell_tools
from app.code_agent.tools.terminal_tools import get_stdio_terminal_tools
from app.code_agent.tools.skill_tools import skill_tools


def pretty_print_messages(update, last_message=False):
    if not isinstance(update, dict):
        return

    if "messages" in update:
        messages = convert_to_messages(update['messages'])
        if last_message:
            messages = messages[-1:]
        for message in messages:
            pretty_message = message.pretty_repr(html=True)
            print(pretty_message)
    else:
        for node_name, node_update in update.items():
            if isinstance(node_update, dict) and 'messages' in node_update:
                messages = convert_to_messages(node_update['messages'])
                if last_message:
                    messages = messages[-1:]

                for message in messages:
                    pretty_message = message.pretty_repr(html=True)
                    print(f"[{node_name}] \n" + pretty_message)

    print("\n")


async def run_agent():
    memory = MemorySaver()

    shell_tools = await get_stdio_shell_tools()

    research_agent = create_react_agent(
        model=llm_qwen,
        tools=shell_tools + file_tools + skill_tools,
        name="research_expert",
        prompt="你是一个极度严谨的技术主管。在面对任何新任务时，你【必须优先】调用 list_skills 函数查看系统有什么可以使用的规范配置，如果是符合当前任务的业务或代码规范，你必须使用 read_skill 读取它们。在获取了技能规范的背景知识后，你再输出你要指导 code_expert 进行开发的技术方案指令。",
    )

    code_agent = create_react_agent(
        model=llm_qwen,
        tools=shell_tools + file_tools + skill_tools,
        name="code_expert",
        prompt="你是一个编程专家，请根据 research_expert 设计的技术方案来实现代 码或进行代码文件相关的操作。如果你需要具体的编码规范或流程指令，请务必提前调用 read_skill 读取相应的技能文件获取指导。",
    )

    supervisor_agent = create_supervisor(
        agents=[research_agent, code_agent],
        model=llm_qwen,
        prompt=(
            "You are an orchestration supervisor for an AI agent team.\n"
            "MANDATORY WORKFLOW FOR ALL NEW CODING OR ANALYSIS REQUESTS:\n"
            "1. You MUST ALWAYS route tasks to 'research_expert' FIRST so it can read relevant SKILLs with its tools and establish a plan.\n"
            "2. Only after 'research_expert' finishes designing the plan, route the task to 'code_expert' for coding/execution.\n"
            "If the user asks about available SKILLS, route directly to research_expert to list them.\n"
        )
    )

    app = supervisor_agent.compile(checkpointer=memory) # 移除了之前过于严格的全量节点打断 (HITL APPROVAL POINT)


    while True:
        config = RunnableConfig(configurable={"thread_id": "session-1"}, recursion_limit=100)
        
        # State processing
        state = app.get_state(config)
        
        # Handle interruptions
        if state.next:
            print(f"\n⚠️ 工作流被中断！待执行节点: {state.next}")
            action = input("是否允许继续执行该高危节点？(y/n): ")
            if action.lower() == 'y':
                print("✅ 审批通过，继续...")
                # Start from resumed state
                # Stream the resumed logic
                try:
                    async for chunk in app.astream(None, config=config):
                        pretty_print_messages(chunk, last_message=True)
                except Exception as e:
                    import traceback; traceback.print_exc()
                    print(f"Exception during resumed execution. Reason: {e}")
            else:
                print("❌ 审批驳回。")
            continue

        user_input = input("用户：")
        if user_input.lower() == "exit":
            break

        # Normal execution
        try:
            if user_input.strip() != "":
                async for chunk in app.astream({"messages": [("user", user_input)]}, config=config):
                    pretty_print_messages(chunk, last_message=True)
        except Exception as e:
            import traceback; traceback.print_exc()
            print(f"Exception during execution. Reason: {e}")
asyncio.run(run_agent())
if __name__ == "__main__":
    asyncio.run(run_agent())
