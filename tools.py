from langchain_core.tools import Tool
from image_tool import ImageRecognitionTool
from knowledge_tool import KnowledgeTool
from design_tool import DesignTool
from multidimensional_annotation_tool import MultiDimensionalAnnotationTool
import json

# 初始化工具实例
image_tool = ImageRecognitionTool()
knowledge_tool = KnowledgeTool()
design_tool = DesignTool()
multidimensional_annotation_tool = MultiDimensionalAnnotationTool()

# 创建工具列表
def create_tools():
    tools = []
    
    # 1. 图像识别工具
    def recognize_image(image_path: str) -> str:
        """
        识别剪纸图像的类别
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            JSON格式的识别结果，包含类别名称、置信度等信息
        """
        try:
            result = image_tool.predict(image_path)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"图像识别失败: {str(e)}"
    
    tools.append(
        Tool(
            name="recognize_image",
            func=recognize_image,
            description="用于识别剪纸图像的类别，输入图像文件路径，返回识别结果"
        )
    )
    
    # 2. 知识库查询工具 - 根据ID查询纹样
    def get_pattern_by_id(pattern_id: str) -> str:
        """
        根据纹样ID查询纹样信息
        
        Args:
            pattern_id: 纹样ID，如 'pattern_001'
            
        Returns:
            JSON格式的纹样信息，包含名称、象征意义、用途等
        """
        try:
            result = knowledge_tool.get_pattern_by_id(pattern_id)
            if result:
                return json.dumps(result, ensure_ascii=False, indent=2)
            else:
                return f"未找到ID为 {pattern_id} 的纹样"
        except Exception as e:
            return f"查询失败: {str(e)}"
    
    tools.append(
        Tool(
            name="get_pattern_by_id",
            func=get_pattern_by_id,
            description="根据纹样ID查询纹样详细信息，输入纹样ID，返回纹样信息"
        )
    )
    
    # 3. 知识库查询工具 - 根据名称查询纹样
    def get_pattern_by_name(pattern_name: str) -> str:
        """
        根据纹样名称查询纹样信息
        
        Args:
            pattern_name: 纹样名称，如 '鱼纹'
            
        Returns:
            JSON格式的纹样信息列表，包含名称、象征意义、用途等
        """
        try:
            results = knowledge_tool.get_pattern_by_name(pattern_name)
            if results:
                return json.dumps(results, ensure_ascii=False, indent=2)
            else:
                return f"未找到名称为 {pattern_name} 的纹样"
        except Exception as e:
            return f"查询失败: {str(e)}"
    
    tools.append(
        Tool(
            name="get_pattern_by_name",
            func=get_pattern_by_name,
            description="根据纹样名称查询纹样详细信息，输入纹样名称，返回纹样信息列表"
        )
    )
    
    # 4. 知识库查询工具 - 搜索纹样
    def search_patterns(keyword: str) -> str:
        """
        根据关键词搜索相关纹样
        
        Args:
            keyword: 搜索关键词，如 '吉祥'、'福'
            
        Returns:
            JSON格式的匹配纹样列表
        """
        try:
            results = knowledge_tool.search_patterns(keyword)
            if results:
                return json.dumps(results, ensure_ascii=False, indent=2)
            else:
                return f"未找到包含关键词 '{keyword}' 的纹样"
        except Exception as e:
            return f"搜索失败: {str(e)}"
    
    tools.append(
        Tool(
            name="search_patterns",
            func=search_patterns,
            description="根据关键词搜索相关纹样，输入关键词，返回匹配的纹样列表"
        )
    )
    
    # 5. 设计工具 - 婚礼主题设计
    def get_wedding_design() -> str:
        """
        获取婚礼主题的剪纸组合设计方案
        
        Returns:
            JSON格式的设计方案，包含纹样组合、布局建议、颜色建议等
        """
        try:
            result = design_tool.get_wedding_combination()
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"生成婚礼设计方案失败: {str(e)}"
    
    tools.append(
        Tool(
            name="get_wedding_design",
            func=get_wedding_design,
            description="获取婚礼主题的剪纸组合设计方案，返回包含纹样组合、布局和颜色建议的设计方案"
        )
    )
    
    # 6. 设计工具 - 节日主题设计
    def get_festival_design(festival: str = "春节") -> str:
        """
        获取节日主题的剪纸组合设计方案
        
        Args:
            festival: 节日名称，默认是'春节'
            
        Returns:
            JSON格式的设计方案，包含纹样组合、布局建议、颜色建议等
        """
        try:
            result = design_tool.get_festival_combination(festival)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"生成节日设计方案失败: {str(e)}"
    
    tools.append(
        Tool(
            name="get_festival_design",
            func=get_festival_design,
            description="获取节日主题的剪纸组合设计方案，输入节日名称（默认为春节），返回设计方案"
        )
    )
    
    # 7. 设计工具 - 随机组合设计
    def get_random_design() -> str:
        """
        获取随机组合的剪纸设计方案
        
        Returns:
            JSON格式的设计方案，包含纹样组合、布局建议、颜色建议等
        """
        try:
            result = design_tool.get_random_combination()
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"生成随机设计方案失败: {str(e)}"
    
    tools.append(
        Tool(
            name="get_random_design",
            func=get_random_design,
            description="获取随机组合的剪纸设计方案，返回包含纹样组合、布局和颜色建议的设计方案"
        )
    )
    
    # 8. 多维标注工具 - 标注剪纸图像
    def annotate_papercut_multidimensionally(image_path: str) -> str:
        """
        对剪纸图像进行多维标注
        
        Args:
            image_path: 剪纸图像的路径
            
        Returns:
            JSON格式的多维标注结果，包括内容/对象、形式/视觉、文化/语义、关联/情境四个维度
        """
        try:
            result = multidimensional_annotation_tool.annotate(image_path)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"标注失败: {str(e)}"
    
    tools.append(
        Tool(
            name="annotate_papercut_multidimensionally",
            func=annotate_papercut_multidimensionally,
            description="对剪纸图像进行多维标注，包括内容/对象、形式/视觉、文化/语义、关联/情境四个维度，输入图像路径，返回标注结果"
        )
    )
    
    # 9. 多维标注工具 - 根据标注生成组合建议
    def generate_combination_from_annotation(annotation_result: str, theme: str = None) -> str:
        """
        根据多维标注结果生成剪纸组合设计建议
        
        Args:
            annotation_result: JSON格式的多维标注结果
            theme: 可选的设计主题
            
        Returns:
            JSON格式的组合设计建议，包括纹样组合、布局建议、颜色建议等
        """
        try:
            # 解析JSON字符串为字典
            annotation_dict = json.loads(annotation_result)
            result = multidimensional_annotation_tool.generate_combination_suggestions(annotation_dict, theme)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except json.JSONDecodeError as e:
            return f"标注结果格式错误: {str(e)}"
        except Exception as e:
            return f"生成组合建议失败: {str(e)}"
    
    tools.append(
        Tool(
            name="generate_combination_from_annotation",
            func=generate_combination_from_annotation,
            description="根据多维标注结果生成剪纸组合设计建议，输入JSON格式的标注结果和可选的设计主题，返回组合设计建议"
        )
    )
    
    return tools

