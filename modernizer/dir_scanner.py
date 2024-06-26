import os
import re

class DirScanner:
    """
    A class for scanning directories and finding relevant files while excluding libraries, 
    minimized files, and large files.

    Attributes:
        root_dir (str): The root directory to start scanning from.
        exclude_libraries (bool): Whether to exclude library directories and files.
        exclude_minimized (bool): Whether to exclude minimized files.
        max_file_size (int): Maximum file size in bytes to include in scanning.
        library_indicators (list): List of directory names indicating libraries.
        library_file_prefixes (list): List of file name prefixes indicating library files.
        minimized_patterns (list): List of regex patterns for minimized file names.
    """

    def __init__(self, root_dir: str, exclude_libraries: bool = True, exclude_minimized: bool = True, max_file_size: int = 100 * 1024):
        """
        Initialize the DirScanner with the given parameters.

        Args:
            root_dir (str): The root directory to start scanning from.
            exclude_libraries (bool, optional): Whether to exclude library directories and files. Defaults to True.
            exclude_minimized (bool, optional): Whether to exclude minimized files. Defaults to True.
            max_file_size (int, optional): Maximum file size in bytes to include in scanning. Defaults to 100KB.
        """
        self.root_dir = root_dir
        self.exclude_libraries = exclude_libraries
        self.exclude_minimized = exclude_minimized
        self.max_file_size = max_file_size
        self.library_indicators = [
            'vendor', 'node_modules', 'lib', 'libs', 'library', 'libraries',
            'framework', 'frameworks', 'dist', 'build', 'external', 'third-party'
        ]
        self.library_file_prefixes = ['jquery', 'bootstrap', 'vue', 'react', 'angular', 'lodash', 'moment']
        self.minimized_patterns = [r'\.min\.(js|css)$', r'-min\.(js|css)$', r'\.bundle\.(js|css)$']

    def find_entry_points(self, files=None):
        """
        Find all relevant files in the root directory and its subdirectories.

        Args:
            files (list, optional): Specific files to search for. If None, all relevant files are returned.

        Returns:
            list: A list of file paths that meet the inclusion criteria.

        Raises:
            FileNotFoundError: If any specified files are not found in the root directory,
                               or if no relevant files are found when searching all files.
        """
        entry_points = []

        if files:
            for file in files:
                file_path = self._find_file(file)
                if file_path:
                    entry_points.append(file_path)
                else:
                    raise FileNotFoundError(f"File not found in the root directory: {file}")
        else:
            for root, dirs, files in os.walk(self.root_dir):
                if self.exclude_libraries:
                    dirs[:] = [d for d in dirs if not self._is_library_directory(d)]
                
                for file in files:
                    if file.endswith(('.php', '.js', '.html', '.htm', '.css')):
                        full_path = os.path.join(root, file)
                        if self._should_include_file(full_path):
                            entry_points.append(full_path)

        if not entry_points:
            raise FileNotFoundError("No relevant files found in the project directory.")

        return entry_points

    def _find_file(self, file):
        """
        Find a specific file in the root directory and its subdirectories.

        Args:
            file (str): The file name to search for.

        Returns:
            str: The full path of the file if found, None otherwise.
        """
        for root, _, files in os.walk(self.root_dir):
            if file in files:
                return os.path.join(root, file)
        return None
        
    def _is_library_directory(self, directory: str) -> bool:
        """
        Check if a directory is likely to be a library directory.

        Args:
            directory (str): The name of the directory to check.

        Returns:
            bool: True if the directory is likely a library directory, False otherwise.
        """
        return any(indicator in directory.lower() for indicator in self.library_indicators)

    def _is_library_file(self, file: str) -> bool:
        """
        Check if a file is likely to be a library file.

        Args:
            file (str): The name of the file to check.

        Returns:
            bool: True if the file is likely a library file, False otherwise.
        """
        return any(os.path.basename(file).lower().startswith(prefix) for prefix in self.library_file_prefixes)

    def _is_minimized_file(self, file: str) -> bool:
        """
        Check if a file is likely to be a minimized file.

        Args:
            file (str): The name of the file to check.

        Returns:
            bool: True if the file is likely a minimized file, False otherwise.
        """
        return any(re.search(pattern, os.path.basename(file).lower()) for pattern in self.minimized_patterns)

    def _is_large_file(self, file_path: str) -> bool:
        """
        Check if a file is larger than the maximum allowed size.

        Args:
            file_path (str): The path of the file to check.

        Returns:
            bool: True if the file is larger than the maximum allowed size, False otherwise.
        """
        return os.path.getsize(file_path) > self.max_file_size

    def _should_include_file(self, file_path: str) -> bool:
        """
        Determine if a file should be included in the scan results.

        This method checks if the file should be excluded based on whether it's a library file,
        a minimized file, or a large file.

        Args:
            file_path (str): The path of the file to check.

        Returns:
            bool: True if the file should be included, False otherwise.
        """
        if self.exclude_libraries and self._is_library_file(file_path):
            return False
        if self.exclude_minimized and self._is_minimized_file(file_path):
            return False
        if self._is_large_file(file_path):
            return False
        return True