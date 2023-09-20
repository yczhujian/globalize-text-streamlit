import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    I want you to be a top American patent attorney, \
    and you have both engineering and legal doctor degrees. \
    Based on the following description and any material you can gather, \
    please draft the first claim with more than 500 words in {language} for a {language} {patent} patent. please double check whether there is only one claim! \
    Ensure that the {language} patent office examiner will not reject this new patent due to lack of novelty, inventiveness, or missing essential technical features. please double check.\
    Please think step by step and write down the Claim 1. 
    
    The description is as follows:{abstract} 
    
"""

template_2nd = """
    I want you to be an American patent attorney, and you have both engineering and legal doctor degrees. \
    Please redraft the following with more than 500 words to be more complicated to have higher sucess rate for grant for an invention patent in {language}:
    
    {first_response}

"""


prompt = PromptTemplate(
    input_variables=["patent", "language", "abstract"],
    template=template,
)

prompt_2nd = PromptTemplate(
    input_variables=["language","first_response"],
    template=template_2nd,
)


llm = OpenAI(temperature=0, openai_api_key=st.secrets['OPENAI_API_KEY'], openai_api_base=st.secrets['OPENAI_API_BASE'])
# llm = OpenAI(temperature=0, openai_api_key=st.secrets['OPENAI_API_KEY'])

openai_api_key=st.secrets['OPENAI_API_KEY']
openai_api_base=st.secrets['OPENAI_API_BASE']

st.set_page_config(page_title="R&D Assistant", page_icon=":book:")
st.header(":orange[R&D] Assistant System :book: :book:", divider='rainbow')
st.write("  ")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
      > Note：
      >  
      > Many R&D engineers conduct research and development based on the traditional brainstorming method, spending a lot of energy, but still the results are not good. 
      > The current R&D assistance tool combines more than 10 years of senior patent lawyers' experiences and AI intelligence. 
      > 
      > Any further queries, please just drop me a line：<1047534116@qq.com>
    """)

with col2:
    st.image(image='fourpatents.jpg', width=300, caption='The patent system added the fuel of interest to the fire of genius')

st.markdown("## Enter Your Requirements:")

col1, col2 = st.columns(2)
with col1:
    option_patent = st.selectbox(
        'Which patent would you like?',
        ('Invention', 'Utility Model'))
    
with col2:
    option_language = st.selectbox(
        'Which language would you like?',
        ('American', 'British', 'French', 'German'))

def get_abstract():
    input_text = st.text_area(label="Abstract", label_visibility='collapsed', placeholder="Your technical idea...", key="input_text")
    return input_text

abstract_input = get_abstract()

if len(abstract_input.split(" ")) > 700:
    st.write("Please enter a shorter description. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    # print ("in drafted")
    st.session_state.abstract_input = """This is a tool and method that helps spacecraft fly. 
    It checks the engine's condition in real-time and adjusts the flight direction based on that info.
    If there's an engine problem, this method helps the spacecraft fly more accurately to its destination.
    """
    
# st.button("*See An Example*", type='secondary', help="Click to see an example.", on_click=update_text_with_example)

# st.markdown("### Your claims for the Patent:")

# if abstract_input:

#     prompt_with_abstract = prompt.format(patent=option_patent, language=option_language, abstract=abstract_input)

#     drafted_abstract = llm(prompt_with_abstract)

#     st.info(drafted_abstract)


if st.button("Draft Patent Claim", type="primary"):
    if abstract_input:
        prompt_with_abstract = prompt.format(patent=option_patent, language=option_language, abstract=abstract_input)
        drafted_abstract = llm(prompt_with_abstract)
        st.info(drafted_abstract)
    else:
        st.write("Please enter a description. The maximum length is 700 words.")
        st.stop()


st.divider()

st.title("Patents Analysis around the World")    
st.image(image='patents.png', width=700, caption='Patents Granted')


tab1, tab2, tab3 = st.tabs(["R&D from Title", "R&D from Description", "R&D from PDF"])

with tab1:
   st.header("R&D Ideas from Title")
   col1, col2 = st.columns(2)
   with col1:
        tab_patent = st.selectbox(
        'Which patent would you like?',
        ('Invention', 'Utility Model'), key="tab_patent")
    
   with col2:
        tab_language = st.selectbox(
        'Which language would you like?',
        ('American', 'British', 'French', 'German'),key="tab_language")

   def get_abstract():
        tab_text = st.text_area(label="Abstract", label_visibility='collapsed', placeholder="Your technical idea...", key="tab_text")
        return tab_text

   tab_abstract = get_abstract()

   if len(tab_abstract.split(" ")) > 700:
        st.write("Please enter a shorter description. The maximum length is 700 words.")
        st.stop()
    
   if st.button("Draft Patent Claim", type="primary", key="tab_button"):
        if tab_abstract:
            prompt_with_abstract = prompt.format(patent=tab_patent, language=tab_language, abstract=tab_abstract)
            response_1st = llm(prompt_with_abstract)
            st.subheader("First draft:")
            st.info(response_1st)
            
            prompt_with_abstract_2nd = prompt_2nd.format(language=tab_language, first_response=response_1st)
            response_2nd = llm(prompt_with_abstract_2nd)
            st.subheader("final draft:")
            st.info(response_2nd)
        else:
            st.write("Please enter a description. The maximum length is 700 words.")
            st.stop()

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   uploaded_files = st.file_uploader("Choose a pdf file", accept_multiple_files=True)
   for uploaded_file in uploaded_files:
      bytes_data = uploaded_file.read()
      st.write("filename:", uploaded_file.name)
      st.write(bytes_data)



