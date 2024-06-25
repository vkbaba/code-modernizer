import re

class APIEndpointFinder:
    @staticmethod
    def find_api_endpoints(php_files):
        api_endpoints = {}
        for file_path in php_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                endpoints = re.findall(r'function\s+(\w+)\s*\(', content)
                if endpoints:
                    api_endpoints[file_path] = endpoints
        return api_endpoints