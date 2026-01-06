import os
from collections import Counter

classified_path = './classified_dataset'
categories = ['花草', '人物', '动物', '剪纸艺术', '其他']

classification_stats = {}
for category in categories:
    category_path = os.path.join(classified_path, category)
    if os.path.exists(category_path):
        image_files = [f for f in os.listdir(category_path) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        classification_stats[category] = len(image_files)
    else:
        classification_stats[category] = 0

print("分类后的图像数量分布:")
for category, count in classification_stats.items():
    print(f"{category}: {count} 张")

print(f"\n总分类图像数: {sum(classification_stats.values())}")
