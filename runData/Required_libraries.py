import os
import re
import pkg_resources

def extract_imports_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return set()
    
    imports = set()
    import_pattern = re.compile(r'^\s*(?:import|from)\s+([^\s]+)')
    
    for line in lines:
        match = import_pattern.match(line)
        if match:
            imports.add(match.group(1).split('.')[0])
    
    return imports

def extract_imports_from_directory(directory_path):
    all_imports = set()
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_imports = extract_imports_from_file(file_path)
                all_imports.update(file_imports)
    
    return list(all_imports)

def get_installed_versions(libraries):
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    library_versions = {}
    for lib in libraries:
        version = installed_packages.get(lib.lower())
        if version:
            library_versions[lib] = version
        else:
            library_versions[lib] = 'Not Installed'
    return library_versions

def save_to_file(library_versions, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for lib, version in library_versions.items():
            file.write(f"{lib}=={version}\n")

def main():
    directory_path = ''  # 替換成要的資料夾路徑
    output_file = 'requirements.txt'  # 替換成要的輸出文件名
    libraries = extract_imports_from_directory(directory_path)
    library_versions = get_installed_versions(libraries)
    
    save_to_file(library_versions, output_file)
    print(f"Library versions have been saved to {output_file}")

if __name__ == "__main__":
    main()
