
from langchain.chat_models import ChatOpenAI 
from langchain.memory import ConversationBufferMemory 
from langchain.chains import ConversationChain,LLMChain
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser 
import json 
import os  



def get_prompt(prompt_id) : 
    with open("prompts.json","r") as json_file : 
        prompts = json.load(json_file) 
        return prompts[prompt_id]  

class SoftwareArchitectAgent : 
    def __init__(self) : 
        prompt = get_prompt("software_architecture_prompt")   
        self.system_prompt = SystemMessagePromptTemplate.from_template(prompt) 
        self.llm = ChatOpenAI(model="gpt-4.5-preview") 
        self.memory = ConversationBufferMemory() 
    def build_architecture(self,user_prompt) : 
        human_prompt = HumanMessagePromptTemplate.from_template("{user_input}") 
        print("human_prompt") 
        print(human_prompt) 
        chat_prompt = ChatPromptTemplate.from_messages([self.system_prompt,human_prompt]) 
        llm_chain = LLMChain(llm=self.llm, prompt=chat_prompt)
        llm_response = llm_chain.run({"user_input":user_prompt}) 
        parser = StrOutputParser()
        result = parser.parse(llm_response)
        return result 


software_architecture_ai_agent = SoftwareArchitectAgent()
result = software_architecture_ai_agent.build_architecture("write me a ecommerce website") 
print(result) 

# print("\n\n\n\n *************************")

# result = software_architecture_ai_agent.build_architecture("write me a budget management app") 
# print(result)



       
