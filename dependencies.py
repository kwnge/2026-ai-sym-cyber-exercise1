from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import List, Union

class ExploiterOutput(BaseModel):
    objective_met: bool = Field(description="True or False did you meet objective.")
    commands_used:  Union[List[str], str]= Field(description="Commands used comma delimited to reach goal")
    sensitive_information: Union[List[str]] = Field(description="Sensitive output that has been identified")
    improvement_notes: str = Field(description="How you could of gotten to goal faster.")
    backdoor_shell_info: str = Field(description="How you placed backdoor shell with netcat and how to access.")

@dataclass
class Dependencies:
    target: str = Field(description="Target hostname or IP")
    goal: str = Field(description="Operation goal")
    
    