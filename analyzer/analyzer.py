from .entry_point_finder import EntryPointFinder
from .file_scanner import FileScanner
from .dependency_analyzer import DependencyAnalyzer
from .visualizer import Visualizer
import os

class PHPProjectAnalyzer:
    def __init__(self, root_dir: str, exclude_images: bool = True):
        self.root_dir = root_dir
        self.exclude_images = exclude_images
        self.file_scanner = FileScanner(root_dir)
        self.visualizer = Visualizer(root_dir)
        self.edge_list = []

    def analyze_dependencies(self):
        files = self.file_scanner.scan_files()
        print("Files:")
        for file in files:
            print(f"- {file}")
        analyzer = DependencyAnalyzer(files, self.root_dir, self.exclude_images)
        self.edge_list = analyzer.analyze_dependencies()

        print("Dependency Edge List:")
        for edge in self.edge_list:
            print(f"{edge[0]} -> {edge[1]}")        

    def visualize_dependencies(self):
        plantuml_content = self.visualizer.generate_plantuml(self.edge_list, show_path=False)
        mermaid_content = self.visualizer.generate_mermaid(self.edge_list, show_path=False)
        # Save PlantUML content
        with open('dependencies.puml', 'w') as f:
            f.write(plantuml_content)
        print("PlantUML graph saved as 'dependencies.puml'")

        # Save Mermaid content
        with open('dependencies.mmd', 'w') as f:
            f.write(mermaid_content)
        print("Mermaid graph saved as 'dependencies.mmd'")

        print("ASCII Graph:")
        self.visualizer.visualize_ascii_graph(self.edge_list, show_path=False)

        self.visualizer.visualize_networkx_graph(self.edge_list)
        


    # def generate_report(self):
    #     print("PHP Project Analysis Report")
    #     print("==========================")
    #     print(f"\nRoot Directory: {self.root_dir}")
    #     print(f"\nTotal PHP Files: {len(self.php_files)}")
    #     print(f"\nExclude Images: {self.exclude_images}")
        
    #     print("\nEntry Points:")
    #     for entry in self.entry_points:
    #         print(f"- {entry}")
        
    #     print("\nAPI Endpoints:")
    #     for file, endpoints in self.api_endpoints.items():
    #         print(f"\nFile: {file}")
    #         for endpoint in endpoints:
    #             print(f"- {endpoint}")
        
    #     print("\nDependencies:")
    #     for file, deps in self.dependencies.items():
    #         print(f"\nFile: {file}")
    #         for dep in deps:
    #             print(f"- {dep}")