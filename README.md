# 🚀 GraphCoder MCP (AI Agent with LangChain)

基于 **LangGraph** 与 **MCP (Model Context Protocol)** 协议构建的多专家协同自动化编程智能体系统。
该系统能够理解复杂的自然语言需求，自主进行任务规划、企业知识检索（RAG）、动态技能加载（SKILLS），并在安全沙箱中自由且安全地跨语言执行代码与系统终端操作。

## ✨ 项目亮点 (Key Features)

### 1. 🧠 Supervisor 多智能体核心架构
- 基于 **LangGraph** 构建了灵活的图状态机工作流，引入核心的 `Supervisor` 路由节点。
- 采用 **Mandatory Workflow（强制工作流）**：通过机制约束，Agent 必须先指派 `research_expert` 进行充分的上下文探索、规则学习与知识库查询，随后才能调度 `code_expert` 进场编写代码与系统交互，大幅降低了大模型常见的"跳步"现象与编码幻觉。

### 2. ⚡️ SKILLS 动态规则自发现机制
- 打破了传统大模型 System Prompt 容易超长、遗忘或污染的上下文瓶颈。
- Agent 会在运行期间，通过专用的文件系统扫描探针，主动去感知并读取项目或独立目录下的 `.md` / `SKILL.md` 业务逻辑约束。
- 开发者可以无缝切入不同项目，Agent 会自动跟随目录特征匹配所需的编码规范、前置要求以及最佳实践操作。

### 3. 🔌 MCP 协议驱动的安全标准工具链
- 深度集成并实践了最新的 **Model Context Protocol (MCP)** 协议，实现外挂能力库的高度解耦：
  - `shell_tools` / `powershell_tools`：跨平台沙箱化的系统终端命令执行。
  - `mysql_tools`：数据库自动化链接、查询、表结构读取与智能排障。
  - `file_tools`：直通宿主机目录的精准项目源文件级操作。
  - `browser_tools`：基于浏览器自动化技术的网页操作与调试信息获取。

### 4. ☁️ 云原生极简 RAG 架构 (接入阿里云百炼)
- 摒弃了通常开源项目依赖的沉重本地向量数据库（如 Chroma / Milvus）。
- 无缝对接 **阿里云百炼 (Bailian) 原生云 SDK**，通过云端数据中心实现全局的文档向量化处理和智能混合检索，保证开发机轻量化。
- 本地提供直接打通百炼云后端的 API Agent Tools (`upload_local_file_to_bailian_rag`)，支持系统自主将新学的技术文档直接灌入个人云端外脑。

---

## 🛠️ 快速开始 (Quick Start)

### 1. 环境准备
确保本地安装有 **Python 3.10+** 环境，推荐使用 `venv` 或 `conda` 创建虚拟沙箱。

### 2. 克隆项目
```bash
git clone https://github.com/jiakailong/GraphCoder.git
cd ai_agent_with_langchain
```

### 3. 环境变量配置
复制并修改根目录环境配置文件：
```bash
cp .env.example .env
```
按照提示申请并填入你的 `OPENAI_API_KEY` (或兼容的服务商 Key)、`ALIBABA_CLOUD_ACCESS_KEY` 以及对应的**百炼各项能力 ID**。

### 4. 一键交互式启动
```bash
# macOS / Linux
bash start.sh

# Windows
start.bat
```

---

## 📂 架构目录概述
```text
├── app/
│   ├── code_agent/
│   │   ├── agent/         # LangGraph 驱动中枢：Supervisor路由与主提示词策略
│   │   ├── mcp/           # MCP Servers：被隔离调用的各种本地原子Native工具服务端
│   │   ├── tools/         # Tools Wrappers：直通模型层的标准化外联工具适配器(SKILLS相关逻辑)
│   │   ├── rag/           # RAG Core：链接阿里云百炼API云端知识库能力模块
│   │   └── utils/         # 独立化运行维护等底层支持类
│   └── core/              # Pydantic Settings 配置中枢与 Env 收口
├── test/                  # (Optional) 模型对接与功能测试用例
├── start.sh               # Bash 交互引导前端
└── .env.example           # 全局环境依赖参考模板
```
