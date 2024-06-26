import os
import re
from typing import Dict, Set, List, Tuple
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

class Visualizer:
    """
    A class for visualizing dependencies between files in various formats.

    This class provides methods to generate PlantUML, Mermaid, ASCII, and interactive
    network graphs from a list of file dependencies.

    Attributes:
        root_dir (str): The root directory of the project being visualized.
        color_map (dict): A mapping of file extensions to colors for graph visualization.
    """

    def __init__(self, root_dir: str):
        """
        Initialize the Visualizer with the project's root directory.

        Args:
            root_dir (str): The root directory of the project being visualized.
        """
        self.root_dir = root_dir
        self.color_map = {
            '.js': '#F0DB4F',  # JavaScript yellow
            '.html': '#E34C26',  # HTML orange
            '.css': '#264DE4',  # CSS blue
            '.php': '#777BB3',  # PHP purple
        }
        # TODO: テキストファイルなどの依存
        self.out_dir = os.path.join(os.getcwd(), 'out')
        os.makedirs(self.out_dir, exist_ok=True)

    def edge_list_to_dict(self, edge_list: List[Tuple[str, str, str]]) -> Dict[str, Set[str]]:
        """
        Convert a list of edges to a dictionary of dependencies.

        Args:
            edge_list (List[Tuple[str, str, str]]): A list of (source, target, label) tuples.

        Returns:
            Dict[str, Set[str]]: A dictionary where keys are source files and values are sets of target files.
        """
        dependencies = {}
        for edge in edge_list:
            source, target, _ = edge
            if source not in dependencies:
                dependencies[source] = set()
            dependencies[source].add(target)
        return dependencies

    def generate_plantuml(self, edge_list: List[Tuple[str, str, str]], show_path: bool = False) -> str:
        """
        Generate a PlantUML graph representation of the dependencies and save it to a file.

        Args:
            edge_list (List[Tuple[str, str, str]]): A list of (source, target, label) tuples.
            show_path (bool, optional): If True, show full file paths. Defaults to False.

        Returns:
            str: Path to the generated PlantUML file.
        """
        dependencies = self.edge_list_to_dict(edge_list)
        plantuml = "@startuml\n"
        for file, deps in dependencies.items():
            for dep in deps:
                source = file if show_path else os.path.basename(file)
                target = dep if show_path else os.path.basename(dep)
                plantuml += f'"{source}" --> "{target}"\n'
        plantuml += "@enduml\n"
        
        output_path = os.path.join(self.out_dir, 'dependencies.puml')
        with open(output_path, 'w') as f:
            f.write(plantuml)

    def generate_mermaid(self, edge_list: List[Tuple[str, str, str]], show_path: bool = False) -> str:
        """
        Generate a Mermaid graph representation of the dependencies.

        Args:
            edge_list (List[Tuple[str, str, str]]): A list of (source, target, label) tuples.
            show_path (bool, optional): If True, show full file paths. Defaults to False.

        Returns:
            str: A Mermaid graph representation as a string.
        """
        dependencies = self.edge_list_to_dict(edge_list)
        mermaid = "graph TD\n"
        
        for src, targets in dependencies.items():
            src_node = self._format_node(src, show_path)
            for target in targets:
                target_node = self._format_node(target, show_path)
                if show_path:
                    # Find the label for the current edge
                    label = next((label for s, t, label in edge_list if s == src and t == target), "")
                    mermaid += f"{self.get_file_id(src)} -->|{label}| {self.get_file_id(target)}\n"
                else:
                    mermaid += f"{self.get_file_id(src)} --> {self.get_file_id(target)}\n"
                
                # Add node definitions with labels
                mermaid += f"{self.get_file_id(src)}[{src_node}]\n"
                mermaid += f"{self.get_file_id(target)}[{target_node}]\n"

        output_path = os.path.join(self.out_dir, 'dependencies.mmd')
        with open(output_path, 'w') as f:
            f.write(mermaid)

    def get_file_id(self, file_path: str) -> str:
        """
        Generate a unique ID for a file path.

        Args:
            file_path (str): The file path to generate an ID for.

        Returns:
            str: A unique ID string for the file path.
        """
        return re.sub(r'[^a-zA-Z0-9]', '_', os.path.relpath(file_path, self.root_dir))

    def visualize_ascii_graph(self, edge_list: List[Tuple[str, str, str]], show_path: bool = False) -> str:
        """
        Generate and print an ASCII representation of the dependency graph.

        Args:
            edge_list (List[Tuple[str, str, str]]): A list of (source, target, label) tuples.
            show_path (bool, optional): If True, show full file paths. Defaults to False.

        Returns:
            str: An ASCII representation of the graph.
        """
        dependencies = self.edge_list_to_dict(edge_list)
        graph = self._build_ascii_tree(dependencies, show_path)
        print(graph)

    def _build_ascii_tree(self, dependencies: Dict[str, Set[str]], show_path: bool, node: str = None, prefix: str = "", is_last: bool = True, visited: Set[str] = None) -> str:
        """
        Recursively build an ASCII tree representation of the dependencies.

        Args:
            dependencies (Dict[str, Set[str]]): A dictionary of dependencies.
            show_path (bool): If True, show full file paths.
            node (str, optional): The current node being processed. Defaults to None.
            prefix (str, optional): The prefix for the current line. Defaults to "".
            is_last (bool, optional): Whether the current node is the last child. Defaults to True.
            visited (Set[str], optional): A set of visited nodes. Defaults to None.

        Returns:
            str: An ASCII tree representation of the dependencies.
        """
        if visited is None:
            visited = set()

        if node is None:
            # Find root nodes (nodes with no incoming edges)
            all_nodes = set(dependencies.keys()).union(*dependencies.values())
            root_nodes = all_nodes - set().union(*dependencies.values())
            return ''.join(self._build_ascii_tree(dependencies, show_path, root, visited=visited) for root in sorted(root_nodes))

        if node in visited:
            return f"{prefix}{'└── ' if is_last else '├── '}{self._format_node(node, show_path)} (circular reference)\n"

        visited.add(node)
        tree = f"{prefix}{'└── ' if is_last else '├── '}{self._format_node(node, show_path)}\n"

        if node in dependencies:
            children = sorted(dependencies[node])
            for i, child in enumerate(children):
                extension = "    " if is_last else "│   "
                tree += self._build_ascii_tree(dependencies, show_path, child, prefix + extension, i == len(children) - 1, visited)

        visited.remove(node)
        return tree

    def _format_node(self, node: str, show_path: bool) -> str:
        """
        Format a node name based on whether to show the full path or just the filename.

        Args:
            node (str): The node (file path) to format.
            show_path (bool): If True, show the full path; otherwise, show only the filename.

        Returns:
            str: The formatted node name.
        """
        return node if show_path else os.path.basename(node)

    def _get_color_for_extension(self, file_path: str) -> str:
        """
        Get the color for a file based on its extension.

        Args:
            file_path (str): The file path to get the color for.

        Returns:
            str: A hex color code for the file extension.
        """
        _, ext = os.path.splitext(file_path)
        return self.color_map.get(ext.lower(), '#808080')  # Default to gray if extension not found

    def visualize_networkx_graph(self, edge_list: List[Tuple[str, str, str]], show_path: bool = False) -> None:
        """
        Generate and display an interactive network graph using NetworkX and Pyvis.

        Args:
            edge_list (List[Tuple[str, str, str]]): A list of (source, target, label) tuples.
            show_path (bool, optional): If True, show full file paths. Defaults to False.
        """
        dependencies = self.edge_list_to_dict(edge_list)
        G = nx.DiGraph()
        
        all_nodes = set()
        for source, targets in dependencies.items():
            all_nodes.add(self._format_node(source, show_path))
            all_nodes.update(self._format_node(target, show_path) for target in targets)
        
        for node in all_nodes:
            G.add_node(node)
        
        for source, targets in dependencies.items():
            formatted_source = self._format_node(source, show_path)
            for target in targets:
                formatted_target = self._format_node(target, show_path)
                G.add_edge(formatted_source, formatted_target)

        net = Network(notebook=True, directed=True, height="100vh", width="100%")
        net.from_nx(G)

        for node in net.nodes:
            node["color"] = self._get_color_for_extension(node["id"])
            node["size"] = 25
            node["title"] = node["id"]  # ホバー時に表示されるタイトル

        for edge in net.edges:
            edge["arrows"] = "to"
            edge["color"] = "#808080"

        net.set_options("""
        var options = {
            "nodes": {
                "font": {
                    "size": 24
                },
                "shape": "dot"
            },
            "edges": {
                "smooth": {
                    "type": "continuous"
                },
                "font": {
                    "size": 10
                }
            },
            "physics": {
                "barnesHut": {
                    "gravitationalConstant": -10000,
                    "centralGravity": 0.01,
                    "springLength": 95,
                    "springConstant": 0.002,
                    "damping": 0.3,
                    "avoidOverlap": 0.1
                },
                "minVelocity": 0.95
            }
        }
        """)

        output_path = os.path.join(self.out_dir, 'dependencies.html')
        net.show(output_path)
        return output_path