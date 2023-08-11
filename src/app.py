import chainlit as cl 
from plan_agent import plan_chain, agent

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Hi, I am Kodime, a retrieval agent.\nWhat can I do for you today").send()

@cl.on_message
async def main(message: str):
    # Plan Exeution
    plan_result = await plan_chain.arun(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Agent execution
    res = agent(plan_result)

    # Send Message
    await cl.Message(content=res["output"]).send()
