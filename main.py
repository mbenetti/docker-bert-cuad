#%% Libraries
from urllib import response
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from scripts.predict import run_prediction
from transformers.pipelines import pipeline
import json
import pandas as pd 
import time
from time import sleep
import base64

# OCR libs
from PIL import Image     
import pytesseract   

#Streamlit libs
import streamlit as st
import streamlit.components.v1 as stc

# File Processing Pkgs
import pandas as pd
import docx2txt
from PIL import Image 
from PyPDF2 import PdfFileReader
import pdfplumber


#%% Setups 
st.set_page_config(layout="wide")
image = Image.open('./banner.PNG')
st.image(image)
questions = ['Highlight the parts (if any) of this contract related to "Document Name". Details: The name of the contract', 'Highlight the parts (if any) of this contract related to "Parties". Details: The two or more parties who signed the contract', 'Highlight the parts (if any) of this contract related to "Agreement Date". Details: The date of the contract', 'Highlight the parts (if any) of this contract related to "Effective Date". Details: The date when the contract is effective\xa0', 'Highlight the parts (if any) of this contract related to "Expiration Date". Details: On what date will the contract\'s initial term expire?', 'Highlight the parts (if any) of this contract related to "Renewal Term". Details: What is the renewal term after the initial term expires? This includes automatic extensions and unilateral extensions with prior notice.', 'Highlight the parts (if any) of this contract related to "Notice Period To Terminate Renewal". Details: What is the notice period required to terminate renewal?', 'Highlight the parts (if any) of this contract related to "Governing Law". Details: Which state/country\'s law governs the interpretation of the contract?', 'Highlight the parts (if any) of this contract related to "Most Favored Nation". Details: Is there a clause that if a third party gets better terms on the licensing or sale of technology/goods/services described in the contract, the buyer of such technology/goods/services under the contract shall be entitled to those better terms?', 'Highlight the parts (if any) of this contract related to "Non-Compete". Details: Is there a restriction on the ability of a party to compete with the counterparty or operate in a certain geography or business or technology sector?\xa0', 'Highlight the parts (if any) of this contract related to "Exclusivity". Details: Is there an exclusive dealing\xa0 commitment with the counterparty? This includes a commitment to procure all “requirements” from one party of certain technology, goods, or services or a prohibition on licensing or selling technology, goods or services to third parties, or a prohibition on\xa0 collaborating or working with other parties), whether during the contract or\xa0 after the contract ends (or both).', 'Highlight the parts (if any) of this contract related to "No-Solicit Of Customers". Details: Is a party restricted from contracting or soliciting customers or partners of the counterparty, whether during the contract or after the contract ends (or both)?', 'Highlight the parts (if any) of this contract related to "Competitive Restriction Exception". Details: This category includes the exceptions or carveouts to Non-Compete, Exclusivity and No-Solicit of Customers above.', 'Highlight the parts (if any) of this contract related to "No-Solicit Of Employees". Details: Is there a restriction on a party’s soliciting or hiring employees and/or contractors from the\xa0 counterparty, whether during the contract or after the contract ends (or both)?', 'Highlight the parts (if any) of this contract related to "Non-Disparagement". Details: Is there a requirement on a party not to disparage the counterparty?', 'Highlight the parts (if any) of this contract related to "Termination For Convenience". Details: Can a party terminate this\xa0 contract without cause (solely by giving a notice and allowing a waiting\xa0 period to expire)?', 'Highlight the parts (if any) of this contract related to "Rofr/Rofo/Rofn". Details: Is there a clause granting one party a right of first refusal, right of first offer or right of first negotiation to purchase, license, market, or distribute equity interest, technology, assets, products or services?', 'Highlight the parts (if any) of this contract related to "Change Of Control". Details: Does one party have the right to terminate or is consent or notice required of the counterparty if such party undergoes a change of control, such as a merger, stock sale, transfer of all or substantially all of its assets or business, or assignment by operation of law?', 'Highlight the parts (if any) of this contract related to "Anti-Assignment". Details: Is consent or notice required of a party if the contract is assigned to a third party?', 'Highlight the parts (if any) of this contract related to "Revenue/Profit Sharing". Details: Is one party required to share revenue or profit with the counterparty for any technology, goods, or\xa0services?', 'Highlight the parts (if any) of this contract related to "Price Restrictions". Details: Is there a restriction on the\xa0 ability of a party to raise or reduce prices of technology, goods, or\xa0 services provided?', 'Highlight the parts (if any) of this contract related to "Minimum Commitment". Details: Is there a minimum order size or minimum amount or units per-time period that one party must buy from the counterparty under the contract?', 'Highlight the parts (if any) of this contract related to "Volume Restriction". Details: Is there a fee increase or consent requirement, etc. if one party’s use of the product/services exceeds certain threshold?', 'Highlight the parts (if any) of this contract related to "Ip Ownership Assignment". Details: Does intellectual property created\xa0 by one party become the property of the counterparty, either per the terms of the contract or upon the occurrence of certain events?', 'Highlight the parts (if any) of this contract related to "Joint Ip Ownership". Details: Is there any clause providing for joint or shared ownership of intellectual property between the parties to the contract?', 'Highlight the parts (if any) of this contract related to "License Grant". Details: Does the contract contain a license granted by one party to its counterparty?', 'Highlight the parts (if any) of this contract related to "Non-Transferable License". Details: Does the contract limit the ability of a party to transfer the license being granted to a third party?', 'Highlight the parts (if any) of this contract related to "Affiliate License-Licensor". Details: Does the contract contain a license grant by affiliates of the licensor or that includes intellectual property of affiliates of the licensor?\xa0', 'Highlight the parts (if any) of this contract related to "Affiliate License-Licensee". Details: Does the contract contain a license grant to a licensee (incl. sublicensor) and the affiliates of such licensee/sublicensor?', 'Highlight the parts (if any) of this contract related to "Unlimited/All-You-Can-Eat-License". Details: Is there a clause granting one party an “enterprise,” “all you can eat” or unlimited usage license?', 'Highlight the parts (if any) of this contract related to "Irrevocable Or Perpetual License". Details: Does the contract contain a\xa0 license grant that is irrevocable or perpetual?', 'Highlight the parts (if any) of this contract related to "Source Code Escrow". Details: Is one party required to deposit its source code into escrow with a third party, which can be released to the counterparty upon the occurrence of certain events (bankruptcy,\xa0 insolvency, etc.)?', 'Highlight the parts (if any) of this contract related to "Post-Termination Services". Details: Is a party subject to obligations after the termination or expiration of a contract, including any post-termination transition, payment, transfer of IP, wind-down, last-buy, or similar commitments?', 'Highlight the parts (if any) of this contract related to "Audit Rights". Details: Does a party have the right to\xa0 audit the books, records, or physical locations of the counterparty to ensure compliance with the contract?', 'Highlight the parts (if any) of this contract related to "Uncapped Liability". Details: Is a party’s liability uncapped upon the breach of its obligation in the contract? This also includes uncap liability for a particular type of breach such as IP infringement or breach of confidentiality obligation.', 'Highlight the parts (if any) of this contract related to "Cap On Liability". Details: Does the contract include a cap on liability upon the breach of a party’s obligation? This includes time limitation for the counterparty to bring claims or maximum amount for recovery.', 'Highlight the parts (if any) of this contract related to "Liquidated Damages". Details: Does the contract contain a clause that would award either party liquidated damages for breach or a fee upon the termination of a contract (termination fee)?', 'Highlight the parts (if any) of this contract related to "Warranty Duration". Details: What is the duration of any\xa0 warranty against defects or errors in technology, products, or services\xa0 provided under the contract?', 'Highlight the parts (if any) of this contract related to "Insurance". Details: Is there a requirement for insurance that must be maintained by one party for the benefit of the counterparty?', 'Highlight the parts (if any) of this contract related to "Covenant Not To Sue". Details: Is a party restricted from contesting the validity of the counterparty’s ownership of intellectual property or otherwise bringing a claim against the counterparty for matters unrelated to the contract?', 'Highlight the parts (if any) of this contract related to "Third Party Beneficiary". Details: Is there a non-contracting party who is a beneficiary to some or all of the clauses in the contract and therefore can enforce its rights against a contracting party?']
questions2 = ['Document Name:','Parties:','Agreement Date:','Effective Date:','Expiration Date:','Renewal Term:','Notice Period To Terminate Renewal:','Governing Law:','Most Favored Nation:','Non-Compete:','Exclusivity:','No-Solicit Of Customers:','Competitive Restriction Exception:','No-Solicit Of Employees:','Non-Disparagement:','Termination For Convenience:','Right of First Refusal, Offer or Negotiation (ROFR/ROFO/ROFN):','Change Of Control:','Anti-Assignment:','Revenue/Profit Sharing:','Price Restrictions:','Minimum Commitment:','Volume Restriction:','Ip Ownership Assignment:','Joint Ip Ownership:','License Grant:','Non-Transferable License:','Affiliate License-Licensor:','Affiliate License-Licensee:','Unlimited/All-You-Can-Eat-License:','Irrevocable Or Perpetual License:','Source Code Escrow:','Post-Termination Services:','Audit Rights:','Uncapped Liability:','Cap On Liability:','Liquidated Damages:','Warranty Duration:','Insurance:','Covenant Not To Sue:','Third Party Beneficiary:']

