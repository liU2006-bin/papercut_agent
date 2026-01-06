import json
import os

class KnowledgeTool:
    def __init__(self, database_path='json_database.py'):
        """
        初始化知识查询工具
        :param database_path: 知识库文件路径
        """
        self.database_path = database_path
        self.knowledge_base = None
        self._load_database()
    
    def _load_database(self):
        """
        加载知识库数据
        """
        try:
            if not os.path.exists(self.database_path):
                raise FileNotFoundError(f"知识库文件不存在: {self.database_path}")
            
            # 读取文件内容
            with open(self.database_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取JSON数据
            # 找到data = { ... }部分
            data_start = content.find('data = {')
            if data_start == -1:
                raise ValueError("无法找到知识库数据")
            
            data_start += len('data = ')
            
            # 解析JSON数据
            # 这里我们需要将Python字典转换为JSON字符串格式
            import ast
            self.knowledge_base = ast.literal_eval(content[data_start:])
            
            print(f"成功加载知识库: {self.database_path}")
        except Exception as e:
            print(f"加载知识库失败: {str(e)}")
            raise
    
    def get_pattern_by_id(self, pattern_id):
        """
        根据纹样ID查询纹样信息
        :param pattern_id: 纹样ID
        :return: 纹样信息字典，如果未找到返回None
        """
        if not self.knowledge_base:
            raise ValueError("知识库未加载")
        
        for pattern in self.knowledge_base['knowledge_base']['patterns']:
            if pattern['id'] == pattern_id:
                return pattern
        return None
    
    def get_pattern_by_name(self, pattern_name):
        """
        根据纹样名称查询纹样信息
        :param pattern_name: 纹样名称
        :return: 纹样信息列表，如果未找到返回空列表
        """
        if not self.knowledge_base:
            raise ValueError("知识库未加载")
        
        results = []
        for pattern in self.knowledge_base['knowledge_base']['patterns']:
            if pattern['name'] == pattern_name:
                results.append(pattern)
            # 检查别名
            if 'aliases' in pattern:
                if pattern_name in pattern['aliases']:
                    results.append(pattern)
        return results
    
    def get_patterns_by_region(self, region_id):
        """
        根据区域ID查询该区域的纹样
        :param region_id: 区域ID
        :return: 纹样信息列表，如果未找到返回空列表
        """
        if not self.knowledge_base:
            raise ValueError("知识库未加载")
        
        results = []
        for pattern in self.knowledge_base['knowledge_base']['patterns']:
            if pattern['region_id'] == region_id:
                results.append(pattern)
        return results
    
    def get_region_info(self, region_id):
        """
        查询区域信息
        :param region_id: 区域ID
        :return: 区域信息字典，如果未找到返回None
        """
        if not self.knowledge_base:
            raise ValueError("知识库未加载")
        
        for region in self.knowledge_base['knowledge_base']['regions']:
            if region['id'] == region_id:
                return region
        return None
    
    def get_related_patterns(self, pattern_id):
        """
        查询相关纹样
        :param pattern_id: 纹样ID
        :return: 相关纹样信息列表，如果未找到返回空列表
        """
        if not self.knowledge_base:
            raise ValueError("知识库未加载")
        
        # 先找到当前纹样
        current_pattern = self.get_pattern_by_id(pattern_id)
        if not current_pattern:
            return []
        
        # 查询相关纹样
        related_patterns = []
        if 'related_patterns' in current_pattern:
            for related_id in current_pattern['related_patterns']:
                related_pattern = self.get_pattern_by_id(related_id)
                if related_pattern:
                    related_patterns.append(related_pattern)
        
        return related_patterns
    
    def search_patterns(self, keyword):
        """
        根据关键词搜索纹样
        :param keyword: 搜索关键词
        :return: 匹配的纹样信息列表
        """
        if not self.knowledge_base:
            raise ValueError("知识库未加载")
        
        results = []
        for pattern in self.knowledge_base['knowledge_base']['patterns']:
            # 检查名称、别名、描述等字段
            if (keyword in pattern['name'] or 
                ('aliases' in pattern and any(keyword in alias for alias in pattern['aliases'])) or 
                ('appearance_description' in pattern and keyword in pattern['appearance_description']) or 
                ('symbolism' in pattern and any(keyword in item for item in pattern['symbolism']))):
                results.append(pattern)
        
        return results
    
    def get_all_patterns(self):
        """
        获取所有纹样信息
        :return: 所有纹样信息列表
        """
        if not self.knowledge_base:
            raise ValueError("知识库未加载")
        
        return self.knowledge_base['knowledge_base']['patterns']
    
    def get_all_regions(self):
        """
        获取所有区域信息
        :return: 所有区域信息列表
        """
        if not self.knowledge_base:
            raise ValueError("知识库未加载")
        
        return self.knowledge_base['knowledge_base']['regions']

# 示例用法
if __name__ == "__main__":
    tool = KnowledgeTool()
    
    # 示例1：根据ID查询纹样
    # pattern = tool.get_pattern_by_id('pattern_001')
    # print(f"纹样ID: pattern_001, 名称: {pattern['name']}, 象征意义: {pattern['symbolism']}")
    
    # 示例2：根据名称查询纹样
    # patterns = tool.get_pattern_by_name('鱼纹')
    # for pattern in patterns:
    #     print(f"纹样名称: {pattern['name']}, ID: {pattern['id']}")
    
    # 示例3：搜索纹样
    # patterns = tool.search_patterns('吉祥')
    # print(f"找到 {len(patterns)} 个包含'吉祥'的纹样")
