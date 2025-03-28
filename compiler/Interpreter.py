import threading
import time
import os
import json
import gc  # Garbage collection for performance optimization

class SandboxedExecutionError(Exception):
    pass

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.events = {}
        self.error_handler = self.default_error_handler
        self.execution_stack = []
        self.event_listeners = {}
        self.sandboxed = True  # Flag to enable sandboxing
        self.state = {}  # Used for stateful computations
        self.cache = {}  # Function result caching for performance optimization

    def default_error_handler(self, error_message):
        print(f"Runtime Error: {error_message}")

    def parse(self, code):
        # Tokenize and parse the code into an Abstract Syntax Tree (AST)
        # For simplicity, let's assume the code is in a basic form and can be parsed directly into a list of operations.
        operations = code.split()  # Just a simplistic tokenizer; use a full parser in a real implementation
        return operations

    def execute(self, code):
        # Main execution loop for parsed code
        operations = self.parse(code)
        for op in operations:
            try:
                if self.sandboxed and 'read_file' in op or 'write_file' in op:
                    raise SandboxedExecutionError("Sandboxing prevents file access.")
                if op == 'print':
                    self.execute_print(operations)
                elif op == 'set':
                    self.execute_set(operations)
                elif op == 'function':
                    self.execute_function(operations)
                elif op == 'if':
                    self.execute_if(operations)
                elif op == 'try':
                    self.execute_try(operations)
                elif op == 'async':
                    self.execute_async(operations)
                elif op == 'await':
                    self.execute_await(operations)
                elif op in self.functions:
                    self.execute_function_call(op, operations)
                else:
                    self.error_handler(f"Unrecognized operation: {op}")
            except Exception as e:
                self.error_handler(f"Error during execution: {str(e)}")

    def execute_print(self, operations):
        value = operations[1]
        print(value)

    def execute_set(self, operations):
        variable_name = operations[1]
        value = self.evaluate_expression(operations[2])
        self.state[variable_name] = value  # Store state here instead of variables directly
        self.variables[variable_name] = value  # Normal assignment for legacy purposes

    def execute_function(self, operations):
        func_name = operations[1]
        params = operations[2].split(',')  # Simple param split
        body = operations[3:]
        self.functions[func_name] = {'params': params, 'body': body}

    def execute_function_call(self, func_name, operations):
        # Check cache first to optimize repeated function calls
        if func_name in self.cache:
            return self.cache[func_name]

        func = self.functions[func_name]
        params = operations[1:]
        if len(params) != len(func['params']):
            self.error_handler(f"Function '{func_name}' called with incorrect number of arguments.")
            return

        local_vars = {param: self.evaluate_expression(val) for param, val in zip(func['params'], params)}
        self.variables.update(local_vars)
        self.execution_stack.append(func_name)

        # Execute function body
        self.execute(' '.join(func['body']))

        # Cache function result to improve performance for repetitive calls
        self.cache[func_name] = self.variables.copy()  # Cache state here

    def execute_if(self, operations):
        condition = operations[1]
        true_block = operations[2]
        false_block = operations[3]

        if self.evaluate_expression(condition):
            self.execute(true_block)
        else:
            self.execute(false_block)

    def execute_try(self, operations):
        try_block = operations[1]
        catch_block = operations[2] if len(operations) > 2 else None
        finally_block = operations[3] if len(operations) > 3 else None

        try:
            self.execute(try_block)
        except Exception as e:
            if catch_block:
                print(f"Caught exception: {str(e)}")
                self.execute(catch_block)
        finally:
            if finally_block:
                self.execute(finally_block)

    def execute_async(self, operations):
        async_function_name = operations[1]
        params = operations[2:]
        threading.Thread(target=self.execute_function_call, args=(async_function_name, params)).start()

    def execute_await(self, operations):
        thread = operations[1]
        thread.join()  # Block until thread completes

    def handle_event(self, event_name, data=None):
        if event_name in self.events:
            for handler in self.events[event_name]:
                handler(data)

    def on(self, event_name, handler):
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(handler)

    def trigger(self, event_name, data=None):
        self.handle_event(event_name, data)

    def add_event_listener(self, event_name, handler):
        self.on(event_name, handler)

    def remove_event_listener(self, event_name, handler):
        if event_name in self.events:
            if handler in self.events[event_name]:
                self.events[event_name].remove(handler)

    # Advanced Expression Support
    def evaluate_expression(self, expression):
        if isinstance(expression, str) and expression.isdigit():
            return int(expression)
        
        # Handle arrays
        if expression.startswith('[') and expression.endswith(']'):
            elements = expression[1:-1].split(',')
            return [self.evaluate_expression(e.strip()) for e in elements]

        # Handle dictionaries
        if expression.startswith('{') and expression.endswith('}'):
            pairs = expression[1:-1].split(',')
            return {pair.split(':')[0].strip(): self.evaluate_expression(pair.split(':')[1].strip()) for pair in pairs}

        # Handle binary operations
        if '+' in expression:
            left, right = expression.split('+')
            return self.evaluate_expression(left) + self.evaluate_expression(right)
        if '-' in expression:
            left, right = expression.split('-')
            return self.evaluate_expression(left) - self.evaluate_expression(right)
        if '*' in expression:
            left, right = expression.split('*')
            return self.evaluate_expression(left) * self.evaluate_expression(right)
        if '/' in expression:
            left, right = expression.split('/')
            return self.evaluate_expression(left) / self.evaluate_expression(right)

    def assert_equal(self, val1, val2):
        if val1 != val2:
            raise Exception(f"Assertion failed: {val1} != {val2}")
        return True

    # File Handling (Reading and Writing files)
    def read_file(self, filename):
        if self.sandboxed:
            raise SandboxedExecutionError("File access is restricted in sandbox mode.")
        try:
            with open(filename, 'r') as file:
                return file.read()
        except Exception as e:
            self.error_handler(f"Error reading file {filename}: {str(e)}")

    def write_file(self, filename, content):
        if self.sandboxed:
            raise SandboxedExecutionError("File access is restricted in sandbox mode.")
        try:
            with open(filename, 'w') as file:
                file.write(content)
        except Exception as e:
            self.error_handler(f"Error writing to file {filename}: {str(e)}")

    # Adding additional built-in functions
    def add_builtin_functions(self):
        self.functions['add'] = {
            'params': ['a', 'b'],
            'body': ['set sum add_result add', 'print sum']
        }

        self.functions['read'] = {
            'params': ['filename'],
            'body': ['set file_content read_file filename', 'print file_content']
        }

        self.functions['write'] = {
            'params': ['filename', 'content'],
            'body': ['write_file filename content']
        }

    # Garbage collection and memory management
    def optimize_memory(self):
        gc.collect()  # Perform garbage collection to optimize memory usage

# Sample code execution flow
interpreter = Interpreter()

# Register some advanced functions
interpreter.add_builtin_functions()

# Add an event listener for 'start' event
interpreter.add_event_listener("start", lambda data: print("Start event triggered"))

# Define a simple asynchronous function
interpreter.execute('function async_print msg print msg')

# Trigger the start event
interpreter.trigger("start", data=None)

# Execute asynchronous function
interpreter.execute('async async_print Hello from async function')

# Execute some code with advanced expressions, arrays, and dictionaries
interpreter.execute('set arr [1, 2, 3, 4, 5]')
interpreter.execute('set dict {key1: value1, key2: value2}')

# Read from file (sandboxed, so it will raise error)
interpreter.execute('read "test.txt"')

# Optimize memory management
interpreter.optimize_memory()

# Perform some stateful computations
interpreter.execute('set x 5')
interpreter.execute('set y 10')
interpreter.execute('set z x + y')

print(interpreter.state)  # Check the computed state
