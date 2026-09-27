import json
import time
from datetime import datetime

class AIAgent:
    def __init__(self, name, role, system_instruction):
        self.name = name
        self.role = role
        self.instruction = system_instruction
        self.memory = []
        print(f"[*] Agent '{self.name}' initialized as {self.role}.")

    def log_to_file(self, data):
        with open("execution_logs.txt", "a", encoding="utf-8") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{timestamp}] {data}\n")

    def process_task(self, task_input):
        print(f"\n[+] Analyzing request: '{task_input}'")
        time.sleep(0.3)
        
        self.memory.append({"role": "user", "content": task_input})
        
        analysis_result = {
            "agent": self.name,
            "role": self.role,
            "task": task_input,
            "decision": "APPROVED_FOR_EXECUTION",
            "memory_depth": len(self.memory)
        }
        
        self.memory.append({"role": "system", "content": analysis_result["decision"]})
        
        json_output = json.dumps(analysis_result, indent=2)
        self.log_to_file(json_output)
        return json_output

if __name__ == "__main__":
    agent = AIAgent(
        name="Nexus-Trader",
        role="Automated Strategy Executor",
        system_instruction="Analyze and execute trade signals with strict risk limits."
    )
    
    tasks = [
        "Check BTC liquidity on Binance",
        "Evaluate ETH/USDT risk-reward ratio",
        "Generate risk report for portfolio"
    ]
    
    for item in tasks:
        output = agent.process_task(item)
        print(output)
        
    print("\n[✓] All logs successfully written to 'execution_logs.txt'")
