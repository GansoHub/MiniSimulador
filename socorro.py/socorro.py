# class File:
#     def __init__(self, name, size):
#         self.name = name
#         self.size = size
#         self.blocks = []

# class Directory:
#     def __init__(self, name):
#         self.name = name
#         self.files = []
#         self.subdirectories = []

# class FileSystemSimulator:
#     def __init__(self, memory_size, block_size):
#         self.memory_size = memory_size
#         self.block_size = block_size
#         self.memory = [None] * (memory_size // block_size)
#         self.free_blocks = list(range(len(self.memory)))
#         self.root_directory = Directory("root")

#     def get_directory_by_name(self, parent_directory, name):
#         for subdirectory in parent_directory.subdirectories:
#             if subdirectory.name == name:
#                 return subdirectory
#         return None
    
# if name == "main":
        
#     memory_size = 1024  # Example memory size in bytes
#     block_size = 64     # Example block size in bytes

#     fs_simulator = FileSystemSimulator(memory_size, block_size)
#     current_directory = fs_simulator.root_directory

#     while True:
#         command = input(f"Current directory: {current_directory.name}\n"
#                         "Enter a command (create_file, create_directory, list_contents, delete_file, delete_directory, change_directory): ")

#         if command == "create_file":
#             name = input("Enter file name: ")
#             size = int(input("Enter file size: "))
#             fs_simulator.create_file(current_directory, name, size)
#         elif command == "create_directory":
#             name = input("Enter directory name: ")
#             fs_simulator.create_directory(current_directory, name)
#         elif command == "list_contents":
#             fs_simulator.list_contents(current_directory)
#         elif command == "delete_file":
#             name = input("Enter file name: ")
#             fs_simulator.delete_file(current_directory, name)
#         elif command == "delete_directory":
#             name = input("Enter directory name: ")
#             fs_simulator.delete_directory(current_directory, name)
#         elif command == "change_directory":
#             name = input("Enter directory name: ")
#             new_directory = fs_simulator.get_directory_by_name(current_directory, name)
#             if new_directory:
#                 current_directory = new_directory
#                 print(f"Changed to directory '{name}'.")
#             else:
#                 print(f"Directory '{name}' not found.")
#         else:
#             print("Invalid command. Try again.")

#         def allocate_blocks(self, num_blocks):
#             if len(self.free_blocks) < num_blocks:
#                 print("Not enough contiguous free blocks to allocate.")
#                 return None

#             allocated_blocks = self.free_blocks[:num_blocks]
#             self.free_blocks = self.free_blocks[num_blocks:]

#             return allocated_blocks

#         def deallocate_blocks(self, blocks):
#             self.free_blocks.extend(blocks)
#             self.free_blocks.sort()

#         def create_file(self, directory, name, size):
#             blocks_needed = (size + self.block_size - 1) // self.block_size
#             allocated_blocks = self.allocate_blocks(blocks_needed)

#             if allocated_blocks is None:
#                 print("Fragmentation detected! Not enough contiguous blocks to allocate.")
#                 return

#             new_file = File(name, size)
#             new_file.blocks = allocated_blocks
#             directory.files.append(new_file)
#             print(f"File '{name}' created with {size} bytes. Allocated blocks: {allocated_blocks}")

#         def create_directory(self, parent_directory, name):
#             new_directory = Directory(name)
#             parent_directory.subdirectories.append(new_directory)
#             print(f"Directory '{name}' created.")

#         def list_contents(self, directory):
#             print(f"Contents of '{directory.name}':")
#             for file in directory.files:
#                 print(f"- File: {file.name} ({file.size} bytes)")
#             for subdirectory in directory.subdirectories:
#                 print(f"- Directory: {subdirectory.name}")

#         def delete_file(self, directory, name):
#             found_file = None
#             for file in directory.files:
#                 if file.name == name:
#                     found_file = file
#                     break

#             if found_file is not None:
#                 self.deallocate_blocks(found_file.blocks)
#                 directory.files.remove(found_file)
#                 print(f"File '{name}' deleted.")
#             else:
#                 print(f"File '{name}' not found.")

#         def delete_directory(self, parent_directory, name):
#             found_directory = None
#             for subdirectory in parent_directory.subdirectories:
#                 if subdirectory.name == name:
#                     found_directory = subdirectory
#                     break

#             if found_directory is not None:
#                 self.recursively_deallocate_directory_blocks(found_directory)
#                 parent_directory.subdirectories.remove(found_directory)
#                 print(f"Directory '{name}' deleted.")
#             else:
#                 print(f"Directory '{name}' not found.")

#         def recursively_deallocate_directory_blocks(self, directory):
#             for file in directory.files:
#                 self.deallocate_blocks(file.blocks)
#             for subdirectory in directory.subdirectories:
#                 self.recursively_deallocate_directory_blocks(subdirectory)

# if __name__ == "__main__":
#     memory_size = 1024  # Example memory size in bytes
#     block_size = 64     # Example block size in bytes

#     fs_simulator = FileSystemSimulator(memory_size, block_size)
#     current_directory = fs_simulator.root_directory

#     while True:
#         command = input("Enter a command (create_file, create_directory, list_contents, delete_file, delete_directory): ")

#         if command == "create_file":
#             name = input("Enter file name: ")
#             size = int(input("Enter file size: "))
#             fs_simulator.create_file(current_directory, name, size)
#         elif command == "create_directory":
#             name = input("Enter directory name: ")
#             fs_simulator.create_directory(current_directory, name)
#         elif command == "list_contents":
#             fs_simulator.list_contents(current_directory)
#         elif command == "delete_file":
#             name = input("Enter file name: ")
#             fs_simulator.delete_file(current_directory, name)
#         elif command == "delete_directory":
#             name = input("Enter directory name: ")
#             fs_simulator.delete_directory(current_directory, name)
#         else:
#             print("Invalid command. Try again.")