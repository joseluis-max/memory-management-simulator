# Emulation memory management for a simple CPU emulator.
class Program: 
    instructions = None
    size = 32

    def __init__(self, size=32):
        """Initialize program memory with a given size."""
        self.size = size
        self.instructions = bytearray(size)

    def add_instruction(self, instruction):
        """Add an instruction to the program memory at the specified address."""
        for i in range(self.size):
            if self.instructions[i] == 0:
                self.instructions[i] = instruction
                print(f"Added instruction {instruction} at address {i}.")
                return i
        raise MemoryError("Program memory is full.")

class Loader:

    def load(self, program):
        raise NotImplementedError("Load program method not implemented.")

class StaticLoader(Loader):

    def load(self, program, memory):
        """Load a program into memory at the first available address."""
        for _byte in memory:
            if _byte == 0:
                memory[:len(program.instructions)] = program.instructions
                print("Program loaded into memory.")
                return
        raise MemoryError("Memory is full, cannot load program.")

class DynamicLoader(Loader):

    def load(self, program, memory):
        """Load a program into memory at the first available address."""
        for i in range(len(memory)):
            if memory[i] == 0:
                memory[i:i + len(program.instructions)] = program.instructions
                print("Program loaded into memory.")
                return
        raise MemoryError("Memory is full, cannot load program.") 

class Memory:
    memory = None
    partitions = []
    size: int

    def __init__(self, size=512):
        """Initialize memory with a given size."""
        self.size = size
        self.memory = bytearray(size)

    def reset(self):
        """Reset memory to zero."""
        self.memory = bytearray(self.size)
        print("Memory reset to zero.")

    def add(self, program, loader):
        """Add a program to memory using the specified loader."""
        loader.load(program, self.memory)

    def read(self, address):
        """Read a byte from memory at the specified address."""
        if 0 <= address < self.size:
            value = self.memory[address]
            print(f"Read {value} from address {address}.")
            return value
        else:
            raise IndexError("Address out of bounds.")

    def write(self, address, value):
        """Write a byte to memory at the specified address."""
        if 0 <= address < self.size:
            if 0 <= value < 256:  # Ensure value is a byte
                self.memory[address] = value
                print(f"Wrote {value} to address {address}.")
            else:
                raise ValueError("Value must be a byte (0-255).")
        else:
            raise IndexError("Address out of bounds.")

    def inspect(self):
        """Inspect the current state of memory with colored output for partitions."""
        # ANSI color codes
        PARTITION_COLOR = "\033[94m"  # Blue
        RESET = "\033[0m" 
        ADDRESS_COLOR = "\033[94m"  # Green
        print("Current memory state:")
        
        # Print header
        print(f"{ADDRESS_COLOR}    :{RESET}", end=' ')
        for i in range(16):
            print(f"{ADDRESS_COLOR}{i + 1:02x}{RESET}", end=' ')
        print()
        for i in range(0, self.size, 16):
            line = f"{ADDRESS_COLOR}{i:04x}:{RESET} " + ' '.join(f"{self.memory[j]:02x}" for j in range(i, min(i + 16, self.size)))
            # Check if this line is the start or end of a partition
            for part in self.partitions:
                if part['start'] == i:
                    print(f"{PARTITION_COLOR}Partition start: {part['start']:04x}:{RESET}")
                if part['end'] == i:
                    print(f"{PARTITION_COLOR}Partition end {part['end']:04x}:{RESET}")
            print(line)

    def partition(self, start, end):
        """Partition memory into a subrange."""
        if 0 <= start < end <= self.size:
            self.partitions.append({
                'start': start,
                'end': end,
                'data': self.memory[start:end]
            })
            print(f"Partitioned memory from {start} to {end}.")
        else:
            raise IndexError("Partition range out of bounds.")

class Pagination:
    memory: None
    size: int
    def __init__(self, memory, size=128):
        """Initialize pagination with a given page size."""
        self.size = size
        self.memory = memory
        self.page_size = memory.size // size
        self.pages = {
            i: None for i in range(self.page_size)
        }
        for i in range(0, memory.size, size):
            self.memory.partition(i, min(i + self.page_size, memory.size))

    def inspect(self):
        # ANSI color codes
        PARTITION_COLOR = "\033[94m"  # Blue
        RESET = "\033[0m" 
        ADDRESS_COLOR = "\033[94m"  # Green
        print("Current memory state:")
        
        # Print header
        print(f"{ADDRESS_COLOR}    :{RESET}", end=' ')
        for i in range(16):
            print(f"{ADDRESS_COLOR}{i + 1:02x}{RESET}", end=' ')
        print()
        for i in range(0, self.memory.size, 16):
            line = f"{ADDRESS_COLOR}{i:04x}:{RESET} " + ' '.join(f"{self.memory.memory[j]:02x}" for j in range(i, min(i + 16, self.memory.size)))
            # Check if this line is the start or end of a partition
            for part in self.memory.partitions:
                if part['start'] == i:
                    print(f"{PARTITION_COLOR}Partition start: {part['start']:04x}:{RESET}")
                if part['end'] == i:
                    print(f"{PARTITION_COLOR}Partition end {part['end']:04x}:{RESET}")
            print(line)

if __name__ == "__main__":
    p1 = Program(size=16)
    p1.add_instruction(0x01)
    p1.add_instruction(0x02)
    p1.add_instruction(0x03)
    p1.add_instruction(0x04)
    p1.add_instruction(0x05)
    p1.add_instruction(0x06)
    p1.add_instruction(0x07)
    p1.add_instruction(0x08)
    p1.add_instruction(0x09)
    p1.add_instruction(0x0A)
    p1.add_instruction(0x0B)
    p1.add_instruction(0x0C)
    p1.add_instruction(0x0D)
    p1.add_instruction(0x0E)
    p1.add_instruction(0x0F)
    p1.add_instruction(0x10)

    mem = Memory()
    pg = Pagination(mem, size=64)

    pg.inspect()

    loader = StaticLoader()
    mem.add(p1, loader)

    # mem.inspect()
