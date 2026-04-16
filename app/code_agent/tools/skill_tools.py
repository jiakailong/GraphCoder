import os
from langchain_core.tools import tool

SKILLS_DIR = os.path.join(os.getenv("WORKSPACE_ROOT", os.getcwd()), "app/code_agent/skills")

@tool
def list_skills() -> str:
    """列出系统中所有可用的专项技能（SKILLS）。系统技能可能以 .md 结尾单文件存在，或是包含 SKILL.md 的同名文件夹。当不知道如何执行特定任务时，优先调用此工具查看是否有对口的技能。"""
    if not os.path.exists(SKILLS_DIR):
        return "没有找到 skills 目录。"
    
    skills = []
    for item in os.listdir(SKILLS_DIR):
        item_path = os.path.join(SKILLS_DIR, item)
        if os.path.isfile(item_path) and item.endswith(".md"):
            skills.append(item)
        elif os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "SKILL.md")):
            skills.append(item)

    if not skills:
        return "当前没有任何可用的 skill 目录或文件。"
    
    return "系统可用技能如下 (请使用 read_skill 并传入名称读取):\n" + "\n".join(skills)

@tool
def read_skill(skill_filename: str) -> str:
    """读取并加载一个专项技能。输入参数可是独立的 md 文件名（如 'abc.md'）或是独立包含技能的文件夹名称（如 'skill-forge'）。"""
    target_path = None
    dir_path = os.path.join(SKILLS_DIR, skill_filename)
    
    # check if it's a directory containing SKILL.md rules
    if os.path.isdir(dir_path) and os.path.exists(os.path.join(dir_path, "SKILL.md")):
        target_path = os.path.join(dir_path, "SKILL.md")
    else:
        # fallback to original logic for .md files
        if not skill_filename.endswith(".md"):
            skill_filename += ".md"
        target_path = os.path.join(SKILLS_DIR, skill_filename)

    if not target_path or not os.path.exists(target_path):
        return f"技能文件或目录 {skill_filename} 不存在或内部不包含 SKILL.md。"
        
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
            return f"成功加载技能 {skill_filename} :\n" + content
    except Exception as e:
        return f"读取技能文件失败: {e}"

skill_tools = [list_skills, read_skill]
