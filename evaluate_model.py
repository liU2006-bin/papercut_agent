import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from sklearn.model_selection import train_test_split
import math
import glob

# 设置参数
img_height, img_width = 224, 224
batch_size = 8
classes = ['人物类', '动物类', '抽象类', '花样类', '花草植物类']

def evaluate_model():
    # 检查模型文件是否存在
    model_path = 'best_model.h5'
    if not os.path.exists(model_path):
        print(f"错误：模型文件 {model_path} 不存在！")
        return False
    
    # 加载模型
    print(f"正在加载模型：{model_path}")
    model = load_model(model_path)
    
    # 收集所有图像文件路径和标签
    all_filepaths = []
    all_labels = []
    
    for label_idx, class_name in enumerate(classes):
        class_dir = os.path.join('.', class_name)
        if not os.path.exists(class_dir):
            print(f"警告：类别目录 '{class_dir}' 不存在，跳过。")
            continue
        
        # 获取该类别下的所有图像文件
        for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            files = glob.glob(os.path.join(class_dir, f'*{ext}'))
            all_filepaths.extend(files)
            all_labels.extend([label_idx] * len(files))
    
    if len(all_filepaths) == 0:
        print("错误：未找到任何图像文件！")
        return False
    
    print(f"共找到 {len(all_filepaths)} 个样本")
    
    # 分割数据集（80%训练，20%验证）
    _, val_files, _, val_labels = train_test_split(
        all_filepaths, all_labels,
        test_size=0.2,
        stratify=all_labels,
        random_state=42
    )
    
    print(f"验证集样本数: {len(val_files)}")
    
    # 预处理验证数据
    def preprocess_image(filepath):
        img = load_img(filepath, target_size=(img_height, img_width))
        img_array = img_to_array(img)
        img_array = img_array / 255.0
        return img_array
    
    val_images = np.array([preprocess_image(file) for file in val_files])
    val_labels_categorical = tf.keras.utils.to_categorical(val_labels, num_classes=len(classes))
    
    # 评估模型
    print("正在评估模型...")
    val_loss, val_accuracy = model.evaluate(val_images, val_labels_categorical, batch_size=batch_size, verbose=1)
    
    print(f"模型准确率：{val_accuracy * 100:.2f}%")
    
    # 检查是否达到50%的准确率要求
    if val_accuracy >= 0.5:
        print("模型准确率达到了50%的要求！")
        return True
    else:
        print("模型准确率未达到50%的要求！")
        return False

if __name__ == "__main__":
    import tensorflow as tf
    evaluate_model()
