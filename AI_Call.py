import json
import os
from asset_processor import asset_diff, asset_parser
from dotenv import load_dotenv
from zhipuai import ZhipuAI

load_dotenv()
api_key = os.getenv("ZHIPUAI_API_KEY")
if not api_key:
    raise ValueError("未检测到API_KEY，请检查.env文件！")
client = ZhipuAI(api_key=api_key)


TOOL_MAP = {"get_asset_diff": lambda p1, p2: asset_diff(*asset_parser(p1, p2))}
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_asset_diff",
            "description": "读取并对比新旧两个 JSON 格式的网络资产文件，分析新增、下线设备及状态变更。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path_1": {
                        "type": "string",
                        "description": "旧资产 JSON 文件路径，如 old-assets.json",
                    },
                    "file_path_2": {
                        "type": "string",
                        "description": "新资产 JSON 文件路径，如 new-assets.json",
                    },
                },
                "required": ["file_path_1", "file_path_2"],
            },
        },
    }
]


def run_agent(user_query: str, model: str = "glm-4") -> str:
    """Agent 核心调度函数：处理用户输入 -> 触发 Function Calling -> 汇总输出"""
    messages = [{"role": "user", "content": user_query}]

    try:
        response = client.chat.completions.create(
            model=model, messages=messages, tools=tools, tool_choice="auto"
        )
        response_msg = response.choices[0].message

        if not response_msg.tool_calls:
            print("\n[AI回复]:\n", response_msg.content)
            return response_msg.content

        tool_call = response_msg.tool_calls[0]
        func_name = tool_call.function.name

        try:
            func_args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
            raise ValueError(
                f"大模型返回了无效的参数 JSON: {tool_call.function.arguments}"
            )

        print(f"\nAI触发工具调用: {func_name}")
        print(f"提取参数{func_args}")

        if func_name in TOOL_MAP:
            raw_diff = TOOL_MAP[func_name](
                func_args.get("file_path_1"), func_args.get("file_path_2")
            )

            # 2. 构造对话上下文闭环
            # 将 AI 第一轮的工具调用指令转化为标准字典追加到历史
            messages.append({
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        }
                    }
                ]
            })
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(raw_diff, ensure_ascii=False),
                }
            )

            print("正在生成网络审计分析报告...")
            second_response = client.chat.completions.create(
                model=model, messages=messages
            )
            final_report = second_response.choices[0].message.content

            print("\n" + "=" * 50)
            print("AI网络资产变动与风险审计报告")
            print("=" * 50)
            print(final_report)
            print("=" * 50 + "\n")

            return final_report
        else:
            raise NotImplementedError(
                f"本地未定义该工具的实现逻辑: {func_name}"
            )

    except Exception as e:
        error_msg = f"[x] Agent 执行失败: {str(e)}"
        print(error_msg)
        return error_msg