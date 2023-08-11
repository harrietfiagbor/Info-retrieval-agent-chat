import chainlit as cl 
from plan_agent import plan_chain, agent

@cl.on_start_chat
async def on_chat_start():
    await cl.Message(content="Hi, I am Kodime retrieval Agent.\nWhat can I do for you today")

@cl.on_message
async def main(message: str):
    # Plan Exeution
    plan_result = plan_chain.run(message)

    # Agent execution
    res = agent(plan_result)

    # Send Message
    cl.Messsage(content=res["output"]).send()