# 导出工具列表
tools = create_tools()
from langchain_core.tools import Tool
from image_tool import ImageRecognitionTool
from knowledge_tool import KnowledgeTool
from design_tool import DesignTool
from multidimensional_annotation_tool import MultiDimensionalAnnotationTool
import json

# 初始化工具实例
image_tool = ImageRecognitionTool()
knowledge_tool = KnowledgeTool()
design_tool = DesignTool()
multidimensional_annotation_tool = MultiDimensionalAnnotationTool()

# 创建工具列表
def create_tools():
    tools = []
    
    # 1. 图像识别工具
    def recognize_image(image_path: str) -> str:
        """
        识别剪纸图像的类别
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            JSON格式的识别结果，包含类别名称、置信度等信息
        """
        try:
            result = image_tool.predict(image_path)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"图像识别失败: {str(e)}"
    
    tools.append(
        Tool(
            name="recognize_image",
            func=recognize_image,
            description="用于识别剪纸图像的类别，输入图像文件路径，返回识别结果"
        )
    )
    
    # 2. 知识库查询工具 - 根据ID查询纹样
    def get_pattern_by_id(pattern_id: str) -> str:
        """
        根据纹样ID查询纹样信息
        
        Args:
            pattern_id: 纹样ID，如 'pattern_001'
            
        Returns:
            JSON格式的纹样信息，包含名称、象征意义、用途等
        """
        try:
            result = knowledge_tool.get_pattern_by_id(pattern_id)
            if result:
                return json.dumps(result, ensure_ascii=False, indent=2)
            else:
                return f"未找到ID为 {pattern_id} 的纹样"
        except Exception as e:
            return f"查询失败: {str(e)}"
    
    tools.append(
        Tool(
            name="get_pattern_by_id",
            func=get_pattern_by_id,
            description="根据纹样ID查询纹样详细信息，输入纹样ID，返回纹样信息"
        )
    )
    
    # 3. 知识库查询工具 - 根据名称查询纹样
    def get_pattern_by_name(pattern_name: str) -> str:
        """
        根据纹样名称查询纹样信息
        
        Args:
            pattern_name: 纹样名称，如 '鱼纹'
            
        Returns:
            JSON格式的纹样信息列表，包含名称、象征意义、用途等
        """
        try:
            results = knowledge_tool.get_pattern_by_name(pattern_name)
            if results:
                return json.dumps(results, ensure_ascii=False, indent=2)
            else:
                return f"未找到名称为 {pattern_name} 的纹样"
        except Exception as e:
            return f"查询失败: {str(e)}"
    
    tools.append(
        Tool(
            name="get_pattern_by_name",
            func=get_pattern_by_name,
            description="根据纹样名称查询纹样详细信息，输入纹样名称，返回纹样信息列表"
        )
    )
    
    # 4. 知识库查询工具 - 搜索纹样
    def search_patterns(keyword: str) -> str:
        """
        根据关键词搜索相关纹样
        
        Args:
            keyword: 搜索关键词，如 '吉祥'、'福'
            
        Returns:
            JSON格式的匹配纹样列表
        """
        try:
            results = knowledge_tool.search_patterns(keyword)
            if results:
                return json.dumps(results, ensure_ascii=False, indent=2)
            else:
                return f"未找到包含关键词 '{keyword}' 的纹样"
        except Exception as e:
            return f"搜索失败: {str(e)}"
    
    tools.append(
        Tool(
            name="search_patterns",
            func=search_patterns,
            description="根据关键词搜索相关纹样，输入关键词，返回匹配的纹样列表"
        )
    )
    
    # 5. 设计工具 - 婚礼主题设计
    def get_wedding_design() -> str:
        """
        获取婚礼主题的剪纸组合设计方案
        
        Returns:
            JSON格式的设计方案，包含纹样组合、布局建议、颜色建议等
        """
        try:
            result = design_tool.get_wedding_combination()
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"生成婚礼设计方案失败: {str(e)}"
    
    tools.append(
        Tool(
            name="get_wedding_design",
            func=get_wedding_design,
            description="获取婚礼主题的剪纸组合设计方案，返回包含纹样组合、布局和颜色建议的设计方案"
        )
    )
    
    # 6. 设计工具 - 节日主题设计
    def get_festival_design(festival: str = "春节") -> str:
        """
        获取节日主题的剪纸组合设计方案
        
        Args:
            festival: 节日名称，默认是'春节'
            
        Returns:
            JSON格式的设计方案，包含纹样组合、布局建议、颜色建议等
        """
        try:
            result = design_tool.get_festival_combination(festival)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"生成节日设计方案失败: {str(e)}"
    
    tools.append(
        Tool(
            name="get_festival_design",
            func=get_festival_design,
            description="获取节日主题的剪纸组合设计方案，输入节日名称（默认为春节），返回设计方案"
        )
    )
    
    # 7. 设计工具 - 随机组合设计
    def get_random_design() -> str:
        """
        获取随机组合的剪纸设计方案
        
        Returns:
            JSON格式的设计方案，包含纹样组合、布局建议、颜色建议等
        """
        try:
            result = design_tool.get_random_combination()
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"生成随机设计方案失败: {str(e)}"
    
    tools.append(
        Tool(
            name="get_random_design",
            func=get_random_design,
            description="获取随机组合的剪纸设计方案，返回包含纹样组合、布局和颜色建议的设计方案"
        )
    )
    
    # 8. 多维标注工具 - 标注剪纸图像
    def annotate_papercut_multidimensionally(image_path: str) -> str:
        """
        对剪纸图像进行多维标注
        
        Args:
            image_path: 剪纸图像的路径
            
        Returns:
            JSON格式的多维标注结果，包括内容/对象、形式/视觉、文化/语义、关联/情境四个维度
        """
        try:
            result = multidimensional_annotation_tool.annotate(image_path)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"标注失败: {str(e)}"
    
    tools.append(
        Tool(
            name="annotate_papercut_multidimensionally",
            func=annotate_papercut_multidimensionally,
            description="对剪纸图像进行多维标注，包括内容/对象、形式/视觉、文化/语义、关联/情境四个维度，输入图像路径，返回标注结果"
        )
    )
    
    # 9. 多维标注工具 - 根据标注生成组合建议
    def generate_combination_from_annotation(annotation_result: str, theme: str = None) -> str:
        """
        根据多维标注结果生成剪纸组合设计建议
        
        Args:
            annotation_result: JSON格式的多维标注结果
            theme: 可选的设计主题
            
        Returns:
            JSON格式的组合设计建议，包括纹样组合、布局建议、颜色建议等
        """
        try:
            # 解析JSON字符串为字典
            annotation_dict = json.loads(annotation_result)
            result = multidimensional_annotation_tool.generate_combination_suggestions(annotation_dict, theme)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except json.JSONDecodeError as e:
            return f"标注结果格式错误: {str(e)}"
        except Exception as e:
            return f"生成组合建议失败: {str(e)}"
    
    tools.append(
        Tool(
            name="generate_combination_from_annotation",
            func=generate_combination_from_annotation,
            description="根据多维标注结果生成剪纸组合设计建议，输入JSON格式的标注结果和可选的设计主题，返回组合设计建议"
        )
    )
    
    return tools

# 导出工具列表
tools = create_tools()
