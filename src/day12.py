CPY_RGX = "cpy (\d+|a|b|c|d) (\d+|a|b|c|d)"
CPY_RGX = "cpy (\d+|a|b|c|d) (\d+|a|b|c|d)"


class Interpreter:
    def __init__(self, file_object, registers_init_values=(0, 0, 0, 0)):
        self.registers = dict(zip('abcd', registers_init_values))
        self.instruction_pointer = 0
        self.instructions = list(file_object)

    def run(self):
        instructions_count = len(self.instructions)
        while self.instruction_pointer < instructions_count:
            instruction = self.instructions[self.instruction_pointer]
            self.instruction_pointer += 1
            if instruction.startswith('cpy'):
                _, src, dst = instruction.split()
                src = self.to_value(src)
                self.registers[dst] = src
            elif instruction.startswith('inc'):
                _, reg = instruction.split()
                self.registers[reg] += 1
            elif instruction.startswith('dec'):
                _, reg = instruction.split()
                self.registers[reg] -= 1
            elif instruction.startswith('jnz'):
                _, cond, value = instruction.split()
                value = int(value)
                cond = self.to_value(cond)
                if cond:
                    self.instruction_pointer += value - 1  # -1 for previously incremented instruction pointer

    def to_value(self, value):
        try:
            return self.registers[value]
        except KeyError:
            return int(value)

    def __str__(self):
        return "<Interpreter: ({})>".format(" ".join(str(self.registers[k]) for k in "abcd"))

    def exec_instruction(self, instruction):
        pass


with open('../data/day12_test.txt') as f:
    test_interpreter = Interpreter(f)
test_interpreter.run()
print("Test interpreter after run:", test_interpreter)

with open('../data/day12.txt') as f:
    interpreter_step1 = Interpreter(f)
interpreter_step1.run()
print("Step 1 interpreter after run:", interpreter_step1)

with open('../data/day12.txt') as f:
    interpreter_step2 = Interpreter(f, (0, 0, 1, 0))
interpreter_step2.run()
print(interpreter_step2)
