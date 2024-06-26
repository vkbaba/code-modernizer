from .dir_scanner import DirScanner
from .dependency_analyzer import DependencyAnalyzer
from .visualizer import Visualizer
import os

class ProjectModernizer:
    def __init__(self, root_dir: str, exclude_images: bool = True):
        self.root_dir = root_dir
        self.exclude_images = exclude_images
        self.edge_list = []
    
    def find_entry_points(self, files=None):
        self.dir_scanner = DirScanner(self.root_dir)
        return self.dir_scanner.find_entry_points(files)

    def analyze_dependencies(self, entry_points):
        analyzer = DependencyAnalyzer(entry_points, self.root_dir, self.exclude_images)
        self.edge_list = analyzer.analyze_dependencies()

        # print("Dependency Edge List:")
        # for edge in self.edge_list:
        #     print(f"{edge[0]} -> {edge[1]}")        

    def visualize_dependencies(self):
        visualizer = Visualizer(self.root_dir)
        visualizer.generate_plantuml(self.edge_list, show_path=False)
        visualizer.generate_mermaid(self.edge_list, show_path=False)
        # Save PlantUML content
        print("ASCII Graph:")
        visualizer.visualize_ascii_graph(self.edge_list, show_path=False)
        visualizer.visualize_networkx_graph(self.edge_list)
        print("All graphs saved.")
        