if 'contract' not in st.session_state:
    st.session_state['contract'] = ''
    st.session_state['predictions'] = ''
    st.session_state['response'] = []
    st.session_state['docx_file'] = []

model_checkpoint = './cuad-models/roberta-base'

#%% Streamlit app
# funtions
def load_model():
    model = AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint , use_fast=False)
    return model, tokenizer

@st.cache
def load_image(image_file):
	img = Image.open(image_file)
	return img 

@st.cache
def read_pdf(file):
    allpages= ''
    pdfReader = pdfplumber.open(file)
    #page = pdf.pages[1] 
    #print(pdfReader.extract_text())
    #print(len(pdfReader.pages))
    for i in range (len(pdfReader.pages)):
        page = pdfReader.pages[i]
        allpages += page.extract_text()
    return allpages

@st.cache
def read_pdf_with_pdfplumber(file):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
        return page.extract_text()


def show_pdf(file):
    with file as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1350" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


st.sidebar.markdown(
"""
**Project:** 

https://www.atticusprojectai.org/cuad

**Git Hub:** 

https://github.com/TheAtticusProject/cuad

**CUAD Dataset:** 

https://huggingface.co/datasets/cuad

Bert models licences Apache License 2.0

*Benetti Mauro 05.2022*

mauro.benetti@gmail.com

*License: CC BY 4.0* 
##### https://creativecommons.org/licenses/by/4.0/*
"""
)

