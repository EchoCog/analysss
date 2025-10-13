import json
import os


def optimize_json(file_path, output_dir):
    """Optimizes a large JSON file by splitting it into smaller files."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Split nodes and hyperedges into separate files
        if "nodes" in data:
            with open(os.path.join(output_dir, "nodes.json"), "w") as f:
                json.dump(data["nodes"], f, indent=2)
            del data["nodes"]

        if "hyperedges" in data:
            with open(os.path.join(output_dir, "hyperedges.json"), "w") as f:
                json.dump(data["hyperedges"], f, indent=2)
            del data["hyperedges"]

        # Save the remaining metadata to a separate file
        with open(os.path.join(output_dir, "metadata.json"), "w") as f:
            json.dump(data, f, indent=2)

        print(
            f"Successfully optimized the JSON file and saved the parts in {output_dir}"
        )

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    optimize_json(
        "/home/ubuntu/analysis/case_hypergraph.json",
        "/home/ubuntu/analysis/optimized_hypergraph_data",
    )
