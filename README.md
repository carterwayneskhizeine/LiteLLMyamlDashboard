# AI Models Dashboard

一个基于Streamlit的AI模型信息仪表板，用于查看和筛选AI模型配置信息。

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 功能特性

### 📊 数据展示
- 以表格形式展示AI模型信息
- 支持输入/输出成本、上下文长度、特性支持等
- 自动编号显示（从1开始）

### 🔍 筛选功能
- **价格范围筛选**：按输入/输出成本筛选模型
- **功能筛选**：按是否支持推理(Reasoning)和视觉(Vision)筛选
- **免费模型**：一键显示完全免费的模型
- **关键词搜索**：按模型名称搜索

### 📤 导入配置
- 支持上传 LiteLLM 的自定义 config.yaml 配置文件
- 自动处理并转换为标准格式
- 手动更新仪表板数据

## 安装说明

### 前提条件
- Python 3.7 或更高版本

### 安装依赖

```bash
pip install streamlit pyyaml pandas
```

## 使用方法

### 启动应用

```bash
streamlit run app.py
```

访问显示的URL（通常是 http://localhost:8501）

### 处理YAML文件

手动处理YAML文件：

```bash
# 使用默认文件
python process_yaml.py

# 指定输入和输出文件
python process_yaml.py path_to_you_input.yaml processed_models.yaml
```

### 导入新配置

1. 点击左侧边栏的 **"导入配置"** 按钮
2. 选择YAML配置文件上传
3. 点击 **"⚙️ 开始处理"**
4. 数据将自动更新到仪表板
5. 如需手动刷新，点击 **"🔄 刷新数据"**

## 数据格式

### 输入YAML格式

```yaml
model_list:
  - model_name: "模型名称"
    model_info:
      input_cost_per_token: 0.0001
      output_cost_per_token: 0.0002
      max_tokens: 128000
      max_output_tokens: 4096
      supports_reasoning: true
      supports_vision: false
```

### 输出显示字段

- **模型名称**：模型标识
- **输入成本 ($/1M)**：每100万token的输入价格
- **输出成本 ($/1M)**：每100万token的输出价格
- **最大上下文**：模型支持的最大输入长度
- **最大输出**：模型支持的最大输出长度
- **推理**：是否支持推理功能（✅/❌）
- **视觉**：是否支持视觉功能（✅/❌）

## 文件说明

| 文件 | 说明 |
|------|------|
| `app.py` | Streamlit应用程序主文件 |
| `process_yaml.py` | YAML数据处理脚本 |
| `processed_models.yaml` | 处理后的模型数据文件 |
| `litellmconfig.yaml` | 原始模型配置文件 |
| `CLAUDE.md` | Claude Code开发指南 |

## 界面预览

### 左侧边栏
- 价格范围筛选器
- 功能支持筛选器
- 免费模型开关
- 模型名称搜索框
- 导入配置和刷新数据按钮

### 主界面
- 模型数据表格
- 自动编号（#列）
- 响应式布局

## 示例

![Dashboard Screenshot](./Snipaste.png)

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持模型数据展示和筛选
- 支持YAML配置导入功能
- 添加输出成本筛选选项
