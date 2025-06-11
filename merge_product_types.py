import json
import re
import sys

def parse_php_array(php_content):
    product_map = {}
    # Regex to find lines like 'Identifier' => 'Product Name',
    # It handles single quotes and potential escaping within names, though simple for now.
    # It expects the array definition to be somewhat consistent.
    array_content_match = re.search(r'\$productNames\s*=\s*array\s*\((.*?)\);\s*\?>', php_content, re.DOTALL | re.IGNORECASE)
    if not array_content_match:
        # Fallback if the closing ?> is not on the same line or structure is different
        array_content_match = re.search(r'\$productNames\s*=\s*array\s*\((.*?)\);\s*', php_content, re.DOTALL | re.IGNORECASE)
        if not array_content_match:
             array_content_match = re.search(r'\$productNames\s*=\s*array\s*\((.*)\)\s*;', php_content, re.DOTALL | re.IGNORECASE)


    if array_content_match:
        array_str = array_content_match.group(1)
        # Regex for individual entries: captures 'key' => 'value'
        # Handles optional trailing comma and varying whitespace.
        entry_regex = r"['\"]([^'\"]+)['\"]\s*=>\s*['\"]([^'\"]+)['\"](?:,\s*)?"
        for match in re.finditer(entry_regex, array_str):
            identifier = match.group(1)
            name = match.group(2)
            product_map[identifier] = name
    return product_map

def main():
    if len(sys.argv) != 3:
        print("Usage: python merge_product_types.py \"<php_file_content_string>\" \"<json_data_string>\"", file=sys.stderr)
        sys.exit(1)

    php_file_content_str = sys.argv[1]
    json_data_str = sys.argv[2]

    existing_devices = parse_php_array(php_file_content_str)
    new_devices = json.loads(json_data_str)

    # Merge: Add new devices, keep existing ones if conflicts occur
    for identifier, name in new_devices.items():
        if identifier not in existing_devices:
            existing_devices[identifier] = name

    # Reconstruct the PHP file content
    # Start with the beginning of the PHP file, up to the array definition
    php_header = php_file_content_str.split('$productNames', 1)[0]

    new_php_array_content = "$productNames = array(\n"
    sorted_keys = sorted(existing_devices.keys()) # Sort for consistent output

    for key in sorted_keys:
        # Ensure proper escaping for PHP strings (though simple names might not need much)
        php_key = key.replace("'", "\\'")
        php_value = existing_devices[key].replace("'", "\\'")
        new_php_array_content += f"\t'{php_key}' => '{php_value}',\n"

    new_php_array_content += ");\n?>" # Assuming the original file ends this way or similarly

    # If the original PHP file had content after the array, it should be appended.
    # For this specific file, it seems to end with the array and ?>
    # A more robust way would be to find the end of the array declaration.

    # A simpler reconstruction just replaces the array part
    # This assumes the array is the last significant part before ?> or end of file.

    # Let's try a more direct reconstruction based on typical format
    output_lines = []
    output_lines.append("<?php")
    output_lines.append("$productNames = array(")
    for key in sorted_keys:
        php_key = key.replace("'", "\\'") # Basic escaping
        php_value = existing_devices[key].replace("'", "\\'")
        output_lines.append(f"\t'{php_key}' => '{php_value}',")
    output_lines.append(");")
    output_lines.append("?>")

    print("\n".join(output_lines))

if __name__ == '__main__':
    main()
