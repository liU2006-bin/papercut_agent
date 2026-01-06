import os
import glob

# 定义五个类别文件夹名称
categories = ['人物类', '动物类', '抽象类', '花样类', '花草植物类']

print("开始统计每个类别的图像数量...")
for category in categories:
    # 构建文件夹路径
    category_path = os.path.join('.', category)
    
    # 检查文件夹是否存在
    if not os.path.exists(category_path):
        print(f"警告：文件夹 {category_path} 不存在！")
        continue
    
    # 使用glob获取所有图像文件
    image_patterns = ['.png', '.jpg', '.jpeg', '.bmp']
    total_images = 0
    
    for pattern in image_patterns:
        images = glob.glob(os.path.join(category_path, f'*{pattern}'))
        total_images += len(images)
    
    print(f"{category}: {total_images} 张图像")

print("统计完成！")
