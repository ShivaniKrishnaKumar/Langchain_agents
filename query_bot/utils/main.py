from langchain_groq import ChatGroq
from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel
# from langchain_huggingface import HuggingFaceEndpoint
# from langchain import HuggingFaceHub
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_structured_chat_agent, AgentExecutor
from dotenv import load_dotenv
from utils.prompt2 import medbot_react_message
from utils.tools import python_tool, update_tool, fetch_tool, delete_tool


load_dotenv()
prompt = ChatPromptTemplate.from_messages(medbot_react_message)

memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# llm = HuggingFaceHub(
#     repo_id="meta-llama/CodeLlama-7b-Instruct-hf",
#     huggingfacehub_api_token="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"
# )

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_retries=3,
    api_key="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"
)
tools = [fetch_tool, update_tool, delete_tool, python_tool]

agent = create_structured_chat_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_chain = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

# def run_agent(input_text):

#     response = agent_chain.invoke({"user_message" : input_text})
#     return response["output"]


# Define the FastAPI app
app = FastAPI()

# Define the request model
class AgentRequest(BaseModel):
    user_message: str

# Define the response model
class AgentResponse(BaseModel):
    response: str

# Define the API endpoint
@app.post("/chat", response_model=AgentResponse)
async def chat(request: AgentRequest):
    try:
        response = agent_chain.invoke({"user_message": request.user_message})
        return AgentResponse(response=response["output"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)