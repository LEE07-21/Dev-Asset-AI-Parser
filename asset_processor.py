import json
import os
import pandas as pd
pd.set_option("display.show_dimensions", False)
def asset_parser(file_path_1, file_path_2):
    """抓取设备信息"""
    found = []
    missing = []
    file_path_1 = "old-assets.json"
    file_path_2 = "new-assets.json"
    print("正在读取设备资产信息 [old-assets] 和 [new-assets]。。。")
    print("-" * 130)
    for path in [file_path_1, file_path_2]:
        if os.path.exists(path):
            found.append(path)
        else:
            missing.append(path)
    if missing:
        raise FileNotFoundError(f"未找到文件{missing},请检查路径是否正确！")
    with open(file_path_1, mode="r", encoding="utf-8") as f:
        old_device_list = json.load(f)
        print(f"[✓] 成功从 {file_path_1} 加载了 {len(old_device_list)} 台设备信息：")
        for dev in old_device_list:
            print(f" -> 发现设备: {dev['hostname']} | 厂商：{dev['vendor']} | dev_ID: {dev['device_id']} | 型号：{dev['model']} | IP: {dev['ip']} | 状态: {dev['status']} | 位置：{dev['location']}")
        print("-" * 130)
    with open(file_path_2, mode="r", encoding="utf-8") as f:
        new_device_list = json.load(f)
        print(f"[✓] 成功从 {file_path_2} 加载了 {len(new_device_list)} 台设备信息：")
        for dev in new_device_list:
            print(f" -> 发现设备: {dev['hostname']} | 厂商：{dev['vendor']} | dev_ID: {dev['device_id']} | 型号：{dev['model']} | IP: {dev['ip']} | 状态: {dev['status']} | 位置：{dev['location']}")
        print("-" * 130)
    return old_device_list, new_device_list

def asset_diff(old_device_list, new_device_list):
    """设备信息DIFF"""
    df_1 = pd.DataFrame(old_device_list)
    df_2 = pd.DataFrame(new_device_list)
    clean_df_1 = df_1.drop_duplicates(keep="first")
    if df_1.duplicated().any():
        print("old_assets有重复内容！查重后如下表old_new_assets：")
        print(clean_df_1)
        print("-" * 100)
    else:
        print("old_dev无重复内容！")
        print("-" * 100)
    clean_df_2 = df_2.drop_duplicates(keep="first")
    if df_2.duplicated().any():
        print("new_assets有重复内容！查重后如下表clean_new_assets：")
        print(clean_df_2)
        print("-" * 100)
    else:
        print("new_dev无重复内容！")
        print("-" * 100)
    old_ids = set(clean_df_1["device_id"])
    new_ids = set(clean_df_2["device_id"])
    added_ids = new_ids - old_ids
    removed_ids = old_ids - new_ids
    added_devs = clean_df_2[clean_df_2["device_id"].isin(added_ids)].to_dict(
        orient="records"
    )
    removed_devs = clean_df_1[clean_df_1["device_id"].isin(removed_ids)].to_dict(
        orient="records"
    )
    diff_result = {
        "added": added_devs,
        "removed": removed_devs,
    }
    return diff_result


if __name__ == "__main__":
    try:
        old_data , new_data = asset_parser("old-assets.json","new-assets.json")
        diff_result = asset_diff(old_data, new_data)
        print("比对完成：",)
        add_ids = [dev["device_id"] for dev in diff_result["added"]]
        print(f"新增设备：{add_ids}")
        remove_ids = [dev["device_id"] for dev in diff_result["removed"]]
        print(f"下线设备：{remove_ids}")
        print("-" * 100)
    except FileNotFoundError as e:
        print(f"[x] 错误：{e}")
        print("-" * 100)
    except json.JSONDecodeError:
        print(f"[✗] 错误：不是合法的 JSON 格式，解析失败！")
        print("-" * 100)