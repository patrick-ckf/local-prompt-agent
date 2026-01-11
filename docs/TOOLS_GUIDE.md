# Tools Guide - Function Calling

## 🎯 What are Tools?

**Tools** are functions that the AI can call to perform actions:
- 🧮 **Calculator** - Math operations
- 📄 **File Read** - Read text files
- 🌐 **Web Search** - Search the internet (coming soon)

## 🚀 Built-in Tools

### 1. Calculator Tool

Perform mathematical calculations:

```python
from local_prompt_agent.tools.builtin import CalculatorTool

calc = CalculatorTool()
result = await calc.execute(expression="25 * 4 + 10")
print(result)
# {"success": True, "result": 110}
```

**Supported operations**:
- Addition: `5 + 3`
- Subtraction: `10 - 4`
- Multiplication: `6 * 7`
- Division: `20 / 4`
- Power: `2 ** 8`
- Complex: `(5 + 3) * 2 ** 3`

**Example with Agent**:
```
You: Calculate 15% of 250
Agent: [Uses calculator] The result is 37.5

You: What is 2 to the power of 10?
Agent: [Uses calculator] 2^10 = 1024
```

### 2. File Read Tool

Read contents of text files:

```python
from local_prompt_agent.tools.builtin import FileReadTool

file_tool = FileReadTool(allowed_paths=["."])
result = await file_tool.execute(file_path="config.yaml")
print(result["content"])
```

**Security**:
- Only reads from allowed directories
- Prevents path traversal attacks
- UTF-8 encoding for Chinese files

**Example with Agent**:
```
You: Read the file README.md
Agent: [Reads file] Here are the contents: # Local Prompt Agent...

You: What's in config.yaml?
Agent: [Reads config] The configuration includes...
```

---

## 🔧 Using Tools

### Manual Tool Execution

```python
from local_prompt_agent.tools import ToolRegistry
from local_prompt_agent.tools.builtin import CalculatorTool, FileReadTool

# Create registry
registry = ToolRegistry()

# Register tools
registry.register(CalculatorTool())
registry.register(FileReadTool())

# List tools
print(registry.list())
# ['calculator', 'read_file']

# Execute tool
result = await registry.execute("calculator", expression="10 + 5")
print(result)
# {"success": True, "result": 15}
```

### With Agent (Automatic - Coming Soon)

The agent will automatically use tools when needed:

```
You: Calculate 25% of 400 and tell me if it's more than 100
Agent: [Uses calculator: 25% of 400 = 100]
       The result is exactly 100, so it's not more than 100.
```

---

## 🛠️ Creating Custom Tools

### Simple Tool Example

```python
from local_prompt_agent.tools.base import Tool
from typing import Any, Dict

class GreeterTool(Tool):
    """Simple greeter tool."""
    
    def __init__(self):
        super().__init__(
            name="greeter",
            description="Greet someone by name"
        )
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of person to greet"
                }
            },
            "required": ["name"]
        }
    
    async def execute(self, **kwargs: Any) -> Dict[str, Any]:
        name = kwargs.get("name", "Friend")
        return {
            "success": True,
            "greeting": f"Hello, {name}! 你好！"
        }

# Use it
registry.register(GreeterTool())
result = await registry.execute("greeter", name="Patrick")
# {"success": True, "greeting": "Hello, Patrick! 你好！"}
```

---

## 📋 Tool Schema (OpenAI Format)

Tools use OpenAI's function calling schema:

```json
{
  "type": "function",
  "function": {
    "name": "calculator",
    "description": "Calculate mathematical expressions",
    "parameters": {
      "type": "object",
      "properties": {
        "expression": {
          "type": "string",
          "description": "Mathematical expression"
        }
      },
      "required": ["expression"]
    }
  }
}
```

---

## 🔒 Security

### File Read Tool
- ✅ Restricted to allowed directories
- ✅ Prevents path traversal (`../../../etc/passwd`)
- ✅ Only reads text files
- ✅ UTF-8 encoding safe

### Calculator Tool
- ✅ Safe AST parsing (no eval())
- ✅ Limited operators (+, -, *, /, **)
- ✅ No arbitrary code execution
- ✅ Sandboxed evaluation

---

## 🎯 Coming Soon

### Future Tools
- 🌐 Web search (DuckDuckGo)
- 💾 File write (with safety checks)
- 🐚 Shell command execution (sandboxed)
- 📧 Email sending
- 📅 Calendar operations
- 🎨 Image generation (DALL-E)

---

## 💡 Best Practices

1. **Test tools individually** before using with agent
2. **Set appropriate allowed_paths** for file operations
3. **Handle errors** gracefully
4. **Log tool execution** for debugging
5. **Validate inputs** before execution

---

**Tools make your agent more capable while keeping it safe!** 🛠️
