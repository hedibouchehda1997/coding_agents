
from langchain.chat_models import ChatOpenAI 
from langchain.memory import ConversationBufferMemory ,ConversationBufferWindowMemory
from langchain.chains import ConversationChain,LLMChain
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, PromptTemplate 
from langchain_core.output_parsers import StrOutputParser 
from langchain_core.pydantic_v1 import BaseModel, Field
import json 
import os  
import re


software_architect_prompt = """
you are a software architect specialized in building web application. 
you are provided with the following requirement document : {product_document}. 
For All frontend code, you are supposed to use html5, bootstrap css and javascript
For All the backend code you need to use FastAPI and python 
you're mission is to analyse it step by step from a software architect perspective and to provide a technical document that is going 
to be the reference for technical stakeholders. You need to analyse the product document step by step and then create the technical document. 

The output format : 
<think> 
    ***this section will contain the process of analysis of the product document 
</think>
<result> 
1- App Overview : 
    1-1. App Idea : 
    1-2. Purpose : 
    1-3. Target audience : 
    1-4. key features : 

2- UI/UX Component Beakdown 
    *** this section should contain all the UX/UI component that should be built to have a complete working application 
3- File and Foldder structure 
    *** this section should contain the folder and the files that need to be created to build the application 
</result> 

"""

def get_prompt(prompt_id) : 
    with open("prompts.json","r") as json_file : 
        prompts = json.load(json_file) 
        return prompts[prompt_id] 

def extract_result(text) : 
    start = text.find("<result>") + len("<result>")
    end = text.find("</result>")
    
    if start - len("<result>") != -1 and end != -1:
        return text[start:end]
    return None
 
class SoftwareArchitectAgent : 
    def __init__(self) : 
        prompt = get_prompt("software_architecture_prompt")   
        self.system_prompt = SystemMessagePromptTemplate.from_template(prompt) 
        self.llm = ChatOpenAI(model="gpt-3.5-turbo") 
        self.memory = ConversationBufferMemory() 
        self.parser = StrOutputParser() 
    def build_architecture_v2(self,user_prompt) : 
        prompt_template = "you are a product owner specialized on understanding the business requirement and the design of web application. \n Your mission is to take an app idea and create a detailed document that contains the software requirements to build this app.\n the app idea : {user_input}"
        prompt = PromptTemplate(
            input_variable = ["user_input"] , 
            template = prompt_template
        )
        llm_chain = LLMChain(llm=self.llm,prompt=prompt) 
        llm_response = llm_chain.run({"user_input":user_prompt}) 
        result = self.parser.parse(llm_response) 

        
        prompt = PromptTemplate(
            input_variable = ["product_document"] ,
            template = software_architect_prompt
        )
        llm_chain = LLMChain(llm=self.llm,prompt=prompt)
        result_architecture = llm_chain.run({"product_document" : result})
        print(result_architecture) 


    
    #this method will create a technical document given the user general idea of an app
    def build_architecture(self,user_prompt) : 
        human_prompt = HumanMessagePromptTemplate.from_template("{user_input}") 
        print("human_prompt") 
        print(human_prompt) 
        chat_prompt = ChatPromptTemplate.from_messages([self.system_prompt,human_prompt]) 
        llm_chain = LLMChain(llm=self.llm, prompt=chat_prompt)
        llm_response = llm_chain.run({"user_input":user_prompt}) 
        result = self.parser.parse(llm_response)
        result = extract_result(result)
        return result 
    #this method will create a chat based on the created the technical document.
    #whether to ask for details about sepecific parts or to edit some parts of it 
    def build_architecture_chat(self,architecture_document) : 
        prompt_template = "You are a software architect expert, you are provided with the following document : {document}\nThis document contains some technical details about the architecture of an application that the user is trying to build. \nYour mission is to respond to user questions and requests regarding the document\nconversation History : {history}\nUser request or question : {request}"
        prompt = PromptTemplate(
            input_variables = ["request","history"] ,
            template = prompt_template 
        ).partial(document=architecture_document)

        print("prompt")
        print(prompt)

        conversation_chain = LLMChain(llm=self.llm, prompt=prompt,memory=self.memory) 

        print("\n\n") 
        print("**** start the chat ******")

        while True : 
            user_input = input("user: ") 
            if user_input.lower() in ["quit","exit","q"] : 
                print("goodbye") 
                break 
            llm_response = conversation_chain.run(user_input) 
            result = self.parser.parse(llm_response) 
            print("AI :")
            print(result) 




# result = get_prompt("software_architecture_prompt")  
# print(result)

software_architecture_ai_agent = SoftwareArchitectAgent()
software_architecture_ai_agent.build_architecture_v2("write me a ecommerce website for dropshipping for pets products")
# result = software_architecture_ai_agent.build_architecture("write me a ecommerce website for dropshipping for pets products") 
# print(result)
# print("software architecture document created correctely ") 
# software_architecture_ai_agent.build_architecture_chat(exp) 
# print("\n\n\n\n *************************")

# result = software_architecture_ai_agent.build_architecture("write me a budget management app") 
# print(result)



       
