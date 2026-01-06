from knowledge_tool import KnowledgeTool
import random

class DesignTool:
    def __init__(self):
        """
        初始化设计工具
        """
        self.knowledge_tool = KnowledgeTool()
    
    def get_wedding_combination(self):
        """
        婚礼主题组合设计方案
        :return: 设计方案字典
        """
        # 选择与婚礼相关的纹样
        wedding_patterns = []
        
        # 获取相关纹样
        double_goose = self.knowledge_tool.get_pattern_by_id('pattern_001')  # 双雁喜花
        fish = self.knowledge_tool.get_pattern_by_id('pattern_003')  # 鱼纹
        snake_rabbit = self.knowledge_tool.get_pattern_by_id('pattern_004')  # 蛇盘兔
        calabash = self.knowledge_tool.get_pattern_by_id('pattern_005')  # 葫芦纹
        
        if double_goose:
            wedding_patterns.append(double_goose)
        if fish:
            wedding_patterns.append(fish)
        if snake_rabbit:
            wedding_patterns.append(snake_rabbit)
        if calabash:
            wedding_patterns.append(calabash)
        
        # 如果没有找到足够的纹样，随机选择一些其他吉祥纹样
        if len(wedding_patterns) < 3:
            all_patterns = self.knowledge_tool.get_all_patterns()
            lucky_patterns = [p for p in all_patterns if any('吉祥' in sym or '福' in sym or '喜' in sym for sym in p.get('symbolism', []))]
            
            while len(wedding_patterns) < 3 and lucky_patterns:
                pattern = random.choice(lucky_patterns)
                if pattern not in wedding_patterns:
                    wedding_patterns.append(pattern)
                lucky_patterns.remove(pattern)
        
        return {
            'theme': '婚礼',
            'description': '适合婚礼场景的剪纸组合设计，象征夫妻恩爱、婚姻美满、多子多福',
            'patterns': [
                {
                    'id': p['id'],
                    'name': p['name'],
                    'symbolism': p['symbolism'],
                    'usage': p['usage_scenarios'][0] if p.get('usage_scenarios') else '婚礼装饰'
                } for p in wedding_patterns
            ],
            'layout_suggestion': '以双雁喜花为中心，周围环绕鱼纹、蛇盘兔和葫芦纹，形成对称的圆形或方形布局',
            'color_suggestion': '以红色为主，象征喜庆；可搭配少量金色或粉色，增添婚礼的温馨氛围'
        }
    
    def get_festival_combination(self, festival='春节'):
        """
        节日主题组合设计方案
        :param festival: 节日名称（默认春节）
        :return: 设计方案字典
        """
        # 根据不同节日选择合适的纹样
        festival_patterns = []
        
        if festival == '春节':
            # 春节相关纹样
            tiger = self.knowledge_tool.get_pattern_by_id('pattern_007')  # 虎纹
            lion = self.knowledge_tool.get_pattern_by_id('pattern_008')  # 狮纹
            calabash = self.knowledge_tool.get_pattern_by_id('pattern_005')  # 葫芦纹
            
            if tiger:
                festival_patterns.append(tiger)
            if lion:
                festival_patterns.append(lion)
            if calabash:
                festival_patterns.append(calabash)
            
            # 添加其他春节相关纹样
            all_patterns = self.knowledge_tool.get_all_patterns()
            spring_patterns = [p for p in all_patterns if any('辟邪' in sym or '纳福' in sym or '平安' in sym for sym in p.get('symbolism', []))]
            
            while len(festival_patterns) < 3 and spring_patterns:
                pattern = random.choice(spring_patterns)
                if pattern not in festival_patterns:
                    festival_patterns.append(pattern)
                spring_patterns.remove(pattern)
                
            layout = '以虎纹和狮纹为门神装饰，中央放置葫芦纹，周围点缀其他吉祥纹样'
            colors = '以红色为主，象征喜庆；可搭配黄色和绿色，增添节日的活力'
        elif festival == '端午节':
            # 端午节相关纹样
            frog = self.knowledge_tool.get_pattern_by_id('pattern_002')  # 蛙纹
            calabash = self.knowledge_tool.get_pattern_by_id('pattern_005')  # 葫芦纹
            tiger = self.knowledge_tool.get_pattern_by_id('pattern_007')  # 虎纹
            
            if frog:
                festival_patterns.append(frog)
            if calabash:
                festival_patterns.append(calabash)
            if tiger:
                festival_patterns.append(tiger)
            
            layout = '以蛙纹和葫芦纹为主体，虎纹作为辅助，形成三角形布局'
            colors = '以红色和绿色为主，象征驱邪避毒；可搭配蓝色，增添清凉感'
        else:
            # 默认节日纹样
            festival_patterns = random.sample(self.knowledge_tool.get_all_patterns(), min(3, len(self.knowledge_tool.get_all_patterns())))
            layout = '根据所选纹样的大小和形状，形成平衡的布局'
            colors = '以红色为主，象征喜庆'
        
        return {
            'theme': f'{festival}装饰',
            'description': f'适合{festival}场景的剪纸组合设计，增添节日氛围',
            'patterns': [
                {
                    'id': p['id'],
                    'name': p['name'],
                    'symbolism': p['symbolism'],
                    'usage': p['usage_scenarios'][0] if p.get('usage_scenarios') else f'{festival}装饰'
                } for p in festival_patterns
            ],
            'layout_suggestion': layout,
            'color_suggestion': colors
        }
    
    def get_custom_combination(self, theme=None, symbolism=None, region=None):
        """
        自定义组合设计方案
        :param theme: 主题
        :param symbolism: 象征意义关键词
        :param region: 区域风格
        :return: 设计方案字典
        """
        custom_patterns = []
        all_patterns = self.knowledge_tool.get_all_patterns()
        
        # 根据条件筛选纹样
        filtered_patterns = all_patterns.copy()
        
        # 根据区域筛选
        if region:
            filtered_patterns = [p for p in filtered_patterns if p.get('region_id') == region]
        
        # 根据象征意义筛选
        if symbolism:
            filtered_patterns = [p for p in filtered_patterns if any(symbolism in sym for sym in p.get('symbolism', []))]
        
        # 如果没有足够的纹样，使用随机选择
        if len(filtered_patterns) < 2:
            filtered_patterns = all_patterns.copy()
        
        # 选择2-3个纹样
        custom_patterns = random.sample(filtered_patterns, min(3, len(filtered_patterns)))
        
        # 生成设计方案
        return {
            'theme': theme if theme else '自定义组合',
            'description': f'基于{theme if theme else "所选条件"}的剪纸组合设计',
            'patterns': [
                {
                    'id': p['id'],
                    'name': p['name'],
                    'symbolism': p['symbolism'],
                    'usage': p['usage_scenarios'][0] if p.get('usage_scenarios') else '装饰'
                } for p in custom_patterns
            ],
            'layout_suggestion': '根据纹样的大小、形状和象征意义，形成协调的布局。中心放置最具代表性的纹样，周围环绕辅助纹样',
            'color_suggestion': '根据主题选择合适的颜色，传统剪纸以红色为主，可根据需要搭配其他颜色'
        }
    
    def get_random_combination(self):
        """
        随机组合设计方案
        :return: 设计方案字典
        """
        all_patterns = self.knowledge_tool.get_all_patterns()
        random_patterns = random.sample(all_patterns, min(3, len(all_patterns)))
        
        return {
            'theme': '随机组合',
            'description': '随机选择的剪纸纹样组合，展现不同纹样的特色和美感',
            'patterns': [
                {
                    'id': p['id'],
                    'name': p['name'],
                    'symbolism': p['symbolism'],
                    'usage': p['usage_scenarios'][0] if p.get('usage_scenarios') else '装饰'
                } for p in random_patterns
            ],
            'layout_suggestion': '根据纹样的特点，尝试不同的布局方式，创造独特的视觉效果',
            'color_suggestion': '可以尝试传统的红色，也可以根据纹样的象征意义和个人喜好选择其他颜色'
        }

