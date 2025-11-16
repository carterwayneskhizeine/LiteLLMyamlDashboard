import yaml
import argparse
import sys

def process_model_list(yaml_file, output_file):
    """
    处理YAML文件，将模型信息转换为标准格式

    Args:
        yaml_file: 输入的YAML文件路径
        output_file: 输出的YAML文件路径
    """
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        model_list = data.get('model_list', [])
        processed_models = []

        for model in model_list:
            model_name = model.get('model_name', '')
            model_info = model.get('model_info', {})

            # 提取参数
            input_cost = model_info.get('input_cost_per_token', 0.0)
            output_cost = model_info.get('output_cost_per_token', 0.0)
            max_tokens = model_info.get('max_tokens', 0)
            max_output_tokens = model_info.get('max_output_tokens', 0)
            supports_vision = model_info.get('supports_vision', False)
            supports_reasoning = model_info.get('supports_reasoning', False)

            # 转换
            input_cost_1M = round(input_cost * 1000000, 2)
            output_cost_1M = round(output_cost * 1000000, 2)

            # 处理token格式，避免除以0错误
            if max_tokens > 0:
                max_tokens_k = f"{int(max_tokens) // 1000}K"
            else:
                max_tokens_k = "0"

            if max_output_tokens > 0:
                max_output_tokens_k = f"{int(max_output_tokens) // 1000}K"
            else:
                max_output_tokens_k = "0"

            # 构建新model_info
            new_model_info = {
                'input_cost_1M_token': input_cost_1M,
                'output_cost_1M_token': output_cost_1M,
                'max_tokens': max_tokens_k,
                'max_output_tokens': max_output_tokens_k
            }
            if supports_reasoning:
                new_model_info['supports_reasoning'] = True
            if supports_vision:
                new_model_info['supports_vision'] = True

            processed_models.append({
                'model_name': model_name,
                'model_info': new_model_info
            })

        # 写入新YAML文件
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump({'model_list': processed_models}, f, default_flow_style=False, allow_unicode=True)

        return True, f"成功处理 {len(processed_models)} 个模型"

    except FileNotFoundError:
        return False, f"错误：找不到文件 {yaml_file}"
    except yaml.YAMLError as e:
        return False, f"错误：YAML格式错误 - {str(e)}"
    except Exception as e:
        return False, f"错误：{str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='处理AI模型配置YAML文件')
    parser.add_argument('input', nargs='?', default='litellmconfig.yaml', help='输入的YAML文件路径 (默认: litellmconfig.yaml)')
    parser.add_argument('output', nargs='?', default='processed_models.yaml', help='输出的YAML文件路径 (默认: processed_models.yaml)')

    args = parser.parse_args()

    success, message = process_model_list(args.input, args.output)
    print(message)

    if not success:
        sys.exit(1)