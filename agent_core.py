# 安塞剪纸智能体核心模块
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import json

# 导入新创建的工具
from image_tool import ImageRecognitionTool
from knowledge_tool import KnowledgeTool
from design_tool import DesignTool

# 初始化工具
image_tool = ImageRecognitionTool()
knowledge_tool = KnowledgeTool()
design_tool = DesignTool()

# 定义剪纸类别
class_names = ['人物', '其他', '动物', '艺术剪纸', '花草']

# 简单的设计建议生成函数
def generate_design_suggestions(category, user_request=""):
    """
    生成简单的剪纸设计建议
    :param category: 剪纸类别
    :param user_request: 用户的设计需求
    :return: 设计建议
    """
    if '人物' in category:
        return "人物类剪纸建议：可以结合传统人物形象，如寿星、娃娃等，添加吉祥图案作为背景"
    elif '动物' in category:
        return "动物类剪纸建议：可以设计成双成对的动物，如龙凤、鸳鸯等，象征吉祥如意"
    elif '花草' in category:
        return "花草类剪纸建议：可以选择牡丹、莲花等吉祥花卉，搭配藤蔓和叶子增加层次感"
    elif '艺术剪纸' in category:
        return "艺术剪纸建议：可以尝试抽象化设计，结合几何图案和传统纹样，创造独特风格"
    else:
        return "剪纸设计建议：可以参考传统剪纸纹样，结合现代元素，创造富有创意的作品"

class PapercutAgent:
    """安塞剪纸智能体类"""
    
    def __init__(self):
        self.image_tool = image_tool
        self.knowledge_tool = knowledge_tool
        self.design_tool = design_tool
        self.class_names = class_names
    
    def recognize_papercut(self, image_path):
        """
        识别剪纸纹样类别
        :param image_path: 剪纸图像路径
        :return: 识别结果（类别名称和置信度）
        """
        return self.image_tool.predict(image_path)
    
    def get_design_suggestions(self, category, user_request=""):
        """
        获取剪纸设计建议
        :param category: 剪纸类别
        :param user_request: 用户的设计需求
        :return: 设计建议
        """
        return generate_design_suggestions(category, user_request)
    
    def get_knowledge_info(self, pattern_name=None, region_name=None):
        """
        获取剪纸纹样的知识库信息
        :param pattern_name: 纹样名称
        :param region_name: 地区名称
        :return: 知识库信息
        """
        if pattern_name:
            return self.knowledge_tool.get_pattern_by_name(pattern_name)
        elif region_name:
            return self.knowledge_tool.get_region_info(region_name)
        else:
            return "请提供纹样名称或地区名称来查询知识库"
    
    def get_combination_design(self, theme="wedding", custom_patterns=None):
        """
        获取组合设计方案
        :param theme: 设计主题（wedding, festival, custom, random）
        :param custom_patterns: 自定义纹样列表（仅当theme="custom"时使用）
        :return: 组合设计方案
        """
        if theme == "wedding":
            return self.design_tool.get_wedding_combination()
        elif theme == "festival":
            return self.design_tool.get_festival_combination()
        elif theme == "custom" and custom_patterns:
            return self.design_tool.get_custom_combination(custom_patterns)
        else:
            return self.design_tool.get_random_combination()
    
    def analyze_and_design(self, image_path, user_request=""):
        """
        完整的分析和设计流程
        :param image_path: 剪纸图像路径
        :param user_request: 用户的设计需求
        :return: 完整的分析和设计结果
        """
        # 识别剪纸
        recognition_result = self.recognize_papercut(image_path)
        
        # 获取设计建议
        design_suggestions = self.get_design_suggestions(
            recognition_result['category'],
            user_request
        )
        
        # 根据识别结果尝试获取相关知识库信息
        category = recognition_result['category']
        related_patterns = self.knowledge_tool.search_patterns(category)
        
        return {
            'recognition': recognition_result,
            'design_suggestions': design_suggestions,
            'related_patterns': related_patterns[:3]  # 返回前3个相关纹样
        }

# 初始化智能体
agent = PapercutAgent()

# 测试函数
if __name__ == "__main__":
    print("=== 安塞剪纸智能体测试 ===")
    
    # 测试1：图像识别
    test_image_path = './动物/1.png'
    if os.path.exists(test_image_path):
        result = agent.recognize_papercut(test_image_path)
        print(f"\n1. 图像识别测试：")
        print(f"   识别结果：{result['category']}")
        print(f"   置信度：{result['confidence']:.2f}")
        
        # 测试设计建议
        suggestions = agent.get_design_suggestions(result['category'], "我想要一个适合春节的设计")
        print(f"   设计建议：{suggestions}")
    else:
        print(f"\n1. 图像识别测试：")
        print(f"   测试图像不存在：{test_image_path}")
    
    # 测试知识库查询
    print(f"\n2. 知识库查询测试：")
    # 测试地区信息查询
    region_info = agent.get_knowledge_info(region_name="安塞")
    if region_info:
        if isinstance(region_info, list) and region_info:
            region_info = region_info[0]
        if isinstance(region_info, dict):
            print(f"   安塞地区信息：{region_info.get('name', '未知')} - {region_info.get('description', '')[:50]}...")
    
    # 测试纹样查询
    fish_pattern = agent.get_knowledge_info(pattern_name="鱼纹")
    if fish_pattern:
        if isinstance(fish_pattern, list) and fish_pattern:
            fish_pattern = fish_pattern[0]
        if isinstance(fish_pattern, dict):
            print(f"   鱼纹信息：{fish_pattern.get('name', '未知')} - 象征{fish_pattern.get('symbolism', '未知')}")
    
    # 测试3：组合设计方案
    print(f"\n3. 组合设计方案测试：")
    wedding_design = agent.get_combination_design(theme="wedding")
    if 'patterns' in wedding_design and wedding_design['patterns']:
        print(f"   婚礼主题设计包含纹样：{', '.join([pattern['name'] for pattern in wedding_design['patterns']])}")
    if 'layout' in wedding_design:
        print(f"   设计布局：{wedding_design['layout']}")
    if 'colors' in wedding_design:
        print(f"   色彩建议：{', '.join(wedding_design['colors'])}")
    
    festival_design = agent.get_combination_design(theme="festival")
    if 'patterns' in festival_design and festival_design['patterns']:
        print(f"   节日主题设计包含纹样：{', '.join([pattern['name'] for pattern in festival_design['patterns']])}")
    if 'layout' in festival_design:
        print(f"   设计布局：{festival_design['layout']}")
    if 'colors' in festival_design:
        print(f"   色彩建议：{', '.join(festival_design['colors'])}")
    
    # 测试4：完整分析设计流程
    if os.path.exists(test_image_path):
        print(f"\n4. 完整分析设计流程测试：")
        complete_result = agent.analyze_and_design(test_image_path, "我想要一个现代风格的设计")
        print(f"   识别结果：{complete_result['recognition']['category']}")
        print(f"   设计建议：{complete_result['design_suggestions']}")
        print(f"   相关纹样：{', '.join([p['name'] for p in complete_result['related_patterns']])}")
    
    print(f"\n=== 测试完成 ===")
