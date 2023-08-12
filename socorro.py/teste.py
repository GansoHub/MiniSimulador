class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.blocks = []

class Directory:
    def __init__(self, name, block):
        self.name = name
        self.files = []
        self.subdirectories = []
        self.block = block

class FileSystemSimulator:
    def __init__(self, memory_size, block_size):
        self.memory_size = memory_size
        self.block_size = block_size
        self.memory = [None] * (memory_size // block_size)
        self.free_blocks = list(range(len(self.memory)))
        self.root_directory = Directory("root", self.allocate_blocks(1)[0])

    def allocate_blocks(self, num_blocks):
        if len(self.free_blocks) < num_blocks:
            print("Not enough contiguous free blocks to allocate.")
            return None

        allocated_blocks = self.free_blocks[:num_blocks]
        self.free_blocks = self.free_blocks[num_blocks:]

        # Display memory usage
        print(f"Allocated blocks: {allocated_blocks}")
        print(f"Free blocks: {self.free_blocks}")
        print(f"Memory usage: {len(allocated_blocks) * self.block_size} bytes / {self.memory_size} bytes")

        if len(allocated_blocks) < num_blocks:
            print(f"Internal fragmentation: {num_blocks - len(allocated_blocks)} blocks")
        else:
            print("No internal fragmentation.")

        return allocated_blocks

    def deallocate_blocks(self, blocks):
        self.free_blocks.extend(blocks)
        self.free_blocks.sort()

        # Display memory usage
        print(f"Deallocated blocks: {blocks}")
        print(f"Free blocks: {self.free_blocks}")
        print(f"Memory usage: {len(self.memory) * self.block_size - len(self.free_blocks) * self.block_size} bytes / {self.memory_size} bytes")

    def create_file(self, directory, name, size):
        # Check if the file name already exists in the current directory's files
        if directory and any(file.name == name for file in directory.files):
            print(f"File '{name}' already exists in directory '{directory.name}'.")
            return
        
        # Check if the file name is the same as any subdirectory name
        if directory and any(subdir.name == name for subdir in directory.subdirectories):
            print(f"File '{name}' cannot have the same name as a subdirectory in directory '{directory.name}'.")
            return
        
        # Check if the file name is the same as the directory name it's being allocated in
        if directory and directory.name == name:
            print("Cannot allocate a file with the same name as the directory.")
            return

        blocks_needed = (size + self.block_size - 1) // self.block_size
        allocated_blocks = self.allocate_blocks(blocks_needed)

        if allocated_blocks is None:
            print("Fragmentation detected! Not enough contiguous blocks to allocate.")
            return

        new_file = File(name, size)
        new_file.blocks = allocated_blocks

        if directory:
            directory.files.append(new_file)
            print(f"File '{name}' created with {size} bytes in directory '{directory.name}'. Allocated blocks: {allocated_blocks}")
        else:
            self.root_directory.files.append(new_file)
            print(f"File '{name}' created as an independent file with {size} bytes. Allocated blocks: {allocated_blocks}")

    def create_directory(self, parent_directory, name):
        # Check if the directory name already exists in the current directory
        if any(subdir.name == name for subdir in parent_directory.subdirectories):
            print(f"Directory '{name}' already exists in current directory.")
            return

        # Check if a file with the same name exists in the parent directory
        if any(file.name == name for file in parent_directory.files):
            print(f"Cannot create a directory '{name}' with the same name as a file in the current directory.")
            return

        block = self.allocate_blocks(1)[0]
        new_directory = Directory(name, block)
        parent_directory.subdirectories.append(new_directory)
        print(f"Directory '{name}' created. Block: {block}")

    def list_contents(self, directory):
        for file in directory.files:
            print(f"- File: {file.name} ({file.size} bytes)")
            print(f"  Blocks: {file.blocks}")
            
        for subdirectory in directory.subdirectories:
            print(f"- Directory: {subdirectory.name} (Block: {subdirectory.block})")
            if subdirectory.files:
                print("  Files:")
                for file in subdirectory.files:
                    print(f"  - File: {file.name} ({file.size} bytes)")
                    print(f"    Blocks: {file.blocks}")

    def delete_file(self, directory, name):
        found_file = None
        for file in directory.files:
            if file.name == name:
                found_file = file
                break

        if found_file is not None:
            self.deallocate_blocks(found_file.blocks)
            directory.files.remove(found_file)
            print(f"File '{name}' deleted.")
        else:
            print(f"File '{name}' not found.")

    def delete_directory(self, parent_directory, name):
        found_directory = None
        for subdirectory in parent_directory.subdirectories:
            if subdirectory.name == name:
                found_directory = subdirectory
                break

        if found_directory is not None:
            self.recursively_deallocate_directory_blocks(found_directory)
            parent_directory.subdirectories.remove(found_directory)
            print(f"Directory '{name}' deleted.")
        else:
            print(f"Directory '{name}' not found.")

    def recursively_deallocate_directory_blocks(self, directory):
        for file in directory.files:
            self.deallocate_blocks(file.blocks)
        for subdirectory in directory.subdirectories:
            self.recursively_deallocate_directory_blocks(subdirectory)

    def get_directory_by_name(self, parent_directory, name):
        for subdirectory in parent_directory.subdirectories:
            if subdirectory.name == name:
                return subdirectory
        return None

if __name__ == "__main__":
    memory_size = 1024  # Example memory size in bytes
    block_size = 64     # Example block size in bytes

    fs_simulator = FileSystemSimulator(memory_size, block_size)
    current_directory = fs_simulator.root_directory

    while True:
        command = input(f"Current directory: {current_directory.name} (Block: {current_directory.block})\n"
                        "Enter a command (create_file, create_directory, list_contents, delete_file, delete_directory, change_directory): ")

        if command == "create_file":
            name = input("Enter file name: ")
            size = int(input("Enter file size: "))
            is_inside_directory = input("Is this file inside a directory? (y/n): ").lower()

            if is_inside_directory == "y":
                directory_name = input("Enter directory name: ")
                directory = fs_simulator.get_directory_by_name(current_directory, directory_name)
                if directory:
                    fs_simulator.create_file(directory, name, size)
                else:
                    print(f"Directory '{directory_name}' not found.")
            else:
                fs_simulator.create_file(None, name, size)
                
        elif command == "create_directory":
            name = input("Enter directory name: ")
            fs_simulator.create_directory(current_directory, name)

        elif command == "list_contents":
            fs_simulator.list_contents(current_directory)

        elif command == "delete_file":
            name = input("Enter file name: ")
            fs_simulator.delete_file(current_directory, name)

        elif command == "delete_directory":
            name = input("Enter directory name: ")
            fs_simulator.delete_directory(current_directory, name)

        elif command == "change_directory":
            name = input("Enter directory name: ")
            new_directory = fs_simulator.get_directory_by_name(current_directory, name)
            if new_directory:
                current_directory = new_directory
                print(f"Changed to directory '{name}'.")
            else:
                print(f"Directory '{name}' not found.")

        else:
            print("Invalid command. Try again.")