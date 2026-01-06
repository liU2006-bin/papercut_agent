import os
import json
import glob
from multidimensional_annotation_tool import MultiDimensionalAnnotationTool

# 数据集根目录
dataset_root = "."

# 类别列表
categories = ["人物类", "动物类", "抽象类", "花样类", "花草植物类"]

# 创建标注工具实例
annotation_tool = MultiDimensionalAnnotationTool()

# 存储所有标注结果
all_annotations = {
    "人物类": [],
    "动物类": [],
    "抽象类": [],
    "花样类": [],
    "花草植物类": []
}

# 处理每个类别
total_images = 0
processed_images = 0

for category in categories:
    category_path = os.path.join(dataset_root, category)
    
    # 检查类别目录是否存在
    if not os.path.exists(category_path):
        print(f"警告：类别目录 {category_path} 不存在，跳过")
        continue
    
    # 获取该类别下的所有图像文件
    image_files = glob.glob(os.path.join(category_path, "*.jpg")) + glob.glob(os.path.join(category_path, "*.png")) + glob.glob(os.path.join(category_path, "*.jpeg"))
    
    print(f"\n处理类别：{category}")
    print(f"找到 {len(image_files)} 张图像")
    
    total_images += len(image_files)
    
    # 处理每张图像
    for image_path in image_files:
        try:
            print(f"\n处理图像：{image_path}")
            
            # 进行多维标注
            annotation_result = annotation_tool.annotate(image_path)
            
            # 添加类别信息
            annotation_result["category"] = category
            
            # 保存到对应类别
            all_annotations[category].append(annotation_result)
            
            processed_images += 1
            print(f"已处理 {processed_images}/{total_images} 张图像")
            
        except Exception as e:
            print(f"处理图像 {image_path} 失败：{str(e)}")
            continue

# 保存所有标注结果到JSON文件
with open("dataset_annotations.json", "w", encoding="utf-8") as f:
    json.dump(all_annotations, f, ensure_ascii=False, indent=2)

print(f"\n=== 标注完成 ===")
print(f"总共处理：{total_images} 张图像")
print(f"成功处理：{processed_images} 张图像")
print(f"标注结果已保存到：dataset_annotations.json")

# 可选：生成统计信息
print(f"\n=== 标注统计信息 ===")
for category in categories:
    if category in all_annotations:
        print(f"{category}：{len(all_annotations[category])} 张图像")

# 可选：生成组合设计建议的示例
if processed_images > 0:
    print(f"\n=== 组合设计建议示例 ===")
    # 取第一个类别中的第一张图像的标注结果
    for category in categories:
        if len(all_annotations[category]) > 0:
            first_annotation = all_annotations[category][0]
            suggestions = annotation_tool.generate_combination_suggestions(first_annotation)
            print(f"\n图像：{first_annotation['image_path']}")
            print(f"类别：{category}")
            print("组合建议：")
            for i, suggestion in enumerate(suggestions['组合建议'][:3], 1):
                print(f"  {i}. {suggestion['组合名称']}")
                print(f"     纹样：{', '.join(suggestion['组合纹样'])}")
                print(f"     象征意义：{', '.join(suggestion['象征意义'])}")
            break
