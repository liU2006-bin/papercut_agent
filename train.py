# 导入必要的库
import os
import math
import numpy as np
from PIL import Image
import tensorflow as tf
# 启用eager execution (通常不需要，除非调试)
# tf.config.run_functions_eagerly(True)
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential, load_model, Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, GlobalAveragePooling2D, Add, Multiply
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam, AdamW
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix
import shutil

# 设置参数
img_height, img_width = 224, 224
batch_size = 8
epochs = 50  # 保持较大的epoch数量
num_classes = 5
initial_learning_rate = 0.0001  # 适当增加初始学习率

# 数据集路径配置 - 指向当前目录下的五类图像数据集
data_dir = '.'  # 当前目录，直接包含五类图像文件夹

# 定义类别列表，必须与当前目录下的子文件夹名称完全一致
classes = ['人物类', '动物类', '抽象类', '花样类', '花草植物类']

# 1. 数据加载与分割
print("正在进行数据加载与分割...")
all_filepaths = []
all_labels = []

# 遍历每个类别文件夹，收集文件路径和标签
for label_idx, class_name in enumerate(classes):
    class_dir = os.path.join(data_dir, class_name)
    if not os.path.exists(class_dir):
        print(f"警告：类别目录 '{class_dir}' 不存在，跳过。")
        continue
    for filename in os.listdir(class_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            file_path = os.path.join(class_dir, filename)
            all_filepaths.append(file_path)
            all_labels.append(label_idx)  # 使用数字索引作为标签

if len(all_filepaths) == 0:
    print(f"错误：在 '{data_dir}' 及其子类别目录下未找到任何图像文件。")
    print("请确保：")
    print(f"  1. 数据目录 '{data_dir}' 存在。")
    print(f"  2. 该目录下包含子文件夹：{classes}")
    print(f"  3. 子文件夹内包含支持的图像文件。")
    exit(1)

print(f"数据加载完成，共找到 {len(all_filepaths)} 个样本")

# 计算并显示类别分布
from collections import Counter

label_counts = Counter(all_labels)
print("原始类别分布（样本数）:")
for idx, count in label_counts.items():
    print(f"  '{classes[idx]}': {count}")

# 检查每个类别是否有最少样本
min_samples_per_class = 2
for idx, count in label_counts.items():
    if count < min_samples_per_class:
        print(
            f"错误：类别 '{classes[idx]}' 只有 {count} 个样本，至少需要 {min_samples_per_class} 个样本才能进行分层分割。")
        print("请补充数据或调整 `min_samples_per_class` 参数。")
        # 此处可以选择退出，或使用非分层抽样
        # exit(1)

# 分层分割数据集（如果样本足够）
use_stratify = all(count >= 2 for count in label_counts.values()) and len(set(all_labels)) > 1
test_size = 0.2

if use_stratify and len(all_filepaths) * test_size >= len(classes):
    train_files, val_files, train_labels, val_labels = train_test_split(
        all_filepaths, all_labels,
        test_size=test_size,
        stratify=all_labels,
        random_state=42
    )
    print("已使用分层抽样分割数据。")
else:
    print("样本量不足以进行严格分层，使用简单随机分割。")
    train_files, val_files, train_labels, val_labels = train_test_split(
        all_filepaths, all_labels,
        test_size=test_size,
        random_state=42
    )

print(f"训练集样本数: {len(train_files)}")
print(f"验证集样本数: {len(val_files)}")


# 2. 创建数据生成器 (Data Generators)
# 注意：Keras的 `flow_from_directory` 期望一个特定的目录结构。
# 我们需要为训练集和验证集分别创建临时目录，以符合其要求。
def create_temp_data_structure(file_list, label_list, base_temp_dir):
    """根据文件列表和标签列表，创建Keras所需的临时目录结构"""
    temp_dir = base_temp_dir
    # 先清理旧的临时目录（如果存在）
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    # 为每个类别创建子目录
    for class_name in classes:
        os.makedirs(os.path.join(temp_dir, class_name), exist_ok=True)

    # 将文件复制（或链接）到对应的类别文件夹
    for file_path, label_idx in zip(file_list, label_list):
        class_name = classes[label_idx]
        filename = os.path.basename(file_path)
        dest_path = os.path.join(temp_dir, class_name, filename)
        # 使用复制（更稳定）而非软链接
        shutil.copy2(file_path, dest_path)
    return temp_dir


print("正在创建临时数据结构以适配Keras生成器...")
train_temp_dir = './temp_train_data'
val_temp_dir = './temp_val_data'

train_dir = create_temp_data_structure(train_files, train_labels, train_temp_dir)
val_dir = create_temp_data_structure(val_files, val_labels, val_temp_dir)

# 自定义数据生成器类，为抽象类提供更激进的数据增强
class CustomImageDataGenerator(tf.keras.utils.Sequence):
    def __init__(self, base_datagen, abstract_datagen, directory, target_size, batch_size, class_mode, classes, shuffle=True):
        self.base_datagen = base_datagen
        self.abstract_datagen = abstract_datagen
        self.directory = directory
        self.target_size = target_size
        self.batch_size = batch_size
        self.class_mode = class_mode
        self.class_list = classes
        self.shuffle = shuffle
        
        # 创建基础生成器
        self.base_generator = self.base_datagen.flow_from_directory(
            directory=directory, 
            target_size=target_size, 
            batch_size=batch_size, 
            class_mode=class_mode, 
            classes=classes, 
            shuffle=shuffle
        )
        
        # 获取类别索引
        self.abstract_class_index = self.base_generator.class_indices['抽象类']
        
        # 获取抽象类的文件路径
        self.abstract_files = []
        abstract_dir = os.path.join(directory, '抽象类')
        if os.path.exists(abstract_dir):
            for filename in os.listdir(abstract_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    self.abstract_files.append(os.path.join(abstract_dir, filename))
        
        print(f"抽象类文件数量: {len(self.abstract_files)}")
        
        # 预加载所有数据到内存中，以便在__getitem__中使用
        self.all_data = []
        self.all_labels = []
        
        # 遍历所有批次并收集数据
        self.base_generator.reset()
        total_batches = len(self.base_generator)
        for i in range(total_batches):
            x_batch, y_batch = next(self.base_generator)
            self.all_data.append(x_batch)
            self.all_labels.append(y_batch)
        
        # 将所有批次合并为一个大的数组
        self.all_data = np.concatenate(self.all_data)
        self.all_labels = np.concatenate(self.all_labels)
        
        print(f"预加载完成，共 {len(self.all_data)} 个样本")
        
    def __len__(self):
        # 返回一个epoch的步数
        return math.ceil(len(self.all_data) / self.batch_size)
    
    def __getitem__(self, idx):
        # 计算当前批次的起始和结束索引
        start_idx = idx * self.batch_size
        end_idx = min((idx + 1) * self.batch_size, len(self.all_data))
        
        # 获取当前批次的数据和标签
        x_batch = self.all_data[start_idx:end_idx]
        y_batch = self.all_labels[start_idx:end_idx]
        
        # 如果批次大小不足，进行零填充或循环填充
        if len(x_batch) < self.batch_size:
            # 计算需要填充的数量
            pad_size = self.batch_size - len(x_batch)
            
            # 随机选择pad_size个样本进行填充
            pad_indices = np.random.choice(len(self.all_data), pad_size, replace=False)
            pad_x = self.all_data[pad_indices]
            pad_y = self.all_labels[pad_indices]
            
            # 拼接原始批次和填充的批次
            x_batch = np.concatenate([x_batch, pad_x])
            y_batch = np.concatenate([y_batch, pad_y])
        
        # 检查批次中是否有抽象类样本
        batch_size = len(x_batch)
        abstract_mask = np.argmax(y_batch, axis=1) == self.abstract_class_index
        
        # 统计抽象类样本数量
        abstract_count = np.sum(abstract_mask)
        
        # 如果抽象类样本较少，增加其数量
        if self.abstract_files and abstract_count < batch_size * 0.3:  # 确保至少有30%的抽象类样本
            # 计算需要增加的抽象类样本数量
            needed_abstracts = max(1, int(batch_size * 0.3) - abstract_count)
            
            # 随机选择要替换的非抽象类样本索引
            non_abstract_indices = np.where(~abstract_mask)[0]
            if len(non_abstract_indices) >= needed_abstracts:
                replace_indices = np.random.choice(non_abstract_indices, size=needed_abstracts, replace=False)
            else:
                replace_indices = non_abstract_indices
            
            # 替换为增强的抽象类样本
            for i in replace_indices:
                img_path = np.random.choice(self.abstract_files)
                img = Image.open(img_path).convert('RGB')
                img = img.resize(self.target_size)
                
                # 使用抽象类专用生成器增强
                img_array = np.array(img)
                img_array = np.expand_dims(img_array, axis=0)
                augmented_img = next(self.abstract_datagen.flow(img_array, batch_size=1, shuffle=False))[0]
                
                # 更新图像和标签
                x_batch[i] = augmented_img
                y_batch[i] = np.zeros_like(y_batch[i])
                y_batch[i][self.abstract_class_index] = 1
        
        # 为批次中已有的抽象类样本应用更激进的增强
        for i in range(batch_size):
            if abstract_mask[i] and self.abstract_files:
                # 对抽象类样本重新应用增强
                img_path = np.random.choice(self.abstract_files)
                img = Image.open(img_path).convert('RGB')
                img = img.resize(self.target_size)
                
                # 使用抽象类专用生成器增强
                img_array = np.array(img)
                img_array = np.expand_dims(img_array, axis=0)
                augmented_img = next(self.abstract_datagen.flow(img_array, batch_size=1, shuffle=False))[0]
                
                x_batch[i] = augmented_img
        
        return x_batch, y_batch
    
    @property
    def samples(self):
        return self.base_generator.samples
    
    @property
    def num_classes(self):
        return self.base_generator.num_classes
    
    @property
    def class_indices(self):
        return self.base_generator.class_indices
    
    @property
    def classes(self):
        return self.base_generator.classes
    
    def reset(self):
        self.base_generator.reset()

# 基础数据增强配置
base_train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    vertical_flip=False,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest'
)

# 抽象类专用的激进数据增强配置
abstract_train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=45,  # 更激进的旋转
    width_shift_range=0.2,  # 更大的平移
    height_shift_range=0.2,
    shear_range=0.2,  # 更大的剪切
    zoom_range=0.3,  # 更大的缩放
    horizontal_flip=True,
    vertical_flip=True,  # 允许垂直翻转
    brightness_range=[0.6, 1.4],  # 更宽的亮度范围
    channel_shift_range=0.2,  # 颜色通道偏移
    fill_mode='nearest'
)

