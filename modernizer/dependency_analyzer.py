import os
import re
from typing import List, Tuple

class DependencyAnalyzer:
    """
    A class for analyzing dependencies between files in a project.

    This class scans through files and extracts dependencies based on various patterns
    for different file types (PHP, JavaScript, HTML, CSS).

    Attributes:
        files (List[str]): List of files to analyze.
        root_dir (str): Root directory of the project.
        exclude_images (bool): Whether to exclude image files from analysis.
        handle_dynamic (bool): Whether to handle dynamic dependencies.
        analyzed_files (set): Set of files that have been analyzed.
    """

    def __init__(self, files: List[str], root_dir: str, exclude_images: bool = True, handle_dynamic: bool = True):
        """
        Initialize the DependencyAnalyzer.

        Args:
            files (List[str]): List of files to analyze.
            root_dir (str): Root directory of the project.
            exclude_images (bool, optional): Whether to exclude image files. Defaults to True.
            handle_dynamic (bool, optional): Whether to handle dynamic dependencies. Defaults to True.
        """
        self.files = files
        self.root_dir = root_dir
        self.exclude_images = exclude_images
        self.handle_dynamic = handle_dynamic
        self.analyzed_files = set()

    def analyze_dependencies(self) -> List[Tuple[str, str, str]]:
        """
        Analyze dependencies for all files.

        Returns:
            List[Tuple[str, str, str]]: List of edges representing dependencies.
            Each edge is a tuple (source_file, target_file, root_dir).
        """
        edge_list = []
        for file in self.files:
            self._analyze_file(file, edge_list)
        return edge_list

    def _analyze_file(self, file: str, edge_list: List[Tuple[str, str, str]]):
        """
        Analyze dependencies for a single file.

        Args:
            file (str): Path to the file to analyze.
            edge_list (List[Tuple[str, str, str]]): List to append found dependencies.
        """
        if file in self.analyzed_files:
            return
        self.analyzed_files.add(file)
        dependencies = self.extract_dependencies(file)
        for dep in dependencies:
            if self.is_dynamic(dep):
                if self.handle_dynamic:
                    print(f"Dynamic dependency detected and skipped: {dep}")
                    continue
                else:
                    print(f"Dynamic dependency detected: {dep}")
            
            if os.path.isabs(dep):
                full_dep_path = os.path.normpath(dep)
            else:
                full_dep_path = os.path.normpath(os.path.join(self.root_dir, dep))
            full_dep_path = os.path.normpath(full_dep_path)

            if not (self.exclude_images and self.is_image_file(full_dep_path)):
                rel_file = os.path.relpath(file, self.root_dir)
                rel_dep_path = os.path.relpath(full_dep_path, self.root_dir)
                rel_file = rel_file.replace(os.path.sep, '/')
                rel_dep_path = rel_dep_path.replace(os.path.sep, '/')
                full_file_path = os.path.join(self.root_dir, rel_file).replace(os.path.sep, '/')
                full_dep_path = os.path.join(self.root_dir, rel_dep_path).replace(os.path.sep, '/')
                edge_list.append((full_file_path, full_dep_path, self.root_dir))
                if full_dep_path in self.files:
                    self._analyze_file(full_dep_path, edge_list)

    def is_dynamic(self, path: str) -> bool:
        """
        Check if a dependency path contains dynamic elements.

        Args:
            path (str): The dependency path to check.

        Returns:
            bool: True if the path contains dynamic elements, False otherwise.
        """
        dynamic_indicators = ['${', '}', '+', '<?php', '?>']
        return any(indicator in path for indicator in dynamic_indicators) or re.search(r'\$[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*', path)

    def extract_dependencies(self, file_path: str) -> List[str]:
        """
        Extract dependencies from a file.

        Args:
            file_path (str): Path to the file to extract dependencies from.

        Returns:
            List[str]: List of extracted dependencies.
        """
        dependencies = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if file_path.endswith('.php'):
                    dependencies.extend(self._extract_dependencies(content, self.php_patterns))
                elif file_path.endswith('.js'):
                    dependencies.extend(self._extract_dependencies(content, self.js_patterns))
                elif file_path.endswith('.html') or file_path.endswith('.htm'):
                    dependencies.extend(self._extract_dependencies(content, self.html_patterns))
                elif file_path.endswith('.css'):
                    dependencies.extend(self._extract_dependencies(content, self.css_patterns))
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
        return [dep for dep in dependencies if not self.is_dynamic(dep)]

    def _extract_dependencies(self, content: str, patterns: List[str]) -> List[str]:
        """
        Extract dependencies from content using specified patterns.

        Args:
            content (str): The content to extract dependencies from.
            patterns (List[str]): List of regex patterns to use for extraction.

        Returns:
            List[str]: List of extracted dependencies.
        """
        dependencies = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    dep = match[0]
                else:
                    dep = match
                if not self._is_external_dependency(dep):
                    dependencies.append(dep)
        return dependencies

    def _is_external_dependency(self, path: str) -> bool:
        """
        Check if a dependency path is external (e.g., a URL).

        Args:
            path (str): The dependency path to check.

        Returns:
            bool: True if the path is an external dependency, False otherwise.
        """
        external_patterns = [
            r'^https?://',
            r'^//',
            r'^www\.',
            r'^\w+://',
        ]
        return any(re.match(pattern, path, re.IGNORECASE) for pattern in external_patterns)

    # Regex patterns for different file types
    php_patterns = [
        r'(?:include|require)(?:_once)?\s*[\'"]([^\'"]+)[\'"]',
        r'use\s+([^;]+)',
        r'<script[^>]*src=[\'"]([^\'"]+)[\'"]',
        r'echo\s*[\'"]<script[^>]*src=[\'"]([^\'"]+)[\'"]',
        r'<link[^>]*href=[\'"]([^\'"]+\.css)[\'"]',
        r'<img[^>]*src=[\'"]([^\'"]+)[\'"]'
    ]

    js_patterns = [
        r'(?:import|export)(?:.*?from)?\s+[\'"]([^\'"]+)[\'"]',
        r'(?:const|let|var)?\s*.*?require\s*\(\s*[\'"]([^\'"]+)[\'"]',
        r'import\s*\(\s*[\'"]([^\'"]+)[\'"]',
        r'fetch\s*\(\s*[\'"]([^\'"]+)[\'"]',
        r'\$\.ajax\s*\(\s*\{[^}]*url\s*:\s*[\'"]([^\'"]+)[\'"]',
        r'\.open\s*\(\s*[\'"](?:GET|POST|PUT|DELETE)[\'"],\s*[\'"]([^\'"]+)[\'"]'
    ]

    html_patterns = [
        r'<script[^>]*src=[\'"]([^\'"]+)[\'"]',
        r'<link[^>]*href=[\'"]([^\'"]+\.css)[\'"]',
        r'<img[^>]*src=[\'"]([^\'"]+)[\'"]'
    ]

    css_patterns = [
        r'@import\s+[\'"]([^\'"]+)[\'"]',
        r'url\s*\(\s*[\'"]?([^\'"]+)[\'"]?\s*\)'
    ]

    @staticmethod
    def is_image_file(file_path: str) -> bool:
        """
        Check if a file is an image based on its extension.

        Args:
            file_path (str): The file path to check.

        Returns:
            bool: True if the file is an image, False otherwise.
        """
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']
        return any(file_path.lower().endswith(ext) for ext in image_extensions)