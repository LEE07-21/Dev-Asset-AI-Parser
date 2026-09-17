from asset_processor import asset_parser
from asset_processor import asset_diff
from AI_Call import run_agent

def show_menu():
    print("-" * 41)
    print(" =========大模型API分析设备资产工具=========")
    print("-" * 41)
    print("0. 退出系统")
    print("1. 进行设备资产信息抓取与差异审计")
    print("2. 调用AI进行设备信息分析")
    print("-" * 41)

def main():

    while True:
        show_menu()
        choice = input("请选择要执行的操作 (0-2): ").strip()

        if choice == "1":
            print("\n进行设备信息抓取与差异审计...")
            try:
                old_data, new_data = asset_parser(
                    "old-assets.json", "new-assets.json"
                )
                diff_result = asset_diff(old_data, new_data)
                print("比对完成：", )
                add_ids = [dev["device_id"] for dev in diff_result["added"]]
                print(f"新增设备：{add_ids}")
                remove_ids = [dev["device_id"] for dev in diff_result["removed"]]
                print(f"下线设备：{remove_ids}")
                print("-" * 130)
            except Exception as e:
                print(f"处理失败，原因: {e}")


        elif choice == "2":
            print("\n正在调用AI...")
            user_prompt = input(
                "请输入你要向 AI 咨询的问题 (回车默认审计old/new差异): "
            ).strip()
            if not user_prompt:
                user_prompt = "帮我对比一下 old-assets.json 和 new-assets.json 这两份巡检数据，分析一下资产变动风险。"
            try:
                results = run_agent(user_prompt)
            except Exception as e:
                print(f"AI 分析失败，原因: {e}")

        elif choice == "0":
            print("\n感谢使用，系统已安全退出！")
            break

        else:
            print("\n输入有误，请输入有效的选项 (0, 1, 2)！")


if __name__ == "__main__":
    main()