# Elements on the center of the layout
# Top center
row1_1, row1_2 = st.columns([3, 2])
with row1_1:
	st.markdown('##### NLP as a service based on **Contract Understanding Atticus Dataset** (CUAD)')

with row1_2:
    st.write("""## """)

with st.expander("Additional information about the project"):
     st.write("Contract Understanding Atticus Dataset (CUAD) v1 is a corpus of 13,000+ labels in 510 commercial legal contracts that have been manually labeled under the supervision of experienced lawyers to identify 41 types of legal clauses that are considered important in contact review in connection with a corporate transaction, including mergers & acquisitions, etc.")

# Center of the app
col1, col2, col3= st.columns([5,8,3])
with col1:  
	st.markdown("##### 1 - Upload an external document")

	docx_file = st.file_uploader("Upload File",type=['txt','docx','pdf'])
	Upload_Button = st.button("Upload", key=None)
	if Upload_Button:
		with st.spinner("Loading..."):
			time.sleep(2)
		#st.success("Done!")
		if docx_file is not None:
			file_details = {"Filename":docx_file.name,"FileType":docx_file.type,"FileSize":docx_file.size}
			#st.write(file_details)
			# Check File Type
			if docx_file.type == "text/plain":
				#st.text(str(docx_file.read(),"utf-8"))
				raw_text = str(docx_file.read(),"utf-8")
				st.session_state.contract = raw_text
			elif docx_file.type == "application/pdf":
				raw_text = read_pdf(docx_file)
				st.session_state.contract = raw_text
				st.session_state.docx_file = docx_file
			elif docx_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
			# Use the right file processor ( Docx,Docx2Text,etc)
				raw_text = docx2txt.process(docx_file)
				st.session_state.contract = raw_text

if Upload_Button == True and docx_file.type == "application/pdf":
	docx_file = st.session_state.docx_file
	with st.expander ("Show pdf preview"):
		show_pdf(docx_file)

with col2:
	st.markdown('##### 2 - Choose one of the 41 elements of the contract')
	selected_question = st.selectbox('Query', questions)
	question_set = [questions[0], selected_question]


	Run_Button = st.button("Run the selected query on the contract", key=None)
	#st.markdown("Answer to the query : ")
	contract = st.session_state.contract
	if Run_Button == True and not len(contract)==0 and not len(question_set)==0:
		with st.spinner("Analyzing..."):
			prediction = run_prediction(question_set, contract, model_checkpoint)
		#st.success("Done!")
		for i, p in enumerate(prediction):
			if i != 0: st.write(f"Question:\n{question_set[int(p)]}\n\nAnswer: {prediction[p]}\n\n")

with col3:
	st.markdown("##### 3 - Run a complete analysis and download the results")
	Save_Button = st.button("Run a complete analysis", key=None)
	if Save_Button == True and not len(contract)==0 and not len(question_set)==0:
		with st.spinner("Analyzing..."):
			with open('temp/contract.txt', 'w') as f:
				f.write(' '.join(contract.split()))
			predictions = run_prediction(questions, contract, model_checkpoint)
			st.session_state.predictions = predictions
			st.success("Done!")

		pred_list = [] 
		for i, p in enumerate(predictions):
			pred_list.append(predictions[p])

		data_tuples = list(zip(questions2,pred_list))
		response = pd.DataFrame(data_tuples, columns=['Question','Answer'])
		st.session_state.response = response
		
		with open('temp/predictions.txt', 'w') as f:
			for i, p in enumerate(predictions):
				f.write(f"{i+1}){questions2[int(p)]}\n   {predictions[p]} \n")


	with open('temp/predictions.txt') as f:
		st.download_button('Download results', f,file_name='results.txt')  # Defaults to 'text/plain'



if Save_Button == True and not len(contract)==0 and not len(question_set)==0:
    with st.expander("Show answers"):
        st.table (st.session_state.response)
