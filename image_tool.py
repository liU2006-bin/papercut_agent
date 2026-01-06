import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from PIL import Image as PILImage, ImageOps

class ImageRecognitionTool:
    def __init__(self, model_path='papercut_model_final.h5'):
        """
        初始化图像识别工具
        :param model_path: 模型文件路径
        """
        self.model_path = model_path
        self.model = None
        self.class_names = ['人物类', '动物类', '抽象类', '花样类', '花草植物类']
        self._load_model()
    
    def _load_model(self):
        """
        加载训练好的模型
        """
        try:
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                print(f"成功加载模型: {self.model_path}")
            else:
                raise FileNotFoundError(f"模型文件不存在: {self.model_path}")
        except Exception as e:
            print(f"加载模型失败: {str(e)}")
            raise
    
    def preprocess_image(self, img_path, target_size=(224, 224)):
        """
        预处理图像
        :param img_path: 图像路径
        :param target_size: 目标尺寸
        :return: 预处理后的图像
        """
        img = image.load_img(img_path, target_size=target_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # 归一化
        return img_array
    
    def analyze_visual_features(self, img_path):
        """
        分析图像的视觉特征（不使用cv2）
        :param img_path: 图像路径
        :return: 视觉特征字典
        """
        # 使用Pillow读取图像
        img = PILImage.open(img_path)
        
        # 转换为灰度图
        gray_img = ImageOps.grayscale(img)
        
        # 分析线条特征
        # 简单的边缘检测：计算像素变化率
        img_array = np.array(gray_img)
        height, width = img_array.shape
        
        # 计算水平和垂直方向的像素差异
        horizontal_diff = np.sum(np.abs(img_array[:, 1:] - img_array[:, :-1])) / (height * (width - 1))
        vertical_diff = np.sum(np.abs(img_array[1:, :] - img_array[:-1, :])) / ((height - 1) * width)
        
        edge_density = (horizontal_diff + vertical_diff) / 2 / 255.0  # 归一化到0-1范围
        
        # 判断线条风格
        if edge_density < 0.1:
            line_style = '粗犷'
        else:
            line_style = '细腻'
        
        # 分析镂空技法
        # 简单判断：白色区域比例
        white_pixels = np.sum(img_array > 200) / (height * width)
        if white_pixels > 0.6:
            cutting_technique = '阳刻'  # 保留主体，镂空背景
        elif white_pixels < 0.4:
            cutting_technique = '阴刻'  # 镂空主体，保留背景
        else:
            cutting_technique = '阴阳刻结合'
        
        # 分析色彩
        img_rgb = img.convert('RGB')
        rgb_array = np.array(img_rgb)
        avg_color = np.mean(rgb_array, axis=(0, 1))
        
        # 判断是否为单色
        # 计算颜色通道的标准差，如果很小则认为是单色
        if np.std(avg_color) < 30:
            color = '单色'
        else:
            color = '套色'
        
        # 分析纸张纹理
        # 使用PIL的Laplacian滤波器实现
        from PIL import ImageFilter
        
        # 应用模糊和边缘检测
        blurred = gray_img.filter(ImageFilter.GaussianBlur(radius=2))
        edge_img = blurred.filter(ImageFilter.FIND_EDGES)
        
        # 计算纹理值
        edge_array = np.array(edge_img)
        texture = np.var(edge_array)
        
        if texture < 1000:
            paper_texture = '平滑'
        else:
            paper_texture = '粗糙'
        
        return {
            'line_style': line_style,
            'cutting_technique': cutting_technique,
            'color': color,
            'paper_texture': paper_texture
        }
    
    def predict(self, img_path):
        """
        预测图像类别并分析特征
        :param img_path: 图像路径
        :return: 预测结果和特征分析字典
        """
        if self.model is None:
            raise ValueError("模型未加载")
        
        # 预处理图像
        img_array = self.preprocess_image(img_path)
        
        # 预测
        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class]
        
        # 分析视觉特征
        visual_features = self.analyze_visual_features(img_path)
        
        return {
            'class_name': self.class_names[predicted_class],
            'class_index': int(predicted_class),
            'confidence': float(confidence),
            'all_predictions': {self.class_names[i]: float(predictions[0][i]) for i in range(len(self.class_names))},
            'visual_features': visual_features
        }

# 示例用法
if __name__ == "__main__":
    tool = ImageRecognitionTool()
    # 测试图像路径需要根据实际情况修改
    # result = tool.predict('test_image.jpg')
    # print(result)