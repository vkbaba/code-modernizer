import os
import re

class FileScanner:
    def __init__(self, root_dir: str, exclude_libraries: bool = True, exclude_minimized: bool = True, max_file_size: int = 100 * 1024):
        self.root_dir = root_dir
        self.exclude_libraries = exclude_libraries
        self.exclude_minimized = exclude_minimized
        self.max_file_size = max_file_size  # デフォルトは1MB
        self.library_indicators = [
            'vendor', 'node_modules', 'lib', 'libs', 'library', 'libraries',
            'framework', 'frameworks', 'dist', 'build', 'external', 'third-party'
        ]
        self.library_file_prefixes = ['jquery', 'bootstrap', 'vue', 'react', 'angular', 'lodash', 'moment']
        self.minimized_patterns = [r'\.min\.(js|css)$', r'-min\.(js|css)$', r'\.bundle\.(js|css)$']

    def scan_files(self):
        target_files = []
        for root, dirs, files in os.walk(self.root_dir):
            if self.exclude_libraries:
                dirs[:] = [d for d in dirs if not self._is_library_directory(d)]
            
            for file in files:
                if file.endswith(('.php', '.js', '.html', '.htm', '.css')):
                    full_path = os.path.join(root, file)
                    if self._should_include_file(full_path):
                        target_files.append(full_path)
        return target_files

    def _is_library_directory(self, directory: str) -> bool:
        return any(indicator in directory.lower() for indicator in self.library_indicators)

    def _is_library_file(self, file: str) -> bool:
        return any(os.path.basename(file).lower().startswith(prefix) for prefix in self.library_file_prefixes)

    def _is_minimized_file(self, file: str) -> bool:
        return any(re.search(pattern, os.path.basename(file).lower()) for pattern in self.minimized_patterns)

    def _is_large_file(self, file_path: str) -> bool:
        return os.path.getsize(file_path) > self.max_file_size

    def _should_include_file(self, file_path: str) -> bool:
        if self.exclude_libraries and self._is_library_file(file_path):
            return False
        if self.exclude_minimized and self._is_minimized_file(file_path):
            return False
        if self._is_large_file(file_path):
            return False
        return True