from agent import agent

response = agent.invoke({
    "messages": [{"role": "user", "content": "Met Dr. Sharma today, discussed OncoBoost Phase III results, she seemed really positive about it, shared the brochure"}]
})

for msg in response["messages"]:
    print(f"{msg.type}: {msg.content}")