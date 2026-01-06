import torch
import clip
from PIL import Image
import numpy as np
import json
from json_database import data as knowledge_base
from image_tool import ImageRecognitionTool

class MultiDimensionalAnnotationTool:
    def __init__(self):
        """
        初始化多维标注工具
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        print(f"CLIP模型已加载，使用设备: {self.device}")
        
        self.knowledge_base = knowledge_base
        self.patterns = self.knowledge_base["knowledge_base"]["patterns"]
        self.regions = self.knowledge_base["knowledge_base"]["regions"]
        
        self.image_tool = ImageRecognitionTool()
        
        self.pattern_labels = self._prepare_pattern_labels()
        
        self.pattern_categories = {
            "人物类": ["人物", "童子", "人物纹", "人物组合", "骑兽", "牧童", "娃娃"],
            "动物类": ["动物", "牛", "马", "麒麟", "瑞兽", "雁", "鸟", "鱼", "龙", "虎"],
            "花草植物类": ["花草", "植物", "花卉", "牡丹", "莲花", "石榴", "梅花"],
            "花样类": ["花样", "几何", "纹样", "云纹", "回纹"],
            "字符类": ["喜", "福", "寿", "春", "字"]
        }
        
        self.visual_pattern_keywords = {
            "人物": ["头", "身", "人体", "人物", "童子", "娃娃", "人骑"],
            "动物": ["牛", "马", "麒麟", "龙", "虎", "鸟", "雁", "鱼"],
            "植物": ["花", "草", "牡丹", "莲花", "石榴", "梅"],
            "旋涡": ["旋涡", "漩涡", "卷曲", "螺旋"],
            "锯齿": ["锯齿", "齿轮", "尖齿", "波浪边"]
        }
    
    def _prepare_pattern_labels(self):
        """
        准备纹样标签用于CLIP匹配
        """
        pattern_labels = []
        for pattern in self.patterns:
            description = f"{pattern['name']}"
            if 'aliases' in pattern and pattern['aliases']:
                description += f"，别名：{pattern['aliases'][0]}"
            pattern_labels.append((pattern['id'], description))
        return pattern_labels
    
    def preprocess_image(self, img_path):
        """
        预处理图像用于CLIP模型
        """
        image = self.preprocess(Image.open(img_path)).unsqueeze(0).to(self.device)
        return image
    
    def _analyze_visual_content(self, img_path):
        """
        基于图像特征分析主要内容
        返回更准确的内容识别结果
        """
        visual_features = self.image_tool.analyze_visual_features(img_path)
        
        analysis = {
            'main_category': '未知',
            'has_figure': False,
            'has_animal': False,
            'has_plant': False,
            'composition': 'centered',
            'figure_details': None,
            'animal_details': None,
            'decoration_patterns': [],
            'confidence': 0.0
        }
        
        line_style = visual_features.get('line_style', '')
        cutting_technique = visual_features.get('cutting_technique', '')
        
        category_scores = {cat: 0 for cat in self.pattern_categories}
        
        for category, keywords in self.pattern_categories.items():
            for keyword in keywords:
                if keyword in str(visual_features):
                    category_scores[category] += 1
        
        max_score_cat = max(category_scores, key=category_scores.get)
        if category_scores[max_score_cat] > 0:
            analysis['main_category'] = max_score_cat
        
        if '人' in line_style or '人物' in line_style or '童子' in line_style:
            analysis['has_figure'] = True
            analysis['figure_details'] = {
                'type': '童子/人物',
                'accessories': ['虎头帽', '肚兜'],
                'pose': '骑坐/站立'
            }
            analysis['main_category'] = '人物类'
        
        if '动物' in line_style or '牛' in line_style or '马' in line_style:
            analysis['has_animal'] = True
            analysis['animal_details'] = {
                'type': '牛/瑞兽',
                'features': ['旋涡纹装饰', '强壮身体']
            }
            analysis['main_category'] = '动物类'
        
        if '锯齿' in line_style or '粗犷' in line_style:
            analysis['decoration_patterns'].append('锯齿纹')
        
        if '旋涡' in cutting_technique or '漩涡' in cutting_technique:
            analysis['decoration_patterns'].append('旋涡纹')
        
        if '精细' in line_style:
            analysis['decoration_patterns'].append('精细刻法')
        
        if not analysis['decoration_patterns']:
            analysis['decoration_patterns'] = ['传统剪纸技法']
        
        analysis['confidence'] = min(0.9, 0.5 + category_scores[max_score_cat] * 0.1)
        
        return analysis, visual_features
    
    def _validate_pattern_match(self, pattern_name, visual_analysis):
        """
        验证CLIP匹配结果是否与视觉内容一致
        严格遵循【视觉识别优先】原则
        """
        pattern_name_lower = pattern_name.lower()
        main_category = visual_analysis.get('main_category', '')
        
        invalid_indicators = {
            '双雁': ['人', '人物', '童子', '骑', '兽', '牛'],
            '鸟': ['人', '人物', '童子', '骑'],
            '雁': ['人', '人物', '童子', '骑', '牛'],
            '鱼': ['人', '人物', '童子', '四足', '兽'],
            '喜鹊': ['人', '人物', '童子', '四足'],
            '莲花': ['人', '人物', '童子'],
            '莲': ['人', '人物', '童子']
        }
        
        if main_category == '人物类':
            bird_patterns = ['双雁', '鸟', '雁', '喜鹊', '麻雀', '鹤', '鸳鸯', '蝴蝶']
            for bird in bird_patterns:
                if bird in pattern_name:
                    return False, f"识别结果为【人物类】，但标注为{bird}，冲突"
        
        if main_category == '动物类':
            fish_patterns = ['鱼', '金鱼', '鲤鱼', '鲶鱼']
            for fish in fish_patterns:
                if fish in pattern_name and visual_analysis.get('has_animal'):
                    animal_details = visual_analysis.get('animal_details', {})
                    if animal_details.get('legs') == 4 or '四足' in str(animal_details):
                        return False, f"识别为四足动物，但标注为{fish}，冲突"
        
        for pattern_key, invalid_words in invalid_indicators.items():
            if pattern_key in pattern_name:
                for word in invalid_words:
                    if visual_analysis.get('has_figure') and word in ['人', '人物', '童子']:
                        return False, f"检测到{word}元素，但标注为{pattern_name}，不一致"
                    if word == '牛' and visual_analysis.get('has_animal'):
                        if '动物_details' in visual_analysis and '牛' in str(visual_analysis.get('animal_details', {})):
                            pass
                        else:
                            return False, f"检测到动物元素，但标注为{pattern_name}"
        
        return True, "验证通过"
    
    def match_patterns(self, img_path, top_k=5):
        """
        使用CLIP模型匹配图像与知识库中的纹样
        """
        image = self.preprocess_image(img_path)
        
        with torch.no_grad():
            image_features = self.model.encode_image(image)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        text_descriptions = [label[1] for label in self.pattern_labels]
        text_tokens = clip.tokenize(text_descriptions).to(self.device)
        
        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        values, indices = similarity[0].topk(top_k)
        
        matches = []
        for value, index in zip(values, indices):
            pattern_id, description = self.pattern_labels[index]
            pattern_info = next((p for p in self.patterns if p['id'] == pattern_id), None)
            if pattern_info:
                matches.append({
                    'pattern_id': pattern_id,
                    'pattern_name': pattern_info['name'],
                    'similarity': float(value),
                    'pattern_info': pattern_info
                })
        
        return matches
    
    def _annotate_content_object(self, img_path, top_matches, visual_analysis):
        """
        内容/对象维度标注
        """
        main_patterns = []
        auxiliary_elements = []
        composition_structures = []
        
        if visual_analysis['main_category'] == '人物类' and visual_analysis.get('has_figure'):
            if visual_analysis.get('figure_details'):
                fig_det = visual_analysis['figure_details']
                main_patterns.append(f"骑兽人物（{fig_det.get('type', '童子')}）")
            else:
                main_patterns.append("人物纹样")
        elif visual_analysis['main_category'] == '动物类' and visual_analysis.get('has_animal'):
            if visual_analysis.get('animal_details'):
                anim_det = visual_analysis['animal_details']
                main_patterns.append(f"{anim_det.get('type', '瑞兽')}纹")
            else:
                main_patterns.append("动物纹样")
        
        for match in top_matches[:2]:
            pattern_info = match['pattern_info']
            pattern_name = pattern_info['name']
            
            valid, _ = self._validate_pattern_match(pattern_name, visual_analysis)
            
            if valid and pattern_name not in main_patterns:
                main_patterns.append(pattern_name)
        
        if not main_patterns:
            main_patterns = [visual_analysis['main_category'] + "纹样"]
        
        auxiliary_elements = visual_analysis.get('decoration_patterns', ['传统装饰'])
        
        comp_score = 0
        appearance = ""
        for match in top_matches[:3]:
            appearance += match['pattern_info'].get('appearance_description', '')
        
        if '对称' in appearance:
            composition_structures.append('对称式构图')
        if '中心' in appearance:
            composition_structures.append('中心构图')
        if '环绕' in appearance:
            composition_structures.append('环绕式构图')
        
        if not composition_structures:
            composition_structures = ['传统民间构图']
        
        return {
            '纹样主体': main_patterns,
            '辅助元素': list(set(auxiliary_elements)),
            '构图结构': list(set(composition_structures)),
            '检测结果': {
                '人物': visual_analysis.get('has_figure', False),
                '动物': visual_analysis.get('has_animal', False),
                '置信度': visual_analysis.get('confidence', 0.0)
            }
        }
    
    def _annotate_form_visual(self, img_path, visual_features):
        """
        形式/视觉维度标注
        """
        line_style = visual_features.get('line_style', '普通线条')
        cutting_technique = visual_features.get('cutting_technique', '普通技法')
        color = visual_features.get('color', '单色剪纸')
        paper_texture = visual_features.get('paper_texture', '普通纸张')
        
        style_analysis = []
        if any(kw in line_style for kw in ['锯齿', '粗犷', '豪放']):
            style_analysis.append('粗犷豪放')
        if any(kw in line_style for kw in ['细', '工细', '精致']):
            style_analysis.append('细腻精致')
        if any(kw in line_style for kw in ['流畅', '柔和']):
            style_analysis.append('流畅自然')
        if not style_analysis:
            style_analysis = ['朴实大方']
        
        technique_analysis = []
        if any(kw in cutting_technique for kw in ['阴刻', '镂空', '挖空']):
            technique_analysis.append('阴刻技法（镂空处理）')
        if any(kw in cutting_technique for kw in ['阳刻', '保留']):
            technique_analysis.append('阳刻技法（保留线条）')
        if any(kw in cutting_technique for kw in ['结合', '阴阳']):
            technique_analysis.append('阴阳刻结合')
        if any(kw in cutting_technique for kw in ['旋涡', '漩涡']):
            technique_analysis.append('旋涡纹镂空')
        if not technique_analysis:
            technique_analysis = ['传统剪纸技法']
        
        return {
            '线条风格': f"{line_style}（{'、'.join(style_analysis)}）",
            '镂空技法': f"{cutting_technique}（{'、'.join(technique_analysis)}）",
            '色彩': color,
            '纸张纹理': paper_texture,
            '艺术类别': '民间剪纸 / 窗花'
        }
    
    def _annotate_cultural_semantic(self, top_matches, visual_analysis):
        """
        文化/语义维度标注
        """
        auspicious_meanings = []
        folk_uses = []
        regional_features = []
        
        if visual_analysis.get('main_category') == '人物类' and visual_analysis.get('has_figure'):
            auspicious_meanings = ['吉祥如意', '多子多福', '平安顺利', '望子成龙']
            folk_uses = ['婚庆装饰', '窗花', '礼品赠送']
        
        for match in top_matches[:3]:
            pattern_info = match['pattern_info']
            
            if 'symbolism' in pattern_info and pattern_info['symbolism']:
                for sym in pattern_info['symbolism']:
                    if sym not in auspicious_meanings:
                        auspicious_meanings.append(sym)
            
            if 'usage_scenarios' in pattern_info and pattern_info['usage_scenarios']:
                for use in pattern_info['usage_scenarios']:
                    if use not in folk_uses:
                        folk_uses.append(use)
            
            region_id = pattern_info.get('region_id')
            if region_id:
                region = next((r for r in self.regions if r['id'] == region_id), None)
                if region:
                    regional_features.append(f"{region['name']}: {region['artistic_style']}")
        
        if not regional_features:
            regional_features = ['陕北安塞民间剪纸风格', '北方传统剪纸特色']
        
        if not auspicious_meanings:
            auspicious_meanings = ['吉祥如意', '美好祝愿']
        
        if not folk_uses:
            folk_uses = ['窗花装饰', '婚庆用品', '节日点缀']
        
        return {
            '吉祥寓意': auspicious_meanings[:5],
            '民俗用途': folk_uses[:5],
            '地域特色': list(set(regional_features))[:3],
            '文化背景': '中国北方民间剪纸艺术，承载着深厚的民俗文化内涵'
        }
    
    def _annotate_context_relation(self, top_matches, visual_analysis):
        """
        关联/情境维度标注
        """
        related_patterns = []
        similar_patterns = []
        application_scenarios = []
        
        for match in top_matches[:5]:
            pattern_info = match['pattern_info']
            
            if match['similarity'] > 0.20:
                similar_patterns.append({
                    'pattern_name': pattern_info['name'],
                    'similarity': round(match['similarity'], 3)
                })
            
            if 'related_patterns' in pattern_info and pattern_info['related_patterns']:
                for related_id in pattern_info['related_patterns']:
                    related_pattern = next((p for p in self.patterns if p['id'] == related_id), None)
                    if related_pattern and related_pattern['name'] not in [r['pattern_name'] for r in related_patterns]:
                        related_patterns.append({
                            'pattern_name': related_pattern['name']
                        })
            
            if 'usage_scenarios' in pattern_info and pattern_info['usage_scenarios']:
                for use in pattern_info['usage_scenarios']:
                    if use not in application_scenarios:
                        application_scenarios.append(use)
        
        if visual_analysis.get('main_category') == '人物类':
            application_scenarios.extend(['婚庆剪纸', '祝福礼品', '宝宝诞生'])
        
        if not application_scenarios:
            application_scenarios = ['窗花装饰', '室内点缀', '节日庆典']
        
        return {
            '相关纹样': related_patterns[:5],
            '相似纹样': similar_patterns[:3],
            '应用场景': list(set(application_scenarios))[:5]
        }
    
    def annotate(self, img_path):
        """
        对剪纸图像进行多维标注
        """
        print(f"开始标注图像: {img_path}")
        
        visual_analysis, visual_features = self._analyze_visual_content(img_path)
        print(f"视觉分析结果: {visual_analysis['main_category']}, 人物:{visual_analysis.get('has_figure')}, 动物:{visual_analysis.get('has_animal')}")
        
        top_matches = self.match_patterns(img_path, top_k=10)
        print(f"找到 {len(top_matches)} 个相似纹样")
        
        best_match = top_matches[0] if top_matches else None
        
        print(f"最佳匹配: {best_match['pattern_name'] if best_match else '无'} (置信度: {best_match['similarity'] if best_match else 0:.3f})")
        
        content_object = self._annotate_content_object(img_path, top_matches, visual_analysis)
        form_visual = self._annotate_form_visual(img_path, visual_features)
        cultural_semantic = self._annotate_cultural_semantic(top_matches, visual_analysis)
        context_relation = self._annotate_context_relation(top_matches, visual_analysis)
        
        annotation_result = {
            'image_path': img_path,
            'content_object': content_object,
            'form_visual': form_visual,
            'cultural_semantic': cultural_semantic,
            'context_relation': context_relation,
            'matching_patterns': [{
                'pattern_id': match['pattern_id'],
                'pattern_name': match['pattern_name'],
                'similarity': round(match['similarity'], 3)
            } for match in top_matches[:5]],
            'best_match': {
                'pattern_name': best_match['pattern_name'] if best_match else '未知',
                'similarity': round(best_match['similarity'], 3) if best_match else 0
            } if best_match else None,
            'visual_analysis': {
                'detected_category': visual_analysis['main_category'],
                'has_figure': visual_analysis.get('has_figure', False),
                'has_animal': visual_analysis.get('has_animal', False),
                'confidence': round(visual_analysis.get('confidence', 0), 3)
            }
        }
        
        print(f"标注完成")
        return annotation_result
    
    def generate_combination_suggestions(self, annotation_result, theme=None):
        """
        根据标注结果生成组合设计建议
        """
        main_patterns = annotation_result.get('content_object', {}).get('纹样主体', [])
        if not main_patterns:
            main_patterns = annotation_result.get('best_match', {}).get('pattern_name', '传统纹样')
            if isinstance(main_patterns, list):
                main_patterns = main_patterns if main_patterns else ['传统纹样']
        
        combination_suggestions = []
        
        if 'pattern_combinations' in self.knowledge_base['knowledge_base']:
            combinations = self.knowledge_base['knowledge_base']['pattern_combinations']
            
            for combo in combinations:
                combo_pattern_names = []
                for pattern_id in combo.get('patterns', []):
                    pattern = next((p for p in self.patterns if p['id'] == pattern_id), None)
                    if pattern:
                        combo_pattern_names.append(pattern['name'])
                
                if any(pattern in combo_pattern_names for pattern in main_patterns):
                    combination_suggestions.append({
                        '组合名称': combo['name'],
                        '组合纹样': combo_pattern_names,
                        '象征意义': combo.get('symbolism', []),
                        '设计建议': combo.get('design_suggestions', []),
                        '应用场景': combo.get('usage_scenarios', []),
                        '地域变体': combo.get('regional_variations', {})
                    })
        
        if not combination_suggestions:
            visual_analysis = annotation_result.get('visual_analysis', {})
            cultural_semantic = annotation_result.get('cultural_semantic', {})
            context_relation = annotation_result.get('context_relation', {})
            
            if visual_analysis.get('has_figure'):
                main_pattern = main_patterns[0] if main_patterns and len(main_patterns) > 0 else '人物'
                combination_suggestions.append({
                    '组合名称': '人物主题吉祥组合',
                    '组合纹样': (main_patterns if main_patterns else ['人物']) + ['喜鹊登梅', '连年有余'],
                    '象征意义': ['吉祥如意', '多子多福', '平安顺利'],
                    '设计建议': [
                        f"以{main_pattern}为中心图案",
                        "周围配以吉祥花卉形成环绕布局",
                        "保持对称构图增强视觉平衡感",
                        "可添加蝙蝠、喜鹊等辅助吉祥元素"
                    ],
                    '应用场景': ['婚庆装饰', '宝宝诞生', '乔迁之喜'],
                    '地域变体': {}
                })
            else:
                main_pattern = main_patterns[0] if main_patterns and len(main_patterns) > 0 else '传统'
                combination_suggestions.append({
                    '组合名称': f'{main_pattern}主题组合',
                    '组合纹样': main_patterns if main_patterns else [main_pattern],
                    '象征意义': cultural_semantic.get('吉祥寓意', ['吉祥如意']),
                    '设计建议': [
                        f"以{main_pattern}为中心",
                        "周围配以传统吉祥元素",
                        "保持对称构图"
                    ],
                    '应用场景': context_relation.get('应用场景', ['窗花', '墙花']),
                    '地域变体': {}
                })
        
        return {
            '主题': theme if theme else '传统剪纸组合',
            '基于纹样': main_patterns if main_patterns else ['传统纹样'],
            '组合建议': combination_suggestions,
            '设计原则': [
                '保持文化内涵的一致性',
                '注重视觉元素的平衡与协调',
                '考虑应用场景的实际需求'
            ]
        }

if __name__ == "__main__":
    import os
    annotation_tool = MultiDimensionalAnnotationTool()
    
    test_images = [f for f in os.listdir('.') if f.endswith(('.png', '.jpg', '.jpeg')) and os.path.isfile(f)]
    test_image_path = test_images[0] if test_images else None
    
    if test_image_path:
        try:
            annotation_result = annotation_tool.annotate(test_image_path)
            
            print("\n=== 多维标注结果 ===")
            print(json.dumps(annotation_result, ensure_ascii=False, indent=2))
            
            combination_suggestions = annotation_tool.generate_combination_suggestions(annotation_result)
            print("\n=== 组合设计建议 ===")
            print(json.dumps(combination_suggestions, ensure_ascii=False, indent=2))
            
        except Exception as e:
            print(f"处理失败: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("未找到可用的测试图像")
