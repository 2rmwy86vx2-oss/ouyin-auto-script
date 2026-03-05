import openai

# 火山方舟豆包API配置
api_key = "27fc07b9-50cf-4ad8-8398-24ee31d2e385"
base_url = "https://ark.cn-beijing.volces.com/api/v3"
model_id = "ep-20260305211700-bfn2m"

def gen_douyin_script():
    # 初始化客户端
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    try:
        # 发送请求给豆包
        msg = [{"role": "user", "content": 
"生成一个抓取抖音公开点赞过万视频的Python脚本，带异常处理"}]
        res = client.chat.completions.create(model=model_id, messages=msg)
        # 保存生成的脚本
        with open("douyin_crawl.py", "w", encoding="utf-8") as f:
            f.write(res.choices[0].message.content)
        print("✅ 脚本生成成功！")
        return True
    except Exception as e:
        print(f"❌ 失败原因：{e}")
        return False

if __name__ == "__main__":
    gen_douyin_script()
