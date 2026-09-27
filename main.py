import json
import time

class AIAgent:
    def __init__(self, name, role, system_instruction):
        self.name = name
        self.role = role
        self.instruction = system_instruction
        self.memory = []
        print(f"[*] Agent '{self.name}' initialized successfully with role: {self.role}")

    def execute_task(self, task_input):
        print(f"\n[+] Processing task: {task_input}")
        print("[*] Thinking, analyzing rules, and preparing response...")
        time.sleep(1)
        
        # ذخیره ورودی در حافظه تعاملی ایجنت
        self.memory.append({"role": "user", "content": task_input})
        
        # خروجی پردازش‌شده
        result = {
            "agent_name": self.name,
            "role": self.role,
            "instruction_applied": self.instruction,
            "status": "COMPLETED",
            "output_data": f"Task '{task_input}' analyzed. Ready for LLM pipeline."
        }
        
        # ذخیره خروجی در حافظه
        self.memory.append({"role": "assistant", "content": result["output_data"]})
        return json.dumps(result, indent=2)

if __name__ == "__main__":
    market_agent = AIAgent(
        name="CryptoSense", 
        role="Quantitative Market Analyst",
        system_instruction="Strict risk management and zero emotional bias."
    )
    
    execution_result = market_agent.execute_task("Analyze BTC/USDT 4H momentum")
    print("\n--- EXECUTION REPORT ---")
    print(execution_result)
    print("\nAgent Memory Count:", len(market_agent.memory), "messages")