# Building AI Agents

This masterclass is designed to guide you through building a simple, yet
functional, coding assistant using Pydantic AI. Over the course of the
exercises, you will gain hands-on experience with the core concepts behind
agentic systems, including how to define and structure an agent, write
instructions (prompts), and enable tool-calling capabilities. You will also
explore how execution hooks can be used to customize and control agent behavior.

By the end of this masterclass, you will have a working prototype and a solid
understanding of foundational patterns to develop agentic applications.

## Exercise 1: Your first LLM call

In this first exercise, the goal is to establish a minimal working setup and
make your first call to a language model. You will configure the model provider,
define the model that you will use for your agent, and connect everything
through a Pydantic AI agent.

1. **Configure the model provider:**  
    We will use an OpenAI Responses API via a gateway. This means that you need
    to define a provider that specifies the endpoint of the API (`base_url`) and
    your authentication key (`api_key`).  

    Create an `OpenAIProvider` instance and configure it with the appropriate
    values for your environment.
2. **Configure the model:**  
    Next, define the model using `OpenAIResponsesModel`. This requires the name
    of the model that you want to use (`model_name`) and the provider instance
    that you just created (`provider`).
3. **Create the agent:**  
    Now, create the Agent instance by passing the configured model (`model`) and
    providing instructions (`instructions`).

    The instructions define how the assistant should behave. For this exercise,
    keep it simple (e.g., `"You are a Python coding assistant. Write clear,
    correct, and minimal Python code. ..."`).
4.  **Run the agent:**  
    Create the basic user interaction. Prompt the user for input using
    `console.input(">> ")`. Pass the user input to the agents using the run
    method. Print the output to the console using
    `console.print(result.output)`.


## Exercise 2: Maintaining conversation state

In the previous exercise, you made a single call to the agent. A natural next
step is to wrap this in a loop to create an interactive assistant. However, this
will not work as expected out of the box.

If you repeatedly call the agent with only the last user input, the model has no
memory of the previous interactions. Each call is treated as an isolated
request, which means that the assistant cannot maintain context across turns.

To build a conversational agent, you need to explicitly pass the message history
between calls.

1. **Capture the message history:**  
    After each agent run, you can retrieve the full conversation history using
    `result.all_messages()`. This returns the message history, including both
    user inputs and model responses.
2. **Reuse message history:**  
    When making the next call to the agent, pass this history back using the
    `message_history` argument in the `run()` method.

You now have a stateful agent that can handle multi-turn conversations
coherently.


## Exercise 3: Adding tool calling

So far, our agent can respond to user prompts, but it cannot take actions. In
this exercise, we will give the agent basic file system capabilities through
tools. This allows the agent to read files, write files, search for files, and
delete files.

A tool is a simple Python function that the agent can call. Each tool should
have a clear docstring describing what the tool does, what its parameters mean,
and what its return value represents. This information is exposed to the model
and helps it decide when and how to use the tool correctly.

1. **Implement the four tools:**  
    Implement the `read_file` and `write_file` tools.
2. **Create the file operations capability:**  
    Once the functions are in place, expose them to the agent through a
    capability. Create a `FileOperations` class that inherits from Pydantic AI’s
    `AbstractCapability[Any]` class and override the `get_toolset()` method to
    return a `FunctionToolset` containing your tools (add the functions using
    the `add_function()` method).
3. **Pass the capability to the agent:**
    Finally, pass `[FileOperations()]` as the agent’s `capability` when
    configuring the agent.


## Exercise 4: Adding visibility with hooks

At this point, our agent can act on files, but as a user we get very little
insight into what is happening while it works. Files may appear or change on
disk, yet the console remains quiet until the final response from the agent is
printed. In this exercise, we will improve the user experience by adding logging
to the FileOperations capability.

Pydantic AI processes many internal events while an agent runs, and hooks allow
us to tap into those events.

1. **Configure the agent’s dependencies:**  
    To make it possible for the capability to write to the console, we need to
    inject a console instance. Set the `deps_type` of the agent to `AgentDeps`
    (defined in `deps.py`), create a dependencies object, and pass it in the
    `run()` method.
2. **Implement the hook:**  
    Use the before_tool_execute hook to display a message whenever the agent is about to call a tool.

    ```python
    async def before_tool_execute(
        self,
        ctx: RunContext[Any],
        *,
        call: ToolCallPart,
        tool_def: ToolDefinition,
        args: dict[str, Any],
    ) -> dict[str, Any]: ...
    ```

    You only need to use `call.tool_name` for this exercise, the other
    parameters can be ignored.


## Exercise 5: Controlling reasoning effort

By default, the model uses a medium level of reasoning effort. However, not
every task needs the same amount of work. For simple tasks, we may want to
reduce the reasoning effort to low for faster, cheaper execution. For more
difficult tasks, we may want to increase it to high.

Pydantic AI allows you to control the reasoning effort, and other model-related
parameters, through the `ModelSettings`. In this exercise, you will implement a
capability that dynamically selects the reasoning effort based on the user’s
request.

1. **Create the reasoning effort capability:**  
    Create a `ReasoningEffort` class that inherits from
    `AbstractCapability[Any]`. Inside it, implement the `get_model_settings`
    method. This method should return a `Callable` that accepts
    `RunContext[Any]` and returns the appropriate `ModelSettings` instance.

    Here is the method signature:

    ```python
    def get_model_settings(self) -> Callable[[RunContext[Any]], ModelSettings]:
        def _set_reasoning_effort(
            ctx: RunContext[Any]
        ) -> ModelSettings:
            ...

        return _set_reasoning_effort
    ```
2. **Set the reasoning effort:**  
    Use `ctx.prompt` to inspect the original user instructions passed to the agent via `run()`. Choose between `"low"`, `"medium"`, and `"high"` reasoning effort.

    Use `ModelSettings` and set the `thinking` field accordingly.
3. **Pass the capability to the agent:**  
    Add the `ReasoningEffort()` capability to the list of capabilities in the
    agent constructor.


## Exercise 6: Making the agent extensible with Skills

So far, all of our agent’s behavior has been directly defined in Python. In this
exercise, we will make the agent extensible by allowing users to provide skills.
Skills are Markdown files that the agent can load dynamically at runtime.

In `skills.py`, you will find a partial implementation of a `Skills` capability.
It already contains a `load_skill` tool as well as the `Skills` capability
itself. However, simply exposing the `load_skill` tool is not enough. The agent
also needs to know which skills are available, so that it can decide when to
load and use them.

1. **Extend the system instructions:**  
    Implement the `get_instructions` method on the capability. This method
    should read all Markdown files in the `skills` directory, extract their
    metadata, and return an additional instruction block listing the available
    skills.

    For each skills file, use:

    ```python
    skill = frontmatter.load(filename)
    ```

    The metadata you need is available as `skill.metadata.get("name")` and
    `skill.metadata.get("description")`.
2. **Pass the capability to the agent:**  
    Add the `Skills()` capability to the list of capabilities in the agent
    constructor.
