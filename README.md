# Dev-Asset-AI-Parser

> 基于 Python + Pandas + LLM Function Calling 的自动化网络资产变动审计工具。

## 核心特性
* **数据清洗管道**：支持 JSON 格式资产解析，利用 Pandas 实现主键去重与格式标准化。
* **差异审计引擎**：精确比对新旧设备信息，提取新增、下线及状态异常设备。
* **AI 风险分析**：基于 Function Calling 深度对接大模型 API，自动生成网络拓扑变更与安全风险评估报告。
* **CLI 交互**：提供直观的终端菜单，支持一键式本地审计和与AI使用自然语言协同分析。

## 项目结构
```text
├── asset_processor.py   # 设备信息抓取解析与Diff比对
├── AI_Call.py           # 大模型Function Calling
├── main.py              # CLI交互主程序
├── old-assets.json      # 旧设备数据示例
├── new-assets.json      # 新设备数据示例
└── env.template         # 环境变量配置模板
```

## 快速开始
1. 克隆项目并安装依赖：
   ```bash
   pip install pandas python-dotenv zhipuai
   ```
2. 配置环境变量：
   拷贝 `env.template` 为 `.env`，并填写你的 `ZHIPUAI_API_KEY`。
3. 启动主程序：
   ```bash
   python main.py
   ```
