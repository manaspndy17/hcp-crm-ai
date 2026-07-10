import sys
import os
import threading
import time
import traceback
from dotenv import load_dotenv

load_dotenv()

def dump_stacks():
    time.sleep(5)
    print("\n⏰ --- TIME OUT DIAGNOSTIC DUMP ---")
    for thread_id, stack in sys._current_frames().items():
        print(f"\n🧵 Thread ID: {thread_id}")
        for filename, lineno, name, line in traceback.extract_stack(stack):
            print(f"  File: {filename}, line {lineno}, in {name}")
            if line:
                print(f"    Code: {line}")
    print("\n⚠️ If you see 'socket.py' or 'pymysql' above, the DB connection is hanging.")
    print("⚠️ If you see 'groq' or 'httpcore' above, the AI API key/network call is hanging.")
    os._exit(1) # Force quit the process so it doesn't stay frozen

# Start the watchdog thread
threading.Thread(target=dump_stacks, daemon=True).start()

print("🚀 Simulating your agent flow...")
try:
    # 1. Test Database Connectivity
    from database import engine
    with engine.connect() as conn:
        print("🟢 DB Engine initialized...")
    
    # 2. Test Agent Initialization
    from agent import agent
    print("🟢 Agent built successfully. Invoking LLM...")
    
    # 3. Test Agent Execution
    response = agent.invoke({"messages": [{"role": "user", "content": "Met Dr. Rao"}]})
    print("✅ Success! Agent output:", response)

except Exception as e:
    print("❌ Failed with exception:", e)