#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#instalação
get_ipython().system('pip install yfinance==0.2.41')
get_ipython().system('pip install crewai==0.28.8')
get_ipython().system("pip install 'crewai[tools]'")
get_ipython().system('pip install langchain==0.1.20')
get_ipython().system('pip install langchain-openai==0.1.7')
get_ipython().system('pip install langchain-community==0.0.38')
get_ipython().system('pip install duckduckgo-search==5.3.0')


# In[1]:


#import das libs
import json 
import os
from datetime import datetime

import yfinance as yf

from crewai import Agent, Task, crew, Process

from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults 


# In[2]:


#Criando yahoo finance tool
def fetch_stock_price(ticket):
    stock = yf.download("ticket", start="2023-20-08", end="2024-20-08")
    return stock

yahoo_finance_tool = Tool(
    name="Yahoo Finance Tool",
    description="Fetches stocks prices for {ticket} from the last year about a specific company from Yahoo Finance API",
    func=lambda ticket: fetch_stock_price(ticket)  # Aqui, sem os parênteses
)


# In[ ]:


#Importando a open AI do GPT
os.environ['OPENAI_API_KEY'] = ""
lln = ChatOpenAI(model="gpt-3.5-turbo")


# In[ ]:


stockPriceAnalyst = Agent(
    role="Senior stock price Analyst",
    goal="FInd the {ticket} stock price and analyses trends",
    backstory="""You're higly experienced in analysing the price of an specifc stock and make predictions about its future price. """,
    verbose=True,
    llm=llm,
    max_iters=5,
    memory=True,
    tools=[yahoo_finance_tool],
    allow_denegation=False 
)


# In[ ]:


getstockPrice = Task(
    description="Analyze the stock {ticket} price history and create a trend analyses of up, down or sideways",
    expected_output="""Specify the current trend stock price - up, down, sideways.
     eg. stock='AAPL, price UP'
       """,
       agent=stockPriceAnalyst

)


# In[ ]:


#Importando a tool de search
search_tool = DuckDuckGoSearchResults(backend='news', num_results=10)


# In[ ]:


newsAnalyst = Agent(
    role="Stock News Analyst",
    goal="""Create a short summary of the market news related to the stock {ticket} companny. Specify the current trend - up, down or  sideways
    with the news context. For each requested stock asset, specify a numbet  between 0 and 100, where 0 is extreme fear and 100 is extreme greed. """,
    backstory="""You're highly expirenced in analyzing the market  trends and news and have tracked assest for more than 10 years.
     
    You're also master level analysts in the tradicional markets and have deep understanding of human psychology. 

    You undersatnd news, theirs tittles and information, but you look at those with health dose of skeptcism.
    You consider also the source of the news articles.

       """,
    verbose=True,
    llm= llm,
    max_iters= 5,
    memory=True,
    tools=[search_tool],
    allow_denegation=False
)


# In[ ]:


get_news = Task(
    description= f"""Take the stock and always include BTC to it (if not request).
    Use the search tool to search each one individually.data=
    The current date is {datetime.now()}.data=
    Compose the results into a helpfall report""",
    expected_output= """A sumamary of the overall market and one sentence summary for each request asset.
    <STOCK ASSET>
    <SUMMARY BASED ON NEWS>
    <TREND PREDICTION>
    <FEAR/GREED SCORE>""",
        agent= newsAnalyst
)


# In[ ]:


stockAnalystWriter= Agent(
    role="Senior Stock Analyst Writer",
    goal="""Analyze the trends price and news and write an insighfull compelling and informative 3 paragraph long newsletter base on the stock report and price trend.""",
    backstory= """You're widely accepeted as the best stock analyst in the market. You understand complex concepts and create compelling stories
    and narratives that resonate  with winder audience.

    You understand macro factors and combine multiple theories - eg. cycle theory and fundamental analyses.
    You're able to hold multiple opinions when analyzing anything. 

""",
verbose=True,
llm=llm,
max_iter=5,
memory=True,
allow_delegation=True
)


# In[ ]:


WriteAnalyses= Task(
    description="""Use the stock price trend and the stock news report to create an analyses  and write the newsletter about the {ticket} companny
    that is brief and highlights the most important points.
    Focus on the stock price trend, news and fear/greed score. What are the near future considerations?
    include the previous analyses os stock trend and news summary.
    """,
    expected_output="""An eloquent 3 paragraphs newsletter formated as markdown in an easy readable manner. it should contain:
    
    - 3 bullets executive summary
    - introduction - set the overall picture and spike up the interest
    - main part provides the meat of the analysis including the news summary and fear/greed scores
    - summary - key facts and concrete future trend prediction - up, donw or sideways.
    """,
    Agent=stockAnalystWriter,
    context = [getstockPrice, get_news]
)


# In[ ]:


crew = crew(
    Agent=[stockPriceAnalyst, newsAnalyst, stockAnalystWriter],
    tasks=[get_news, getstockPrice, WriteAnalyses],
    verbose=2,
    process=Process.hierarchical,
    full_output=True,
    share_crew=False,
    manager_llm=llm,
    max_iter=15
    )


# In[ ]:


results=crew.kickoff(inputs={'ticket': 'AAPL'})

with st.sidebar:
    st.header('Enter the Stock to Research')

    with st.form(key='research_form'):
        topic = st.text_input("Select the ticket")
        submit_button = st.form_submit_button(label = "Run Research")

if submit_button:
    if not topic:
        st.error("Please fill the ticket field")
    else:
        results = crew.kickoff(inputs={'ticket': topic})

        st.subheader("Results of your research:")
        st.write(results['final_output'])
