import os
import glob

def summarize_json_files(annotations_dir):
    models_dir = os.path.join(annotations_dir, "models")
    all_stems = set()
    model_stems = {}
    stem_to_parts = {}

    # Find all model folders under all part folders
    part_paths = [d for d in glob.glob(os.path.join(models_dir, "*")) if os.path.isdir(d)]
    for part_path in part_paths:
        part_name = os.path.basename(part_path)
        model_paths = [d for d in glob.glob(os.path.join(part_path, "*")) if os.path.isdir(d)]
        for model_path in model_paths:
            model_name = os.path.basename(model_path)
            if model_name not in model_stems:
                model_stems[model_name] = set()
            for subfolder in ["with_aha_moment", "without_aha_moment"]:
                pattern = os.path.join(model_path, subfolder, "*.json")
                for f in glob.glob(pattern):
                    stem = os.path.splitext(os.path.basename(f))[0]
                    all_stems.add(stem)
                    model_stems[model_name].add(stem)
                    # Track which part each stem is in
                    if stem not in stem_to_parts:
                        stem_to_parts[stem] = set()
                    stem_to_parts[stem].add(part_name)

    for model, stems in model_stems.items():
        missing = all_stems - stems
        if missing:
            print(f"{model} is missing the following json stems:")
            for m in sorted(missing):
                # Show all parts where this stem appears
                parts = ', '.join(sorted(stem_to_parts.get(m, [])))
                print(f"  {parts}/{m}")

if __name__ == "__main__":
    annotations_dir = os.path.join(os.path.dirname(__file__), "annotations")
    summarize_json_files(annotations_dir)
