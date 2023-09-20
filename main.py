import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

template = """
    I want you to be an excellent Chinese patent attorney, \
    you have an undergraduate degree in engineering and a doctoral degree in law. \
    With over 20 years of practice, you've drafted more than 3,000 invention patents and 2,000 utility model patents. \
    Based on the following description and any material you can gather, \
    please draft the first {patent} patent claim with more than 500 words in the language of {language} . please double check whether there is only one claim! \
    Ensure that the patent office examiner will not reject this new patent due to lack of novelty, inventiveness, or missing essential technical features. please double check.\
    Please think step by step and write down the technical features of the invention. \
    The description contains many technical features selected from different patents, please combine them into a new patent and make the new patent totally defferent from the original ones. \
    
    **
    Here is two examples of the patent claim:
    
    
1. A method implemented by a network node in a Bit Index Explicit Replication Traffic Engineering (BIER-TE) domain, comprising:
generating a fast reroute bit index forwarding table (FRR-BIFT) containing a backup path from the network node to each next hop of a neighbor node of the network node, wherein the backup path is represented by one or more bit positions for adjacencies along the backup path; and
sending a packet to the next hop of the neighbor node in accordance with the backup path of the FRR-BIFT when the neighbor node has failed.

1. A method of fabricating a three-dimensional (3D) NAND memory structure, comprising:
forming a memory hole in a semiconductor structure including a plurality of stacked layers, the memory hole having a depth to diameter aspect-ratio of at least 25:1; and
forming a dielectric on sidewalls of the memory hole having a cross-section profile where a first thickness of the dielectric proximate to a bottom of the memory hole is greater than or equal to a second thickness of the dielectric in at least one portion of memory hole above the bottom of the memory hole.
    
    **
    
    The description is as follows:{abstract}
    
    
"""

prompt = PromptTemplate(
    input_variables=["patent", "language", "abstract"],
    template=template,
)

# llm = OpenAI(temperature=.7, openai_api_key=st.secrets['OPENAI_API_KEY'], openai_api_base=st.secrets['OPENAI_API_BASE'])
llm = OpenAI(temperature=.7, openai_api_key=st.secrets['OPENAI_API_KEY'])

openai_api_key=st.secrets['OPENAI_API_KEY']

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
            abstract_drafted = llm(prompt_with_abstract)
            st.info(abstract_drafted)
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