# 验证集数据增强
validation_datagen = ImageDataGenerator(
    rescale=1. / 255
)

print("创建数据生成器...")

# 创建自定义的训练生成器，为抽象类应用更激进的增强
train_generator = CustomImageDataGenerator(
    base_train_datagen,
    abstract_train_datagen,
    train_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    classes=classes,
    shuffle=True
)

validation_generator = validation_datagen.flow_from_directory(
    val_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    classes=classes,
    shuffle=False  # 验证集不要打乱，便于分析
)

print(f"训练集: {train_generator.samples} 样本, {train_generator.num_classes} 类别")
print(f"验证集: {validation_generator.samples} 样本")

# 修正步骤计算：使用向上取整，确保所有样本都被用到
steps_per_epoch = math.ceil(train_generator.samples / batch_size)
validation_steps = math.ceil(validation_generator.samples / batch_size)
print(f"训练步数/epoch: {steps_per_epoch}")
print(f"验证步数: {validation_steps}")

# 3. 计算类别权重（修正版）
print("计算类别权重以处理不平衡数据...")
# 从生成器中获取真实的训练标签索引
train_labels_for_weight = train_generator.classes
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(train_labels_for_weight),
    y=train_labels_for_weight
)
class_weight_dict = {i: weight for i, weight in enumerate(class_weights)}
print("类别权重:", class_weight_dict)

