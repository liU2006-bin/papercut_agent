from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os
import re

# 尝试导入tools，形成多层防御
HAS_TOOLS = False
try:
    from tools import tools
    HAS_TOOLS = True
except ImportError as e:
    print(f"Warning: Failed to import tools: {e}")
    # 定义一个空的tools列表作为备用
    tools = []

class PapercutAgent:
    def __init__(self, model_name="deepseek-chat", temperature=0.7):
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise Exception("请设置DEEPSEEK_API_KEY环境变量")
        
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        
        self.tools_dict = {tool.name: tool for tool in tools}
        
        self.system_prompt = """你是一个安塞剪纸智能体，擅长剪纸图像识别、纹样知识查询和设计方案生成。

你具备多维标注功能，可以从四个维度理解剪纸纹样：
1. 内容/对象维度：描述图像中的客观实体，包括纹样主体、辅助元素、构图结构
2. 形式/视觉维度：描述视觉呈现特征与技法，包括线条风格、镂空技法、色彩、纸张纹理
3. 文化/语义维度：解释纹样的文化内涵与寓意，包括吉祥寓意、民俗用途、地域特色、神话传说关联
4. 关联/情境维度：构建纹样的关系网，包括传承人信息、创作年代、地域流派、相似纹样链接、当代应用案例

**回答格式要求（重要）：**
- 不同内容之间必须换行
- 使用空行分隔不同主题或段落
- 列表项之间换行
- 标题和内容之间换行
- 保持段落清晰，便于阅读

可用的工具：
{tools_list}

当你需要调用工具时，请使用以下 XML 格式：
<tool_call>
<tool_name>工具名称</tool_name>
<tool_input>输入参数</tool_input>
</tool_call>

如果你不确定如何回答某些问题，可以调用相关工具来获取信息。
"""
        

    
    def _get_available_tools(self):
        tools_list = []
        for tool in tools:
            tools_list.append(f"- {tool.name}: {tool.description}")
        # 将换行符替换为空格，避免LangChain模板解析问题
        return " ".join(tools_list)
    
    def _call_tool(self, tool_name, input_str):
        if tool_name in self.tools_dict:
            try:
                return self.tools_dict[tool_name].func(input_str)
            except Exception as e:
                return f"工具调用失败: {str(e)}"
        return f"未知工具: {tool_name}"
    
    def run(self, query: str, chat_history: str = "") -> str:
        try:
            # 构建消息列表
            system_message = self.system_prompt.format(tools_list=self._get_available_tools())
            messages = [
                SystemMessage(content=system_message),
                HumanMessage(content=query)
            ]
            
            # 添加历史对话
            if chat_history:
                messages.insert(1, HumanMessage(content=f"历史对话：{chat_history}"))
            
            # 第一轮：发送问题给 LLM
            response = self.llm.invoke(messages).content
            
            # 检查是否需要调用工具
            max_iterations = 3
            iteration = 0
            
            while "<tool_call>" in response and "</tool_call>" in response and iteration < max_iterations:
                iteration += 1
                
                # 解析工具调用
                tool_pattern = r'<tool_name>(.*?)</tool_name>.*?<tool_input>(.*?)</tool_input>'
                matches = re.findall(tool_pattern, response, re.DOTALL)
                
                if not matches:
                    break
                
                # 调用所有工具
                tool_results = []
                for tool_name, input_str in matches:
                    tool_name = tool_name.strip()
                    input_str = input_str.strip()
                    result = self._call_tool(tool_name, input_str)
                    tool_results.append(f"工具 [{tool_name}] 的结果：\n{result}")
                
                # 将工具结果返回给 LLM，让它生成最终回答
                results_text = "\n\n".join(tool_results)
                
                # 构建包含工具结果的对话
                messages_with_results = messages.copy()
                # 添加 AI 的工具调用意图
                messages_with_results.append(AIMessage(content=response))
                # 添加工具结果
                messages_with_results.append(HumanMessage(content=f"以下是工具调用结果：\n{results_text}\n\n请根据工具结果，用清晰的格式回答用户的问题。"))
                
                # 直接调用LLM，避免使用ChatPromptTemplate
                response = self.llm.invoke(messages_with_results).content
            
            return response
        except Exception as e:
            return f"智能体执行失败: {str(e)}"

if __name__ == "__main__":
    if "DEEPSEEK_API_KEY" not in os.environ:
        os.environ["DEEPSEEK_API_KEY"] = input("请输入您的DeepSeek API密钥: ")
    
    agent = PapercutAgent()
    test_query = "请生成一个婚礼主题的剪纸设计方案"
    print(f"测试查询: {test_query}")
    response = agent.run(test_query)
    print(f"智能体回答: {response}")
