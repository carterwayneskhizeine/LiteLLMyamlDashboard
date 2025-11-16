import streamlit as st
import yaml
import pandas as pd
import subprocess
import os
import sys

# 页面配置
st.set_page_config(
    page_title="AI Models Dashboard",
    page_icon="🤖",
    layout="wide"
)

# 读取YAML文件
@st.cache_data(show_spinner=False)
def load_data():
    try:
        with open('processed_models.yaml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # 转换为DataFrame
        models = []
        for item in data['model_list']:
            model_info = item['model_info'].copy()
            model_info['model_name'] = item['model_name']
            models.append(model_info)

        df = pd.DataFrame(models)

        # 重新排列列顺序
        cols = ['model_name', 'input_cost_1M_token', 'output_cost_1M_token',
                'max_tokens', 'max_output_tokens', 'supports_reasoning',
                'supports_vision']

        # 只保留存在的列
        cols = [col for col in cols if col in df.columns]
        other_cols = [col for col in df.columns if col not in cols]
        df = df[cols + other_cols]

        # 填充NaN值
        df['supports_reasoning'] = df['supports_reasoning'].fillna(False)
        df['supports_vision'] = df['supports_vision'].fillna(False)

        return df
    except Exception as e:
        st.error(f"读取数据文件失败: {e}")
        return pd.DataFrame()

# 加载数据
df = load_data()

# 检查是否需要显示数据更新成功消息
if 'data_updated' in st.session_state and st.session_state.data_updated:
    st.success("✅ 配置导入成功！数据已更新", icon="✅")
    # 清除标志
    del st.session_state['data_updated']

# 价格范围过滤
st.sidebar.subheader("价格范围")

# 输入成本过滤
min_input_cost = st.sidebar.number_input(
    "最低输入成本 ($/1M tokens)",
    min_value=0.0,
    max_value=float(df['input_cost_1M_token'].max()),
    value=0.0
)
max_input_cost = st.sidebar.number_input(
    "最高输入成本 ($/1M tokens)",
    min_value=0.0,
    max_value=float(df['input_cost_1M_token'].max()),
    value=float(df['input_cost_1M_token'].max())
)

# 输出成本过滤
min_output_cost = st.sidebar.number_input(
    "最低输出成本 ($/1M tokens)",
    min_value=0.0,
    max_value=float(df['output_cost_1M_token'].max()),
    value=0.0
)
max_output_cost = st.sidebar.number_input(
    "最高输出成本 ($/1M tokens)",
    min_value=0.0,
    max_value=float(df['output_cost_1M_token'].max()),
    value=float(df['output_cost_1M_token'].max())
)

# 功能过滤
st.sidebar.subheader("功能支持")
show_reasoning = st.sidebar.checkbox("支持推理 (Reasoning)", value=False)
show_vision = st.sidebar.checkbox("支持视觉 (Vision)", value=False)

# 免费模型过滤
show_free_only = st.sidebar.checkbox("仅显示免费模型", value=False)

# 模型名称搜索
search_term = st.sidebar.text_input("🔎 搜索模型名称", "")

st.sidebar.markdown("---")

# 初始化会话状态
if 'show_uploader' not in st.session_state:
    st.session_state.show_uploader = False
if 'uploaded_file_path' not in st.session_state:
    st.session_state.uploaded_file_path = None

# 导入配置功能
col1, col2 = st.sidebar.columns([1, 1])
with col1:
    if st.button("导入配置", use_container_width=True):
        st.session_state.show_uploader = True
        st.rerun()

with col2:
    if st.button("刷新数据", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# 文件上传区域
if st.session_state.show_uploader or st.session_state.uploaded_file_path:
    st.sidebar.markdown("---")
    st.sidebar.subheader("上传配置文件")

    if not st.session_state.uploaded_file_path:
        uploaded_file = st.sidebar.file_uploader(
            "选择YAML文件",
            type=['yaml', 'yml'],
            key="yaml_uploader"
        )

        if uploaded_file is not None:
            try:
                # 保存临时文件
                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)
                temp_file_path = os.path.join(temp_dir, uploaded_file.name)

                with open(temp_file_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())

                st.session_state.uploaded_file_path = temp_file_path
                st.rerun()

            except Exception as e:
                st.sidebar.error(f"❌ 文件保存失败: {str(e)}")

    # 显示已选择的文件和处理按钮
    if st.session_state.uploaded_file_path:
        file_name = os.path.basename(st.session_state.uploaded_file_path)
        st.sidebar.info(f"📄 已选择: {file_name}")

        col1, col2 = st.sidebar.columns([1, 1])
        with col1:
            if st.sidebar.button("⚙️ 开始处理", key="process_button", use_container_width=True):
                try:
                    # 调用 process_yaml.py 处理文件
                    with st.spinner("处理中..."):
                        result = subprocess.run(
                            [sys.executable, 'process_yaml.py', st.session_state.uploaded_file_path, 'processed_models.yaml'],
                            capture_output=True,
                            text=True,
                            timeout=30
                        )

                    if result.returncode == 0:
                        # 清理临时文件和状态
                        if os.path.exists(st.session_state.uploaded_file_path):
                            os.remove(st.session_state.uploaded_file_path)
                        st.session_state.uploaded_file_path = None
                        st.session_state.show_uploader = False

                        # 设置数据已更新标志
                        st.session_state.data_updated = True

                        st.rerun()
                    else:
                        st.sidebar.error(f"❌ 处理失败")
                        st.sidebar.error(result.stderr)

                except subprocess.TimeoutExpired:
                    st.sidebar.error("❌ 处理超时")
                except Exception as e:
                    st.sidebar.error(f"❌ 发生错误: {str(e)}")

        with col2:
            if st.sidebar.button("🗑️ 清除", key="clear_button", use_container_width=True):
                # 删除临时文件
                if os.path.exists(st.session_state.uploaded_file_path):
                    os.remove(st.session_state.uploaded_file_path)
                st.session_state.uploaded_file_path = None
                st.session_state.show_uploader = False
                st.rerun()

# 应用过滤器
filtered_df = df.copy()

# 价格过滤
filtered_df = filtered_df[
    (filtered_df['input_cost_1M_token'] >= min_input_cost) &
    (filtered_df['input_cost_1M_token'] <= max_input_cost) &
    (filtered_df['output_cost_1M_token'] >= min_output_cost) &
    (filtered_df['output_cost_1M_token'] <= max_output_cost)
]

# 功能过滤
if show_reasoning:
    filtered_df = filtered_df[filtered_df['supports_reasoning'] == True]
if show_vision:
    filtered_df = filtered_df[filtered_df['supports_vision'] == True]

# 免费模型过滤
if show_free_only:
    filtered_df = filtered_df[
        (filtered_df['input_cost_1M_token'] == 0) & 
        (filtered_df['output_cost_1M_token'] == 0)
    ]

# 搜索过滤
if search_term:
    filtered_df = filtered_df[
        filtered_df['model_name'].str.contains(search_term, case=False, na=False)
    ]

# 格式化显示
display_df = filtered_df.copy()

# 格式化布尔值
if 'supports_reasoning' in display_df.columns:
    display_df['supports_reasoning'] = display_df['supports_reasoning'].apply(
        lambda x: '✅' if x else '❌'
    )
if 'supports_vision' in display_df.columns:
    display_df['supports_vision'] = display_df['supports_vision'].apply(
        lambda x: '✅' if x else '❌'
    )

# 重命名列为中文
column_names = {
    'model_name': '模型名称',
    'input_cost_1M_token': '输入成本 ($/1M)',
    'output_cost_1M_token': '输出成本 ($/1M)',
    'max_tokens': '最大上下文',
    'max_output_tokens': '最大输出',
    'supports_reasoning': '推理',
    'supports_vision': '视觉'
}

display_df = display_df.rename(columns=column_names)

# 重置索引，从1开始计数
display_df = display_df.reset_index(drop=True)
display_df.index = display_df.index + 1
display_df.index.name = '#'

# 显示表格 - 占满主内容区域
st.dataframe(
    display_df,
    use_container_width=True,
    height=600
)