# 4. 设置学习率调度器
# 使用更有效的余弦退火学习率调度器
cosine_decay_schedule = tf.keras.optimizers.schedules.CosineDecayRestarts(
    initial_learning_rate=initial_learning_rate,
    first_decay_steps=20 * steps_per_epoch,  # 调整第一个周期的步数
    t_mul=2.0,  # 周期倍增因子
    m_mul=0.85,  # 调整衰减因子
    name='cosine_decay_restarts'
)

# 5. 构建或加载模型 - 使用优化的自定义CNN模型，适合小数据集
model_path = 'papercut_model_improved.h5'
if os.path.exists(model_path):
    print(f"加载已保存的模型: {model_path}")
    model = load_model(model_path)
    # 重新编译以应用新的学习率等设置
    optimizer = AdamW(learning_rate=cosine_decay_schedule, weight_decay=1e-4)
    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    print("模型加载并重新编译成功。")
else:
    print("构建优化的自定义CNN模型...")
    
    # 增加模型深度和宽度，添加Residual连接，使用更高效的架构
    
    # 输入层
    inputs = Input(shape=(img_height, img_width, 3))
    
    # 第一层卷积块 - 无残差连接
    x = Conv2D(64, (3, 3), padding='same')(inputs)
    x = BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)
    x = Conv2D(64, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.2)(x)
    
    # 第二层卷积块 - 无残差连接
    x = Conv2D(128, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)
    x = Conv2D(128, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.2)(x)
    
    # 第三层卷积块 - Residual连接
    shortcut = x
    # 添加1x1卷积调整shortcut通道数以匹配后续输出
    shortcut = Conv2D(256, (1, 1), padding='same')(shortcut)
    shortcut = BatchNormalization()(shortcut)
    
    x = Conv2D(256, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)
    x = Conv2D(256, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = Add()([x, shortcut])  # Residual连接
    x = tf.keras.layers.Activation('relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.2)(x)
    
    # 第四层卷积块 - Residual连接
    shortcut = x
    # 添加1x1卷积调整shortcut通道数以匹配后续输出
    shortcut = Conv2D(512, (1, 1), padding='same')(shortcut)
    shortcut = BatchNormalization()(shortcut)
    
    x = Conv2D(512, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)
    x = Conv2D(512, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = Add()([x, shortcut])  # Residual连接
    x = tf.keras.layers.Activation('relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.2)(x)
    
    # 第五层卷积块 - Residual连接
    shortcut = x
    # 添加1x1卷积调整shortcut通道数以匹配后续输出
    shortcut = Conv2D(768, (1, 1), padding='same')(shortcut)
    shortcut = BatchNormalization()(shortcut)
    
    x = Conv2D(768, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)
    x = Conv2D(768, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = Add()([x, shortcut])  # Residual连接
    x = tf.keras.layers.Activation('relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.2)(x)
    
    # 添加通道注意力机制
    attention = GlobalAveragePooling2D()(x)
    attention = Dense(128, activation='relu')(attention)
    attention = Dense(768, activation='sigmoid')(attention)
    # 使用Reshape层替代tf.expand_dims
    attention = tf.keras.layers.Reshape((1, 1, 768))(attention)
    attention = Multiply()([x, attention])
    
    # 结合原始特征和注意力加权特征
    x = Add()([x, attention])
    
    # 全连接层
    x = Flatten()(x)
    x = Dense(1024, activation='relu', kernel_regularizer=l2(5e-5))(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(512, activation='relu', kernel_regularizer=l2(5e-5))(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs, x)

    # 使用AdamW优化器，提供更好的正则化效果
    optimizer = AdamW(learning_rate=cosine_decay_schedule, beta_1=0.9, beta_2=0.999, epsilon=1e-08, weight_decay=1e-4)
    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    print("优化的自定义CNN模型构建完成！")

# 6. 设置回调函数
callbacks = [
    EarlyStopping(
        monitor='val_accuracy',
        patience=30,  # 进一步增加patience值，让模型有更多机会收敛
        restore_best_weights=True,
        verbose=1
    ),
    ModelCheckpoint(
        'best_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
]


# 自定义回调，用于输出训练进度
class BatchLogger(tf.keras.callbacks.Callback):
    def on_epoch_begin(self, epoch, logs=None):
        print(f"\n=== Epoch {epoch + 1}/{epochs} 开始 ===")

    def on_epoch_end(self, epoch, logs=None):
        print(f"=== Epoch {epoch + 1}/{epochs} 结束 ===")
        print(f"  训练损失: {logs.get('loss', 'N/A'):.4f}, 训练准确率: {logs.get('accuracy', 'N/A'):.4f}")
        print(f"  验证损失: {logs.get('val_loss', 'N/A'):.4f}, 验证准确率: {logs.get('val_accuracy', 'N/A'):.4f}")


callbacks.append(BatchLogger())

# 6. 训练模型
print("\n" + "=" * 50)
print("开始训练模型...")
print("=" * 50)

history = None
val_loss = None
val_accuracy = None

try:
    # 训练模型
    history = model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=validation_steps,
        callbacks=callbacks,
        class_weight=class_weight_dict,
        verbose=0  # 由自定义回调控制输出
    )
    print("\n训练完成！")
    
    # 7. 评估模型
    print("\n" + "=" * 50)
    print("模型评估")
    print("=" * 50)
    
    # 加载并评估最佳模型
    if os.path.exists('best_model.h5'):
        best_model = load_model('best_model.h5')
        print("加载最佳模型进行评估...")
        val_loss, val_accuracy = best_model.evaluate(validation_generator, steps=validation_steps, verbose=0)
        print(f"最佳模型验证准确率: {val_accuracy * 100:.2f}%")
        model = best_model  # 后续使用最佳模型
    else:
        print("未找到 'best_model.h5'，使用最终epoch的模型。")
        val_loss, val_accuracy = model.evaluate(validation_generator, steps=validation_steps, verbose=0)
        print(f"最终模型验证准确率: {val_accuracy * 100:.2f}%")
    
    # 8. 生成详细评估报告
    print("\n生成分类报告与混淆矩阵...")
    validation_generator.reset()
    predictions = model.predict(validation_generator, steps=validation_steps, verbose=0)
    
    # 处理预测结果，确保长度与验证集样本数一致
    y_pred = np.argmax(predictions, axis=1)[:validation_generator.samples]
    y_true = validation_generator.classes[:validation_generator.samples]
    
    # 分类报告
    class_names = list(validation_generator.class_indices.keys())
    report = classification_report(y_true, y_pred, target_names=class_names, digits=4)
    print("分类报告:")
    print(report)
    
    # 保存报告
    with open('classification_report.txt', 'w', encoding='utf-8') as f:
        f.write("安塞剪纸纹样识别模型 - 分类报告\n")
        f.write("=" * 60 + "\n\n")
        f.write(report)
    
    # 混淆矩阵
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title('混淆矩阵 (Confusion Matrix)')
    plt.xlabel('预测标签 (Predicted)')
    plt.ylabel('真实标签 (True)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()  # 不显示，只保存
    
    # 9. 绘制训练历史
    print("\n绘制训练历史图表...")
    if history:
        acc = history.history['accuracy']
        val_acc = history.history.get('val_accuracy', [])
        loss = history.history['loss']
        val_loss = history.history.get('val_loss', [])
    
        epochs_range = range(1, len(acc) + 1)
    
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
        # 准确率曲线
        ax1.plot(epochs_range, acc, 'b-', label='训练准确率', linewidth=2)
        if val_acc:
            ax1.plot(epochs_range, val_acc, 'r-', label='验证准确率', linewidth=2)
        ax1.set_title('训练与验证准确率')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim([0, 1.05])
    
        # 损失曲线
        ax2.plot(epochs_range, loss, 'b-', label='训练损失', linewidth=2)
        if val_loss:
            ax2.plot(epochs_range, val_loss, 'r-', label='验证损失', linewidth=2)
        ax2.set_title('训练与验证损失')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
        plt.tight_layout()
        plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
        plt.close()  # 不显示，只保存
    
    # 10. 保存最终模型
    final_model_path = 'papercut_model_final.h5'
    model.save(final_model_path)
    print(f"\n最终模型已保存为: {final_model_path}")
except Exception as e:
    print(f"\n训练或评估过程中发生错误: {e}")
    import traceback
    traceback.print_exc()
finally:
    # 所有训练和评估完成后，清理临时目录
    print("清理临时数据目录...")
    if os.path.exists(train_dir):
        shutil.rmtree(train_dir)
    if os.path.exists(val_dir):
        shutil.rmtree(val_dir)

print("=" * 50)
print("所有流程执行完毕！")
print("=" * 50)