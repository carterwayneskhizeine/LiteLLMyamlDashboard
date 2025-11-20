"""
Sync models from litellmconfig.yaml to config.json

This script extracts all model names from litellmconfig.yaml's model_list
and updates the models array in config.json for the provider named "lite".
"""

import yaml
import json
import sys
import io
from typing import List, Tuple

import config_paths

# 设置 stdout 为 UTF-8 编码，避免 Windows 下的 GBK 编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def extract_model_names(yaml_file: str) -> Tuple[bool, List[str], str]:
    """
    Extract model names from litellmconfig.yaml
    
    Args:
        yaml_file: Path to the YAML configuration file
        
    Returns:
        Tuple of (success, model_names_list, message)
    """
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if not config or 'model_list' not in config:
            return False, [], "未找到 model_list 配置"
        
        model_names = []
        for model in config['model_list']:
            if 'model_name' in model:
                model_names.append(model['model_name'])
        
        if not model_names:
            return False, [], "model_list 中没有找到任何模型"
        
        return True, model_names, f"成功提取 {len(model_names)} 个模型名称"
    
    except FileNotFoundError:
        return False, [], f"文件未找到: {yaml_file}"
    except yaml.YAMLError as e:
        return False, [], f"YAML 解析错误: {str(e)}"
    except Exception as e:
        return False, [], f"提取模型名称时出错: {str(e)}"


def update_config_json(json_file: str, model_names: List[str]) -> Tuple[bool, str]:
    """
    Update models array in config.json for provider named "lite"
    
    Args:
        json_file: Path to the JSON configuration file
        model_names: List of model names to set
        
    Returns:
        Tuple of (success, message)
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if 'Providers' not in config:
            return False, "config.json 中未找到 Providers 配置"
        
        for provider in config['Providers']:
            if provider.get('name') == 'lite':
                old_count = len(provider.get('models', []))
                provider['models'] = model_names
                
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                
                return True, f"成功更新 lite provider 的模型列表 (原: {old_count} 个, 新: {len(model_names)} 个)"
        
        return False, "未找到名为 'lite' 的 Provider"
    
    except FileNotFoundError:
        return False, f"文件未找到: {json_file}"
    except json.JSONDecodeError as e:
        return False, f"JSON 解析错误: {str(e)}"
    except Exception as e:
        return False, f"更新配置时出错: {str(e)}"


def sync_models(yaml_file: str = config_paths.LITELLM_CONFIG_PATH,
                json_file: str = config_paths.CLAUDE_CONFIG_PATH) -> Tuple[bool, str]:
    """
    Main function to sync models from YAML to JSON
    
    Args:
        yaml_file: Path to litellmconfig.yaml (default: 'litellmconfig.yaml')
        json_file: Path to config.json (default: 'config.json')
        
    Returns:
        Tuple of (success, message)
    """
    print(f"开始同步模型配置...")
    print(f"源文件: {yaml_file}")
    print(f"目标文件: {json_file}")
    print()
    
    # Step 1: Extract model names from YAML
    success, model_names, message = extract_model_names(yaml_file)
    print(f"[提取模型] {message}")
    
    if not success:
        return False, message
    
    print(f"提取到的模型: {len(model_names)} 个")
    for i, name in enumerate(model_names[:5], 1):
        print(f"  {i}. {name}")
    if len(model_names) > 5:
        print(f"  ... 还有 {len(model_names) - 5} 个模型")
    print()
    
    # Step 2: Update config.json
    success, message = update_config_json(json_file, model_names)
    print(f"[更新配置] {message}")
    
    return success, message


if __name__ == '__main__':
    # Get file paths from command line arguments or use defaults
    yaml_file = sys.argv[1] if len(sys.argv) > 1 else config_paths.LITELLM_CONFIG_PATH
    json_file = sys.argv[2] if len(sys.argv) > 2 else config_paths.CLAUDE_CONFIG_PATH
    
    success, message = sync_models(yaml_file, json_file)
    
    if success:
        print("\n[SUCCESS] 模型同步完成!")
        sys.exit(0)
    else:
        print(f"\n[ERROR] 模型同步失败: {message}")
        sys.exit(1)
