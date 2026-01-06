import torch
import clip
from PIL import Image
import numpy as np
import json
from json_database import data

class CLIPAnnotationTool:
    def __init__(self):
        """
        初始化CLIP多模态图像标注工具
        """
        # 加载CLIP模型
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        
        # 加载知识库
        self.knowledge_base = data["knowledge_base"]
        self.patterns = self.knowledge_base["patterns"]
        
        # 生成知识库中的标签
        self.pattern_labels = []
        self.pattern_embeddings = []
        
        # 预处理纹样标签
        self._preprocess_pattern_labels()
    
    def _preprocess_pattern_labels(self):
        """
        预处理知识库中的纹样标签，生成CLIP嵌入
        """
        for pattern in self.patterns:
            # 构建纹样的文本描述
            pattern_desc = f"{pattern['name']} 剪纸纹样，{pattern['appearance_description']}，象征{', '.join(pattern['symbolism'])}，用于{', '.join(pattern['usage_scenarios'])}场景"
            self.pattern_labels.append(pattern_desc)
        
        # 生成CLIP文本嵌入
        with torch.no_grad():
            text = clip.tokenize(self.pattern_labels).to(self.device)
            self.pattern_embeddings = self.model.encode_text(text)
            self.pattern_embeddings /= self.pattern_embeddings.norm(dim=-1, keepdim=True)
    
    def get_multidimensional_annotation(self, image_path):
        """
        使用CLIP进行多维度图像标注
        
        :param image_path: 图像路径
        :return: 多维标注结果
        """
        # 加载并预处理图像
        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            # 生成图像嵌入
            image_features = self.model.encode_image(image)
            image_features /= image_features.norm(dim=-1, keepdim=True)
            
            # 计算图像与所有纹样标签的相似度
            similarity = (100.0 * image_features @ self.pattern_embeddings.T).softmax(dim=-1)
            values, indices = similarity[0].topk(3)  # 获取前3个最相似的纹样
        
        # 解析标注结果
        top_patterns = []
        for i in range(3):
            idx = indices[i].item()
            confidence = values[i].item()
            if confidence > 0.1:  # 设置阈值
                pattern_info = self.patterns[idx].copy()
                pattern_info['confidence'] = float(confidence)
                top_patterns.append(pattern_info)
        
        # 基于前3个最相似的纹样生成多维标注
        annotation = {
            "content_object": self._annotate_content_object(top_patterns),
            "form_visual": self._annotate_form_visual(image_path),
            "cultural_semantic": self._annotate_cultural_semantic(top_patterns),
            "context_relation": self._annotate_context_relation(top_patterns),
            "recognized_patterns": top_patterns
        }
        
        return annotation
    
    def _annotate_content_object(self, top_patterns):
        """
        内容/对象维度标注
        """
        main_subjects = []
        auxiliary_elements = []
        composition_structure = []
        
        for pattern in top_patterns:
            # 提取纹样主体
            main_subjects.append(pattern['name'])
            
            # 从外观描述中提取辅助元素
            appearance = pattern['appearance_description']
            if '周围装饰' in appearance:
                elements = appearance.split('周围装饰')[1].split('等')[0].strip()
                auxiliary_elements.extend([e.strip() for e in elements.split('、')])
            
            # 分析构图结构
            if '对称' in appearance:
                composition_structure.append('对称布局')
            if '交尾' in appearance:
                composition_structure.append('交合构图')
            if '团花' in appearance:
                composition_structure.append('团花结构')
        
        return {
            "main_subjects": list(set(main_subjects)),
            "auxiliary_elements": list(set(auxiliary_elements)),
            "composition_structure": list(set(composition_structure))
        }
    
    def _annotate_form_visual(self, image_path):
        """
        形式/视觉维度标注
        """
        # 使用CLIP生成视觉特征描述
        import cv2
        from image_tool import ImageRecognitionTool
        
        # 复用现有的视觉分析功能
        image_tool = ImageRecognitionTool()
        visual_features = image_tool.analyze_visual_features(image_path)
        
        return {
            "line_style": visual_features['line_style'],
            "cutting_technique": visual_features['cutting_technique'],
            "color": visual_features['color'],
            "paper_texture": visual_features['paper_texture']
        }
    
    def _annotate_cultural_semantic(self, top_patterns):
        """
        文化/语义维度标注
        """
        symbolism = []
        cultural_background = []
        usage_scenarios = []
        regional_features = []
        
        for pattern in top_patterns:
            symbolism.extend(pattern['symbolism'])
            cultural_background.append(pattern['cultural_background'])
            usage_scenarios.extend(pattern['usage_scenarios'])
            
            # 获取地域特征
            if 'region_id' in pattern:
                region_id = pattern['region_id']
                for region in self.knowledge_base['regions']:
                    if region['id'] == region_id:
                        regional_features.append(region['name'])
                        break
            elif 'regions' in pattern:
                for region_id in pattern['regions']:
                    for region in self.knowledge_base['regions']:
                        if region['id'] == region_id:
                            regional_features.append(region['name'])
                            break
        
        return {
            "symbolism": list(set(symbolism)),
            "cultural_background": list(set(cultural_background)),
            "usage_scenarios": list(set(usage_scenarios)),
            "regional_features": list(set(regional_features))
        }
    
    def _annotate_context_relation(self, top_patterns):
        """
        关联/情境维度标注
        """
        related_patterns = []
        similar_patterns = []
        application_cases = []
        
        for pattern in top_patterns:
            # 获取相关纹样
            if 'related_patterns' in pattern and pattern['related_patterns']:
                for related_id in pattern['related_patterns']:
                    for p in self.patterns:
                        if p['id'] == related_id:
                            related_patterns.append(p['name'])
                            break
            
            # 添加相似纹样
            for p in self.patterns:
                if p['id'] != pattern['id'] and set(p['symbolism']) & set(pattern['symbolism']):
                    similar_patterns.append(p['name'])
            
            # 应用场景作为应用案例
            application_cases.extend(pattern['usage_scenarios'])
        
        return {
            "related_patterns": list(set(related_patterns)),
            "similar_patterns": list(set(similar_patterns)),
            "application_cases": list(set(application_cases))
        }
    
    def generate_combination_suggestions(self, annotation_result, theme=None):
        """
        根据标注结果生成组合设计建议
        
        :param annotation_result: 标注结果
        :param theme: 设计主题（可选）
        :return: 组合设计建议
        """
        # 获取识别到的纹样
        recognized_patterns = annotation_result.get('recognized_patterns', [])
        
        if not recognized_patterns:
            return {
                "error": "未识别到有效纹样"
            }
        
        # 基于识别到的纹样查找组合建议
        combination_suggestions = {
            "theme": theme or "传统文化组合",
            "patterns": [],
            "design_suggestions": [],
            "usage_scenarios": [],
            "regional_features": []
        }
        
        # 收集纹样信息
        for pattern in recognized_patterns:
            combination_suggestions["patterns"].append(pattern['name'])
            
            # 查找知识库中的组合信息
            for combo in self.knowledge_base.get("pattern_combinations", []):
                if pattern['id'] in combo['patterns']:
                    combination_suggestions["design_suggestions"].extend(combo['design_suggestions'])
                    combination_suggestions["usage_scenarios"].extend(combo['usage_scenarios'])
                    if 'regional_variations' in combo:
                        combination_suggestions["regional_features"].extend(combo['regional_variations'].keys())
        
        # 去重
        for key in combination_suggestions:
            if isinstance(combination_suggestions[key], list):
                combination_suggestions[key] = list(set(combination_suggestions[key]))
        
        return combination_suggestions

# 测试代码
if __name__ == "__main__":
    tool = CLIPAnnotationTool()
    # 测试图像路径需要根据实际情况修改
    # result = tool.get_multidimensional_annotation("test_image.jpg")
    # print(json.dumps(result, ensure_ascii=False, indent=2))
