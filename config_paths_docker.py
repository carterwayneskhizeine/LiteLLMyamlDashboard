"""
Docker 环境下的配置路径常量文件，用于定义 LiteLLM 和 Claude Code Router 的配置文件路径。
方便统一管理和修改。
"""

# Docker 容器内的路径
LITELLM_CONFIG_PATH = '/app/real_litellmconfig.yaml'
CLAUDE_CONFIG_PATH = '/app/claude_config.json'