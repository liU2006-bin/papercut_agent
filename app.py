import streamlit as st
from PIL import Image
import numpy as np
import os
import json
from pathlib import Path
from agent import PapercutAgent
from image_tool import ImageRecognitionTool



# 初始化图像识别工具
@st.cache_resource
def get_image_tool():
    try:
        return ImageRecognitionTool()
    except Exception as e:
        st.error(f"图像识别工具初始化失败: {str(e)}")
        return None

# 初始化多维标注工具
@st.cache_resource
def get_annotation_tool():
    try:
        from multidimensional_annotation_tool import MultiDimensionalAnnotationTool
        return MultiDimensionalAnnotationTool()
    except ImportError as e:
        # 如果是缺少依赖（如torch），只在调试模式下显示警告
        if st.get_option('client.showErrorDetails'):
            st.warning(f"多维标注工具未初始化（缺少依赖）: {str(e)}")
        return None
    except Exception as e:
        st.error(f"多维标注工具初始化失败: {str(e)}")
        return None

# 初始化设计工具
@st.cache_resource
def get_design_tool():
    try:
        from design_tool import DesignTool
        return DesignTool()
    except Exception as e:
        st.error(f"设计工具初始化失败: {str(e)}")
        return None

# 创建智能体实例
def get_agent():
    if "DEEPSEEK_API_KEY" not in os.environ:
        return None
    try:
        return PapercutAgent()
    except Exception as e:
        st.error(f"智能体初始化失败: {str(e)}")
        return None

# 获取工具实例
image_tool = get_image_tool()
annotation_tool = get_annotation_tool()
design_tool = get_design_tool()
agent = get_agent()

# 设置页面配置
st.set_page_config(
    page_title="安塞剪纸智能体",
    page_icon="✂️",
    layout="wide"
)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = "DEEPSEEK_API_KEY" in os.environ

# 页面标题和介绍
st.title("✂️ 安塞剪纸智能体")
st.write("欢迎使用安塞剪纸智能体！上传一张剪纸图像，我将为您识别其类别并提供设计建议。")

# 尝试加载模型
if image_tool:
    load_success = image_tool.load_model()
    if load_success:
        st.success("✅ 所有模型已就绪，可以正常使用")
    else:
        st.warning("⚠️ 模型加载失败，部分功能可能受限")
else:
    st.warning("⚠️ 图像识别工具未初始化，部分功能可能受限")

# 创建侧边栏
with st.sidebar:
    st.header("功能说明")
    st.write("1. 上传剪纸图像进行识别")
    st.write("2. 对剪纸图像进行多维标注")
    st.write("3. 查询剪纸纹样知识")
    st.write("4. 生成各种主题的设计方案")
    st.write("5. 与智能体进行聊天互动")
    st.write("\n支持的类别：人物类、动物类、抽象类、花样类、花草植物类")
    
    st.subheader("多维标注说明")
    st.write("- **内容/对象**：纹样主体、辅助元素、构图结构")
    st.write("- **形式/视觉**：线条风格、镂空技法、色彩、纸张纹理")
    st.write("- **文化/语义**：吉祥寓意、民俗用途、地域特色、神话传说")
    st.write("- **关联/情境**：传承人、创作年代、流派、当代应用")
    
    # API密钥设置
    if not st.session_state.api_key_set:
        api_key = st.text_input("DeepSeek API密钥", type="password")
        if api_key:
            os.environ["DEEPSEEK_API_KEY"] = api_key
            st.session_state.api_key_set = True
            st.rerun()
    else:
        st.info("DeepSeek API密钥已设置")

# 聊天界面
st.subheader("💬 与智能体聊天")

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入区域
user_input = st.chat_input("请输入您的问题或需求...")

