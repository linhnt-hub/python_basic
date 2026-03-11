#!/usr/bin/env python3
"""
Jinja2 to YAML Schema Generator (Enhanced Version)
Tự động tạo YAML schema từ Jinja2 template
"""

import re
import yaml
import argparse
import sys
from typing import Set, Dict, Any, List
from pathlib import Path


class Jinja2SchemaGenerator:
    def __init__(self):
        # Patterns để tìm các biến trong Jinja2
        self.var_pattern = re.compile(r'\{\{[\s]*([a-zA-Z_][a-zA-Z0-9_\.\[\]\'\"]*)[\s]*\}\}')
        self.for_pattern = re.compile(r'\{%[\s]*for[\s]+([a-zA-Z_][a-zA-Z0-9_]*)[\s]+in[\s]+([a-zA-Z_][a-zA-Z0-9_\.\[\]\'\"]*)[\s]*%\}')
        self.if_pattern = re.compile(r'\{%[\s]*(?:if|elif)[\s]+([^%]+)[\s]*%\}')
        
        # Biến cục bộ (loop variables) không cần trong schema
        self.local_vars = set()
        
    def extract_loop_variables(self, template_content: str) -> Set[str]:
        """Trích xuất các biến iterator trong vòng lặp (biến cục bộ)"""
        loop_vars = set()
        for match in self.for_pattern.finditer(template_content):
            loop_var = match.group(1).strip()
            loop_vars.add(loop_var)
        return loop_vars
    
    def extract_variables(self, template_content: str) -> Set[str]:
        """Trích xuất tất cả các biến root từ template"""
        all_variables = set()
        
        # Tìm biến loop trước
        self.local_vars = self.extract_loop_variables(template_content)
        
        # Built-in variables và tests của Jinja2
        builtin_vars = {'loop', 'super', 'self', 'varargs', 'kwargs', 'namespace'}
        builtin_tests = {'defined', 'undefined', 'none', 'boolean', 'false', 'true', 
                        'integer', 'float', 'number', 'string', 'mapping', 'sequence',
                        'iterable', 'callable', 'sameas', 'even', 'odd', 'divisibleby',
                        'escaped', 'lower', 'upper'}
        jinja_keywords = builtin_vars | builtin_tests
        
        # Tìm biến trong {{ }}
        for match in self.var_pattern.finditer(template_content):
            var = match.group(1).strip()
            root_var = var.split('.')[0]
            # Bỏ qua biến cục bộ và built-in
            if root_var not in self.local_vars and root_var not in jinja_keywords:
                all_variables.add(var)
        
        # Tìm biến trong {% for %}
        for match in self.for_pattern.finditer(template_content):
            source_var = match.group(2).strip()
            root_var = source_var.split('.')[0]
            if root_var not in self.local_vars and root_var not in jinja_keywords:
                all_variables.add(source_var)
        
        # Tìm biến trong {% if %} và {% elif %}
        # Cần phải loại bỏ string literals trước khi extract
        for match in self.if_pattern.finditer(template_content):
            condition = match.group(1).strip()
            
            # Loại bỏ string literals (cả ' và ")
            # Replace strings with placeholder để không extract chúng
            condition_no_strings = re.sub(r'[\'"][^\'"]*[\'"]', ' ', condition)
            
            # Tách các biến từ điều kiện
            condition_vars = re.findall(r'([a-zA-Z_][a-zA-Z0-9_\.]*)', condition_no_strings)
            for var in condition_vars:
                root_var = var.split('.')[0]
                # Bỏ qua keywords, biến cục bộ và built-in
                if (var not in ['and', 'or', 'not', 'in', 'is', 'true', 'false', 'none'] 
                    and root_var not in self.local_vars
                    and root_var not in jinja_keywords):
                    all_variables.add(var)
        
        return all_variables
    
    def parse_variable_path(self, var_path: str) -> List[str]:
        """Phân tích đường dẫn biến"""
        var_path = re.sub(r'\[[\'\"]?([^\]\'\"]+)[\'\"]?\]', r'.\1', var_path)
        return var_path.split('.')
    
    def infer_type(self, var_name: str, context: str) -> str:
        """Suy luận kiểu dữ liệu từ context"""
        escaped_var = re.escape(var_name)
        
        # Nếu có 'for ... in', nhiều khả năng là list
        if re.search(r'for\s+\w+\s+in\s+' + escaped_var, context):
            return 'list'
        
        # Nếu có .attribute, nhiều khả năng là dict/object
        if re.search(escaped_var + r'\.\w+', context):
            return 'dict'
        
        return 'string'  # default
    
    def build_nested_structure(self, variables: Set[str], template_content: str) -> Dict[str, Any]:
        """Xây dựng cấu trúc lồng nhau từ danh sách biến"""
        structure = {}
        
        for var in sorted(variables):
            parts = self.parse_variable_path(var)
            current = structure
            
            for i, part in enumerate(parts):
                if i == len(parts) - 1:  # Phần cuối cùng
                    var_type = self.infer_type(var, template_content)
                    
                    if var_type == 'list':
                        # Tìm các thuộc tính của item trong list
                        item_attrs = self._find_list_item_attributes(var, template_content)
                        if item_attrs:
                            # Xây dựng dict structure cho list item
                            item_dict = {}
                            for attr, attr_value in sorted(item_attrs.items()):
                                if isinstance(attr_value, list):
                                    # Nested list with its own structure
                                    item_dict[attr] = attr_value
                                elif '.' in attr:
                                    # Nested attribute như manager.name
                                    attr_parts = attr.split('.')
                                    attr_current = item_dict
                                    for j, attr_part in enumerate(attr_parts):
                                        if j == len(attr_parts) - 1:
                                            attr_current[attr_part] = '<value>'
                                        else:
                                            if attr_part not in attr_current:
                                                attr_current[attr_part] = {}
                                            elif not isinstance(attr_current[attr_part], dict):
                                                # Nếu đã là string, convert thành dict
                                                attr_current[attr_part] = {}
                                            attr_current = attr_current[attr_part]
                                else:
                                    # Simple attribute
                                    if attr not in item_dict or not isinstance(item_dict[attr], (dict, list)):
                                        item_dict[attr] = '<value>'
                            current[part] = [item_dict] if item_dict else ['<item>']
                        else:
                            current[part] = ['<item>']
                    elif var_type == 'dict':
                        if part not in current:
                            current[part] = {}
                    else:
                        current[part] = '<value>'
                else:
                    if part not in current:
                        current[part] = {}
                    elif not isinstance(current[part], dict):
                        current[part] = {}
                    current = current[part]
        
        return structure
    
    def _find_list_item_attributes(self, list_var: str, template_content: str) -> Dict[str, Any]:
        """Tìm các thuộc tính được truy cập từ item trong list"""
        attributes = {}
        
        # Tìm các vòng lặp for với list này
        escaped_var = re.escape(list_var)
        pattern = r'\{%[\s]*for[\s]+(\w+)[\s]+in[\s]+' + escaped_var + r'[\s]*%\}(.*?)\{%[\s]*endfor[\s]*%\}'
        for_matches = re.finditer(pattern, template_content, re.DOTALL)
        
        for match in for_matches:
            item_var = match.group(1)
            loop_body = match.group(2)
            
            # Tìm nested loops (lists inside the item)
            nested_for_pattern = r'\{%[\s]*for[\s]+(\w+)[\s]+in[\s]+' + re.escape(item_var) + r'\.([a-zA-Z_][a-zA-Z0-9_]*)'
            for nested_match in re.finditer(nested_for_pattern, loop_body):
                nested_item_var = nested_match.group(1)
                nested_attr = nested_match.group(2)
                
                # Tìm attributes của nested list item
                nested_attrs = {}
                escaped_nested_item = re.escape(nested_item_var)
                nested_attr_pattern = escaped_nested_item + r'\.([a-zA-Z_][a-zA-Z0-9_]*)'
                for nested_attr_match in re.finditer(nested_attr_pattern, loop_body):
                    nested_attrs[nested_attr_match.group(1)] = '<value>'
                
                if nested_attrs:
                    attributes[nested_attr] = [nested_attrs]
                else:
                    attributes[nested_attr] = ['<item>']
            
            # Tìm tất cả các thuộc tính của item_var
            escaped_item = re.escape(item_var)
            attr_pattern = escaped_item + r'\.([a-zA-Z_][a-zA-Z0-9_\.]*)'
            for attr_match in re.finditer(attr_pattern, loop_body):
                full_attr = attr_match.group(1)
                first_part = full_attr.split('.')[0]
                
                # Bỏ qua nếu đã được đánh dấu là nested list
                if first_part in attributes and isinstance(attributes[first_part], list):
                    continue
                
                # Nếu chưa được đánh dấu, đánh dấu
                if full_attr not in attributes:
                    if '.' in full_attr:
                        attributes[full_attr] = 'dict'
                    else:
                        attributes[full_attr] = 'value'
        
        return attributes
    
    def generate_yaml_schema(self, template_content: str, add_comments: bool = True) -> str:
        """Tạo YAML schema từ template"""
        variables = self.extract_variables(template_content)
        structure = self.build_nested_structure(variables, template_content)
        
        yaml_output = yaml.dump(structure, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        if add_comments:
            yaml_output = "# Auto-generated YAML schema from Jinja2 template\n" + \
                         "# Replace all <value> placeholders with actual data\n\n" + \
                         yaml_output
        
        return yaml_output


def main():
    parser = argparse.ArgumentParser(
        description='Tự động tạo YAML schema từ Jinja2 template',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  # Đọc từ file
  python jinja2_yaml_schema.py template.j2
  
  # Đọc từ stdin
  cat template.j2 | python jinja2_yaml_schema.py
  
  # Xuất ra file
  python jinja2_yaml_schema.py template.j2 -o schema.yaml
        """
    )
    
    parser.add_argument('template_file', nargs='?', 
                       help='Đường dẫn file Jinja2 template (nếu không có sẽ đọc từ stdin)')
    parser.add_argument('-o', '--output', 
                       help='File output để lưu YAML schema')
    parser.add_argument('--no-comments', action='store_true',
                       help='Không thêm comments vào YAML output')
    
    args = parser.parse_args()
    
    # Đọc template
    if args.template_file:
        try:
            template_content = Path(args.template_file).read_text(encoding='utf-8')
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Đọc từ stdin
        template_content = sys.stdin.read()
    
    # Tạo schema
    generator = Jinja2SchemaGenerator()
    yaml_schema = generator.generate_yaml_schema(template_content, add_comments=not args.no_comments)
    
    # Xuất kết quả
    if args.output:
        try:
            Path(args.output).write_text(yaml_schema, encoding='utf-8')
            print(f"✓ YAML schema đã được lưu vào: {args.output}")
        except Exception as e:
            print(f"Lỗi khi ghi file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(yaml_schema, end='')


if __name__ == '__main__':
    main()
