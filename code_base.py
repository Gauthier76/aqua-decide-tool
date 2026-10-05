from pathlib import Path


def generate_tree(directory, prefix=""):
    """Génère une représentation textuelle de l'arborescence du projet en excluant les dossiers techniques."""
    tree_str = ""
    # Exclusion explicite des dossiers techniques (ajout de node_modules et build pour le JS)
    excluded_dirs = {".idea", ".venv", "venv", "__pycache__", ".git", "newPlot", ".vscode", "node_modules", "build"}

    items = sorted([item for item in directory.iterdir() if
                    item.name not in excluded_dirs and item.name != "tous_les_fichiers.txt"])

    for index, path in enumerate(items):
        connector = "└── " if index == len(items) - 1 else "├── "
        tree_str += f"{prefix}{connector}{path.name}\n"
        if path.is_dir():
            extension = "    " if index == len(items) - 1 else "│   "
            tree_str += generate_tree(path, prefix + extension)
    return tree_str


def main():
    root_dir = Path(__file__).resolve().parent
    output_path = root_dir / "tous_les_fichiers.txt"

    # Ajout de node_modules et build pour éviter d'aspirer les dépendances JS
    excluded_dirs_set = {".idea", ".venv", "venv", "__pycache__", ".git", "newPlot", ".vscode", "node_modules", "build"}

    with output_path.open("w", encoding="utf-8") as outfile:
        # 1. Écrire l'arborescence du projet au début du fichier
        outfile.write("# " + "=" * 50 + "\n")
        outfile.write("# ARBORESCENCE DU PROJET aqua-decide-tool\n")
        outfile.write("# " + "=" * 50 + "\n\n")
        outfile.write(f"{root_dir.name}/\n")
        outfile.write(generate_tree(root_dir))
        outfile.write("\n" + "# " + "=" * 50 + "\n\n")

        # 2. Rechercher récursivement les fichiers par extension
        source_files = []
        extensions = ["*.py", "*.js", "*.jsx"]

        for ext in extensions:
            for p in root_dir.rglob(ext):
                # Ignore si l'un des parents fait partie des dossiers exclus
                if any(ex in p.parts for ex in excluded_dirs_set):
                    continue
                if p.resolve() == output_path.resolve():
                    continue
                source_files.append(p)

        # Trier tous les fichiers trouvés par ordre alphabétique de chemin
        source_files = sorted(source_files)

        for filepath in source_files:
            rel_path = filepath.relative_to(root_dir)
            header = f"\n# {'=' * 50}\n# FILE: {rel_path}\n# {'=' * 50}\n\n"
            outfile.write(header)
            try:
                outfile.write(filepath.read_text(encoding="utf-8"))
            except Exception as e:
                outfile.write(f"# Erreur de lecture du fichier : {e}\n")
            outfile.write("\n")

    print(f"✅ Architecture et codes sources (.py, .js, .jsx) exportés avec succès dans : {output_path}")


if __name__ == "__main__":
    main()