# 处理用户输入
if user_input:
    # 添加用户消息到会话状态
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # 如果没有智能体实例，提示用户设置API密钥
    if not agent:
        with st.chat_message("assistant"):
            st.error("请先在侧边栏设置DeepSeek API密钥")
    else:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            with st.spinner("智能体正在思考..."):
                try:
                    response = agent.run(user_input)
                    
                    full_response = response
                    message_placeholder.markdown(full_response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    error_message = f"智能体执行失败: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

# 图像识别和设计方案区域
col1, col2 = st.columns(2)

with col1:
    st.subheader("🖼️ 剪纸图像识别")
    
    # 创建文件上传组件
    uploaded_file = st.file_uploader("选择一张剪纸图像", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # 显示上传的图像
        image = Image.open(uploaded_file)
        st.image(image, caption="上传的剪纸图像", use_container_width=True)
        
        # 保存图像到临时文件
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 识别按钮
        if st.button("识别图像", key="recognize_btn"):
            if not image_tool:
                st.error("图像识别工具未初始化，请检查模型文件")
            else:
                with st.spinner("正在识别..."):
                    try:
                        # 直接调用图像识别工具
                        result = image_tool.predict(temp_path)
                        
                        # 格式化结果
                        result_text = f"""**图像识别结果**

**类别**: {result['class_name']}

**置信度**: {result['confidence']:.2%}

**各类别置信度**:
"""
                        for class_name, prob in result['all_predictions'].items():
                            result_text += f"- {class_name}: {prob:.2%}\n"
                        
                        result_text += f"""
**视觉特征分析**:
- 线条风格: {result['visual_features']['line_style']}
- 镂空技法: {result['visual_features']['cutting_technique']}
- 色彩: {result['visual_features']['color']}
- 纸张纹理: {result['visual_features']['paper_texture']}
"""
                        
                        # 添加到聊天历史
                        st.session_state.messages.append({"role": "user", "content": "识别这张剪纸图像"})
                        st.session_state.messages.append({"role": "assistant", "content": result_text})
                        
                        # 显示结果
                        st.success("识别完成！")
                        st.markdown(result_text)
                    except Exception as e:
                        st.error(f"识别失败: {str(e)}")
                    finally:
                        # 删除临时文件
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
        
        # 多维标注按钮
        if st.button("多维标注", key="annotate_btn"):
            if not annotation_tool:
                st.error("多维标注工具未初始化")
            else:
                with st.spinner("正在进行多维标注..."):
                    try:
                        # 先进行图像识别获取类别
                        recognition_result = image_tool.predict(temp_path)
                        class_name = recognition_result['class_name']
                        
                        # 进行多维标注
                        annotation_result = annotation_tool.annotate(temp_path)
                        
                        # 格式化结果
                        content_obj = annotation_result.get('content_object', {})
                        form_vis = annotation_result.get('form_visual', {})
                        cultural_sem = annotation_result.get('cultural_semantic', {})
                        context_rel = annotation_result.get('context_relation', {})
                        
                        def format_list(items):
                            if isinstance(items, list):
                                return '、'.join(str(item) for item in items) if items else '无数据'
                            return str(items) if items else '无数据'
                        
                        result_text = f"""**多维标注结果**

**图像类别**: {class_name}

---

### 1. 内容/对象维度
- **辅助元素**: {format_list(content_obj.get('辅助元素', []))}
- **构图结构**: {format_list(content_obj.get('构图结构', []))}

### 2. 形式/视觉维度
- **线条风格**: {form_vis.get('线条风格', '无数据')}
- **镂空技法**: {form_vis.get('镂空技法', '无数据')}
- **色彩**: {form_vis.get('色彩', '无数据')}
- **纸张纹理**: {form_vis.get('纸张纹理', '无数据')}

### 3. 文化/语义维度
- **吉祥寓意**: {format_list(cultural_sem.get('吉祥寓意', []))}
- **民俗用途**: {format_list(cultural_sem.get('民俗用途', []))}
- **地域特色**: {format_list(cultural_sem.get('地域特色', []))}

### 4. 关联/情境维度
- **应用场景**: {format_list(context_rel.get('应用场景', []))}
"""
                        
                        # 添加到聊天历史
                        st.session_state.messages.append({"role": "user", "content": "对这张剪纸图像进行多维标注"})
                        st.session_state.messages.append({"role": "assistant", "content": result_text})
                        
                        st.success("多维标注完成！")
                        st.markdown(result_text)
                    except Exception as e:
                        st.error(f"标注失败: {str(e)}")
                    finally:
                        # 删除临时文件
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

with col2:
    st.subheader("🎨 设计方案生成")
    
    # 设计主题选择
    theme = st.selectbox(
        "选择设计主题",
        ["婚礼", "节日", "随机"]
    )
    
    # 生成设计方案按钮
    if st.button("生成设计方案", key="design_btn"):
        with st.spinner("正在生成..."):
            try:
                # 直接调用设计工具生成方案
                if theme == "婚礼":
                    design_result = design_tool.get_wedding_combination()
                elif theme == "节日":
                    design_result = design_tool.get_festival_combination("春节")
                else:
                    design_result = design_tool.get_random_combination()
                
                # 格式化设计结果
                if isinstance(design_result, dict):
                    # 从字典中提取信息
                    patterns = design_result.get('patterns', [])
                    layout = design_result.get('layout', '')
                    color_suggestions = design_result.get('color_suggestions', '')
                    description = design_result.get('description', '')
                    
                    # 构建结果文本
                    result_text = f"**设计方案**\n\n"
                    result_text += f"### 纹样组合\n"
                    for i, pattern in enumerate(patterns, 1):
                        result_text += f"{i}. **{pattern.get('name', '未知纹样')}** - {pattern.get('meaning', '无描述')}\n"
                    
                    if layout:
                        result_text += f"\n### 布局建议\n{layout}\n"
                    
                    if color_suggestions:
                        result_text += f"\n### 色彩建议\n{color_suggestions}\n"
                    
                    if description:
                        result_text += f"\n### 设计说明\n{description}\n"
                else:
                    # 如果返回的是字符串，直接使用
                    result_text = design_result
                
                # 添加到聊天历史
                query = f"请生成一个{theme}主题的剪纸组合设计方案，包含纹样组合、布局建议、颜色建议"
                st.session_state.messages.append({"role": "user", "content": query})
                st.session_state.messages.append({"role": "assistant", "content": result_text})
                
                st.success("设计方案已生成！")
                st.markdown(result_text)
            except Exception as e:
                st.error(f"生成失败: {str(e)}")
    
    # 基于标注生成组合建议按钮
    st.write("\n**基于多维标注的组合设计**")
    st.write("可以上传图像进行多维标注后，生成个性化的组合设计建议")
    
    uploaded_annotate_file = st.file_uploader("上传图像进行标注并生成组合设计", type=["jpg", "jpeg", "png"], key="annotate_design_uploader")
    
    if uploaded_annotate_file is not None:
        # 保存图像到临时文件
        temp_annotate_path = f"temp_annotate_{uploaded_annotate_file.name}"
        with open(temp_annotate_path, "wb") as f:
            f.write(uploaded_annotate_file.getbuffer())
        
        # 生成基于标注的设计按钮
        if st.button("标注并生成组合设计", key="annotate_design_btn"):
            with st.spinner("正在进行标注和设计生成..."):
                try:
                    # 先进行图像识别
                    recognition_result = image_tool.predict(temp_annotate_path)
                    
                    # 进行多维标注
                    annotation_result = annotation_tool.annotate(temp_annotate_path)
                    
                    # 基于标注生成组合设计
                    if agent:
                        content_obj = annotation_result.get('content_object', {})
                        form_vis = annotation_result.get('form_visual', {})
                        cultural_sem = annotation_result.get('cultural_semantic', {})
                        context_rel = annotation_result.get('context_relation', {})
                        
                        def format_list(items):
                            if isinstance(items, list):
                                return '、'.join(str(item) for item in items) if items else '无数据'
                            return str(items) if items else '无数据'
                        
                        query = f"""基于以下多维标注结果，生成一个组合设计建议：

**图像类别**: {recognition_result['class_name']}

**多维标注**:
1. 内容/对象:
   - 纹样主体: {format_list(content_obj.get('纹样主体', []))}
   - 辅助元素: {format_list(content_obj.get('辅助元素', []))}
   - 构图结构: {format_list(content_obj.get('构图结构', []))}

2. 形式/视觉:
   - 线条风格: {form_vis.get('线条风格', '无数据')}
   - 镂空技法: {form_vis.get('镂空技法', '无数据')}
   - 色彩: {form_vis.get('色彩', '无数据')}
   - 纸张纹理: {form_vis.get('纸张纹理', '无数据')}

3. 文化/语义:
   - 吉祥寓意: {format_list(cultural_sem.get('吉祥寓意', []))}
   - 民俗用途: {format_list(cultural_sem.get('民俗用途', []))}
   - 地域特色: {format_list(cultural_sem.get('地域特色', []))}

4. 关联/情境:
   - 相关纹样: {format_list([p['pattern_name'] for p in context_rel.get('相关纹样', [])])}
   - 应用场景: {format_list(context_rel.get('应用场景', []))}

请生成一个符合该剪纸特点的组合设计建议，包括推荐的搭配纹样、布局方式和色彩搭配。"""
                        
                        design_response = agent.run(query)
                        
                        # 格式化最终结果
                        result_text = f"""**图像识别结果**: {recognition_result['class_name']}

**多维标注结果**:
- 纹样主体: {format_list(content_obj.get('纹样主体', []))}
- 构图结构: {format_list(content_obj.get('构图结构', []))}
- 吉祥寓意: {format_list(cultural_sem.get('吉祥寓意', []))}
- 应用场景: {format_list(context_rel.get('应用场景', []))}

**组合设计建议**:
{design_response}
"""
                    else:
                        content_obj = annotation_result.get('content_object', {})
                        cultural_sem = annotation_result.get('cultural_semantic', {})
                        context_rel = annotation_result.get('context_relation', {})
                        
                        def format_list(items):
                            if isinstance(items, list):
                                return '、'.join(str(item) for item in items) if items else '无数据'
                            return str(items) if items else '无数据'
                        
                        result_text = f"""**图像识别结果**: {recognition_result['class_name']}

**多维标注结果**:
- 纹样主体: {format_list(content_obj.get('纹样主体', []))}
- 吉祥寓意: {format_list(cultural_sem.get('吉祥寓意', []))}

请在侧边栏设置API密钥后生成组合设计建议。"""
                    
                    # 添加到聊天历史
                    st.session_state.messages.append({"role": "user", "content": "标注图像并生成组合设计"})
                    st.session_state.messages.append({"role": "assistant", "content": result_text})
                    
                    st.success("处理完成！")
                    st.markdown(result_text)
                except Exception as e:
                    st.error(f"处理失败: {str(e)}")
                finally:
                    # 删除临时文件
                    if os.path.exists(temp_annotate_path):
                        os.remove(temp_annotate_path)

# 页脚信息
st.markdown("---")
st.markdown("安塞剪纸智能体 © 2025 - 基于深度学习和自然语言处理技术")
