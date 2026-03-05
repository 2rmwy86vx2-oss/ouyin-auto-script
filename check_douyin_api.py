import requests
import json
import os
import subprocess
from openai import OpenAI

# 配置项
DOUYIN_TEST_URL = "https://www.douyin.com/api/v2/feed/list/"
LIKE_THRESHOLD = 10000  # 点赞过万阈值
AI_API_KEY = os.getenv("AI_API_KEY")  # 从GitHub Secrets读取
AI_BASE_URL = "https://api.doubao.com/v1"
GITHUB_USERNAME = os.getenv("GH_USERNAME")  # GitHub用户名（Secrets配置）
GITHUB_EMAIL = os.getenv("GH_EMAIL")  # GitHub邮箱（Secrets配置）
# 检测接口是否可用
def check_api():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(DOUYIN_TEST_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ 抖音接口正常，无需更新脚本")
            return True
        else:
            print(f"❌ 接口失效，状态码：{response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 接口访问失败：{str(e)}")
        return False

# 调用AI生成新脚本
def generate_new_script():
    if not AI_API_KEY:
        print("❌ 未配置AI API Key，无法生成新脚本")
        return False
    
    try:
        client = OpenAI(
            api_key=AI_API_KEY,
            base_url=AI_BASE_URL
        )
        prompt = f"""
        抖音接口 {DOUYIN_TEST_URL} 失效了，请生成2026年最新的Python抓取脚本，要求：
        1. 抓取抖音公开的视频流，筛选点赞数≥{LIKE_THRESHOLD}的视频
        2. 包含接口异常处理、视频下载功能（保存到本地douyin_videos文件夹）
        3. 代码可直接运行，带详细注释，兼容Python 3.8+
        4. 避免使用已失效的接口，优先用抖音web端可用的公开接口
        """
        response = client.chat.completions.create(
            model="doubao-pro",
            messages=[{"role": "user", "content": prompt}]
        )
        new_script = response.choices[0].message.content
        
        # 保存新脚本到文件
        with open("douyin_download.py", "w", encoding="utf-8") as f:
            f.write(new_script)
        print("✅ AI已生成新脚本：douyin_download.py")
        return True
    except Exception as e:
        print(f"❌ AI生成脚本失败：{str(e)}")
        return False

# 自动提交新脚本到GitHub
def commit_and_push():
    if not (GITHUB_USERNAME and GITHUB_EMAIL):
        print("❌ 未配置GitHub用户名或邮箱，无法提交代码")
        return False
    
    try:
        # 配置Git用户信息
        subprocess.run(["git", "config", "--global", "user.name", GITHUB_USERNAME], check=True)
        subprocess.run(["git", "config", "--global", "user.email", GITHUB_EMAIL], check=True)
        
        # 提交并推送
        subprocess.run(["git", "add", "douyin_download.py"], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update: 接口失效，AI生成新脚本"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ 新脚本已自动提交到GitHub仓库")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败：{str(e)}")
        return False

if __name__ == "__main__":
    if not check_api():
        if generate_new_script():
            commit_and_push()
