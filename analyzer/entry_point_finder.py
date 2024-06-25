import os
import re

# ファイル名から仮のエントリーポイントを見つけるクラス
class EntryPointFinder:
    def __init__(self):
        self.file_dependencies = {}
        self.called_files = set()

    def simple_find_entry_points(self, php_files):
        potential_entry_points = []
        
        for file in php_files:
            filename = os.path.basename(file)
            if self.is_likely_entry_point(filename):
                potential_entry_points.append(file)
        
        # If no potential entry points found, return all PHP files
        return potential_entry_points if potential_entry_points else php_files

    def is_likely_entry_point(self, filename):
        # Check if the filename is in PascalCase
        is_pascal_case = filename[0].isupper() and '_' not in filename

        # Check for specific keywords that suggest it's not an entry point
        lower_filename = filename.lower()
        has_class_keyword = 'class' in lower_filename
        has_api_keyword = 'api' in lower_filename
        has_ajax_keyword = 'ajax' in lower_filename

        # List of common entry point file names
        common_entry_points = [
            'index.php',
            'main.php',
            'app.php',
            'home.php',
            'front.php',
            'public.php',
            'start.php',
            'bootstrap.php'
        ]
        
        # Check if the filename matches any common entry point names
        if filename.lower() in common_entry_points:
            return True
        
        # Check for patterns that might indicate an entry point
        patterns = [
            '^index_',  # Files starting with 'index_'
            '^main_',   # Files starting with 'main_'
            '_controller\.php$',  # Files ending with '_controller.php'
            '^route',   # Files starting with 'route'
        ]
        
        matches_pattern = any(re.search(p, filename.lower()) for p in patterns)

        # A file is likely an entry point if it's not in PascalCase and doesn't contain class, api, or ajax keywords
        return not is_pascal_case and not (has_class_keyword or has_api_keyword or has_ajax_keyword) and matches_pattern