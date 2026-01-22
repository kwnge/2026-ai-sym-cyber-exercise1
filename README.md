# Automating Exploitation with Agentic Systems - Workshop

**This workshop demonstrates Agentic AI in offensive cybersecurity roles solely for educational use and must not be used against any system without explicit permission.**

## Exercise 1 - Sensitive Data Exfiltration

This repository demonstrates a locally run AI Agent designed to access a virtual machine (VM). The agent includes two primary capabilities:

- **Exploit**: Extracts contents of sensitive files and establishes a backdoor for persistent access.
- **Summary**: Provides a concise overview of the extracted data and the backdoor implementation.

Outputs Exploit and Summary agent results to terminal as well as saving summary report markdown to file in local directory.

## Tools Used

- SSH Tool via Paramiko provided locally
- Local Model Nvidia Nemotron 3 nano
- Pydantic Logfire for observability 

## Purpose

Highlights capabilities of local agents with SSH tooling.

## Installation

**Note Logfire requires an account to use however they have a VERY generous free tier**

1. git clone https://github.com/kwnge/2026-ai-sym-cyber-exercise1.git
2. cd 2026-ai-sym-cyber-exercise1
3. uv sync
4. source .venv/bin/activate
5. logfire auth ## if using logfire 
6. uv run main.py

## Usage

1. Initalize and confirm your local Model is available at address for LOCAL_MODEL definition. 
2. Initialize your SSH_CLIENT with hostname, username, and pw. Its also possible to pass these via dependencies within context window. 
3. Ensure your local VM is running with ssh access available.
4. The Exploit agent will look for sensitive files (e.g., authorized_keys, user credentials, configuration files).
5. Extracted data is packaged and a backdoor is created to maintain simple persistence mechanism via netcat to highlight capability.
6. The Summary agent generates a report summarizing the harvested data and the backdoor details.

## Ethical Considerations

This tool is provided for educational purposes only. It should be used exclusively in controlled lab environments to improve defensive security measures. Unauthorized use on systems without explicit permission is prohibited.

---

*Created for 2026 AI Symposium workshop to highlight agentic capability. Use responsibly.*