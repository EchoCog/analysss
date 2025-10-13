import json
import sys


def analyze_json_structure(file_path):
    """Analyzes the structure of a large JSON file without loading it all into memory."""
    try:
        with open(file_path, "r") as f:
            # Read the first few lines to get a sense of the structure
            print("First 20 lines of the file:")
            for i in range(20):
                line = f.readline()
                if not line:
                    break
                print(line.strip())

        with open(file_path, "r") as f:
            data = json.load(f)
            print("\nTop-level keys:", list(data.keys()))
            if "nodes" in data:
                print("Number of nodes:", len(data["nodes"]))
                if data["nodes"]:
                    # Get the first node to inspect its structure
                    first_node_key = list(data["nodes"].keys())[0]
                    first_node = data["nodes"][first_node_key]
                    print("\nStructure of the first node:")
                    print(json.dumps(first_node, indent=2))
            if "hyperedges" in data:
                print("\nNumber of hyperedges:", len(data["hyperedges"]))
                if data["hyperedges"]:
                    # Get the first hyperedge to inspect its structure
                    first_hyperedge_key = list(data["hyperedges"].keys())[0]
                    first_hyperedge = data["hyperedges"][first_hyperedge_key]
                    print("\nStructure of the first hyperedge:")
                    print(json.dumps(first_hyperedge, indent=2))

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_json_structure(sys.argv[1])
    else:
        print("Please provide the path to the JSON file as an argument.")
