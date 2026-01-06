import os

# 检查依赖是否安装
try:
    from agent import PapercutAgent
    HAS_DEPENDENCIES = True
except ImportError as e:
    HAS_DEPENDENCIES = False
    DEPENDENCY_ERROR = str(e)

def main():
    """
    安塞剪纸智能体主程序
    实现与智能体的交互循环
    """
    print("=" * 50)
    print("        安塞剪纸智能体")
    print("=" * 50)
    print("功能介绍：")
    print("1. 剪纸图像识别：识别上传的剪纸图像")
    print("2. 纹样知识查询：查询安塞剪纸的纹样信息")
    print("3. 设计方案生成：生成各种主题的剪纸设计方案")
    print("\n输入 'exit' 或 'quit' 退出程序")
    print("=" * 50)
    
    # 检查并设置DeepSeek API密钥
    if "DEEPSEEK_API_KEY" not in os.environ:
        api_key = input("\n请输入您的DeepSeek API密钥: ")
        os.environ["DEEPSEEK_API_KEY"] = api_key
    
    # 检查依赖
    if not HAS_DEPENDENCIES:
        print(f"\n依赖缺失: {DEPENDENCY_ERROR}")
        print("请先安装必要的依赖：")
        print("pip install langchain langchain_openai")
        return
    
    # 创建智能体实例
    try:
        agent = PapercutAgent()
        print("\n智能体初始化成功！")
    except Exception as e:
        print("智能体初始化失败: {str(e)}")
        print("可能的原因：")
        print("1. DeepSeek API密钥无效")
        print("2. 网络连接问题")
        print("3. 依赖版本不兼容")
        return
    
    # 初始化对话历史
    chat_history = ""
    
    # 交互循环
    while True:
        try:
            # 获取用户输入
            user_input = input("\n请输入您的问题: ")
            
            # 检查退出条件
            if user_input.lower() in ["exit", "quit", "退出", "结束"]:
                print("\n感谢使用安塞剪纸智能体，再见！")
                break
            
            # 检查输入是否为空
            if not user_input.strip():
                print("\n请输入有效的问题！")
                continue
            
            # 运行智能体
            print("\n智能体正在思考，请稍候...")
            response = agent.run(user_input, chat_history)
            
            # 打印智能体回答
            print(f"\n智能体回答: {response}")
            
            # 更新对话历史
            chat_history += f"用户: {user_input}\n智能体: {response}\n"
            
        except KeyboardInterrupt:
            # 处理用户中断（Ctrl+C）
            print("\n\n用户中断操作，程序退出。")
            break
        except Exception as e:
            # 处理其他异常
            print(f"\n发生错误: {str(e)}")
            print("请检查您的输入或网络连接后重试。")

if __name__ == "__main__":
    main()