# 示例用法
if __name__ == "__main__":
    tool = DesignTool()
    
    # 示例1：婚礼主题组合
    print("=== 婚礼主题组合设计 ===")
    wedding_design = tool.get_wedding_combination()
    print(f"主题: {wedding_design['theme']}")
    print(f"描述: {wedding_design['description']}")
    print("纹样组合:")
    for p in wedding_design['patterns']:
        print(f"- {p['name']}: {', '.join(p['symbolism'])}")
    print(f"布局建议: {wedding_design['layout_suggestion']}")
    print(f"颜色建议: {wedding_design['color_suggestion']}")
    
    print("\n" + "="*50 + "\n")
    
    # 示例2：节日主题组合
    print("=== 春节主题组合设计 ===")
    festival_design = tool.get_festival_combination('春节')
    print(f"主题: {festival_design['theme']}")
    print(f"描述: {festival_design['description']}")
    print("纹样组合:")
    for p in festival_design['patterns']:
        print(f"- {p['name']}: {', '.join(p['symbolism'])}")
    print(f"布局建议: {festival_design['layout_suggestion']}")
    print(f"颜色建议: {festival_design['color_suggestion']}")
    
    print("\n" + "="*50 + "\n")
    
    # 示例3：随机组合
    print("=== 随机组合设计 ===")
    random_design = tool.get_random_combination()
    print(f"主题: {random_design['theme']}")
    print(f"描述: {random_design['description']}")
    print("纹样组合:")
    for p in random_design['patterns']:
        print(f"- {p['name']}: {', '.join(p['symbolism'])}")
    print(f"布局建议: {random_design['layout_suggestion']}")
    print(f"颜色建议: {random_design['color_suggestion']}")
