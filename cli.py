#!/usr/bin/env python3
# 安塞剪纸智能体命令行界面

import os
import argparse
import sys
from agent import PapercutAgent

def print_banner():
    """打印欢迎横幅"""
    banner = """
    ==========================================
            ✂️  安塞剪纸智能体命令行界面
    ==========================================
    """
    print(banner)

def print_help():
    """打印帮助信息"""
    help_text = """
可用命令：
  recognize <image_path>   - 识别剪纸图像
  knowledge <query>        - 查询剪纸纹样知识
  design <theme>           - 生成设计方案（theme: wedding/festival/random）
  chat <message>           - 与智能体聊天
  exit/quit                - 退出程序
  help                     - 显示帮助信息
    """
    print(help_text)

def setup_environment():
    """设置环境变量"""
    if "sk-d336ed913a0f4cd5a823aad14359fa3f" not in os.environ:
        api_key = input("请输入您的DeepSeek API密钥: ")
        os.environ["sk-d336ed913a0f4cd5a823aad14359fa3f"] = api_key

def main():
    """主函数"""
    print_banner()
    
    # 设置环境
    setup_environment()
    
    # 创建智能体实例
    try:
        agent = PapercutAgent()
        print("智能体初始化成功！\n")
    except Exception as e:
        print(f"智能体初始化失败: {str(e)}")
        return
    
    print_help()
    
    # 命令行交互循环
    while True:
        try:
            # 获取用户输入
            user_input = input("\n请输入命令: ").strip()
            
            if not user_input:
                continue
            
            # 解析命令
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            # 处理命令
            if command in ["exit", "quit", "退出", "结束"]:
                print("\n感谢使用安塞剪纸智能体，再见！")
                break
            
            elif command == "help":
                print_help()
            
            elif command == "recognize":
                if not args:
                    print("错误: 请指定图像路径")
                    continue
                
                if not os.path.exists(args):
                    print(f"错误: 图像文件不存在: {args}")
                    continue
                
                print(f"正在识别图像: {args}")
                query = f"识别这张剪纸图像: {args}"
                response = agent.run(query)
                print(f"\n识别结果: {response}")
            
            elif command == "knowledge":
                if not args:
                    print("错误: 请输入查询内容")
                    continue
                
                print(f"正在查询知识: {args}")
                query = f"查询关于{args}的剪纸纹样信息"
                response = agent.run(query)
                print(f"\n查询结果: {response}")
            
            elif command == "design":
                if not args:
                    print("错误: 请指定设计主题")
                    print("可用主题: wedding(婚礼), festival(节日), random(随机)")
                    continue
                
                theme = args.lower()
                if theme not in ["wedding", "festival", "random"]:
                    print("错误: 无效的设计主题")
                    print("可用主题: wedding(婚礼), festival(节日), random(随机)")
                    continue
                
                themes = {
                    "wedding": "婚礼",
                    "festival": "节日",
                    "random": "随机"
                }
                
                print(f"正在生成{themes[theme]}主题的设计方案")
                query = f"请生成一个{themes[theme]}主题的剪纸设计方案"
                response = agent.run(query)
                print(f"\n设计方案: {response}")
            
            elif command == "chat":
                if not args:
                    print("错误: 请输入聊天内容")
                    continue
                
                print("智能体正在思考...")
                response = agent.run(args)
                print(f"\n智能体回答: {response}")
            
            else:
                print(f"错误: 未知命令 '{command}'")
                print("输入 'help' 查看可用命令")
                
        except KeyboardInterrupt:
            print("\n\n用户中断操作，程序退出。")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            print("请检查您的输入或网络连接后重试。")

if __name__ == "__main__":
    main()
