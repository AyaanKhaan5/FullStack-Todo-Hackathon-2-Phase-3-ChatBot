"""AI Agent service using OpenAI Agents SDK."""
from openai import OpenAI
from typing import List, Dict, Any, Callable
import os


class AIAgent:
    """AI Agent for natural language task management."""

    def __init__(self, api_key: str, model: str = "xiaomi/mimo-v2-flash:free"):
        """
        Initialize AI Agent with OpenAI client.

        Args:
            api_key: OpenAI API key (or OpenRouter API key)
            model: Model to use (default: xiaomi/mimo-v2-flash:free)
        """
        # Check if using OpenRouter (API key starts with sk-or-v1-)
        if api_key.startswith("sk-or-v1-"):
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            self.client = OpenAI(api_key=api_key)
        self.model = model

    def create_agent(self, tools: List[Callable]) -> Dict[str, Any]:
        """
        Create agent configuration with MCP tools.

        Args:
            tools: List of MCP tool functions

        Returns:
            Agent configuration dictionary
        """
        return {
            "name": "Task Manager",
            "instructions": """You help users manage their todo tasks through natural language.

Your capabilities:
- Create tasks from natural language descriptions
- Extract task titles, descriptions, and due dates from user messages
- Handle various date formats (tomorrow, next week, specific dates)
- Provide friendly, concise responses

Guidelines:
- Always confirm task creation with details
- If a date is ambiguous, use your best judgment
- Keep responses brief and friendly
- Focus on task management only

When creating tasks:
1. Extract the task title (main action)
2. Extract any description or details
3. Extract due date if mentioned
4. Call add_task with the extracted information
5. Confirm the task was created""",
            "tools": tools,
            "model": self.model
        }

    def process_message(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        tools: List[Callable]
    ) -> Dict[str, Any]:
        """
        Process user message and generate response.

        Args:
            message: User's message
            conversation_history: Previous messages in conversation
            tools: Available MCP tools

        Returns:
            Response dictionary with content and tool calls
        """
        # Build messages for OpenAI API
        messages = conversation_history + [
            {"role": "user", "content": message}
        ]

        # Create agent configuration
        agent_config = self.create_agent(tools)

        # For MVP, we'll use a simplified approach without full Swarm
        # Call OpenAI API with tool calling (modern format)
        try:
            # Convert tool functions to OpenAI tool definitions
            tool_definitions = self._tools_to_definitions(tools)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tool_definitions if tool_definitions else None,
                tool_choice="auto" if tool_definitions else None
            )

            assistant_message = response.choices[0].message

            # Check if tool was called
            if assistant_message.tool_calls:
                tool_call = assistant_message.tool_calls[0]
                function_name = tool_call.function.name

                # Parse function arguments safely
                import json
                try:
                    function_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    function_args = eval(tool_call.function.arguments)

                # Execute the function
                tool_function = next(
                    (t for t in tools if t.__name__ == function_name),
                    None
                )

                if tool_function:
                    try:
                        result = tool_function(**function_args)
                        return {
                            "content": f"I've created a task: '{result['title']}'",
                            "function_called": function_name,
                            "function_result": result
                        }
                    except Exception as e:
                        return {
                            "content": f"I encountered an error creating the task: {str(e)}",
                            "error": str(e)
                        }

            return {
                "content": assistant_message.content or "I'm not sure how to help with that.",
                "function_called": None
            }

        except Exception as e:
            raise Exception(f"AI service error: {str(e)}")

    def _tools_to_definitions(self, tools: List[Callable]) -> List[Dict[str, Any]]:
        """
        Convert tool functions to OpenAI tool definitions (modern format).

        Args:
            tools: List of tool functions

        Returns:
            List of tool definitions for OpenAI API
        """
        tool_definitions = []

        for tool in tools:
            if tool.__name__ == "add_task":
                tool_definitions.append({
                    "type": "function",
                    "function": {
                        "name": "add_task",
                        "description": "Create a new task for the user",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "Task title (required)"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Task description (optional)"
                                },
                                "due_date": {
                                    "type": "string",
                                    "description": "Due date in natural language or ISO format (optional)"
                                }
                            },
                            "required": ["title"]
                        }
                    }
                })

        return tool_definitions
