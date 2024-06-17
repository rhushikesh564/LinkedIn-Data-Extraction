import os
import requests
from PyPDF2 import PdfReader
import PyPDF2 as pdf1
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain_cohere import ChatCohere
import streamlit as st

def scrape_linkedin_profile(linkedin_profile_url:str):

    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}

    response = requests.get(
        api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
    )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


def input_pdf_text(uploaded_file):
    reader = pdf1.PdfReader(uploaded_file)
    text = ""
    for page_number in range(len(reader.pages)):
        page = reader.pages[page_number]
        text += str(page.extract_text())

    return text


def linkedin_summary(linkedin_profile_url:str):
    if st.button(f"Action for {linkedin_profile_url}"):
        linkedin_data = """{'public_identifier': 'rhushikesh-ingole-425516230', 'profile_pic_url': 'https://s3.us-west-000.backblazeb2.com/proxycurl/person/rhushikesh-ingole-425516230/profile?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=0004d7f56a0400b0000000001%2F20240527%2Fus-west-000%2Fs3%2Faws4_request&X-Amz-Date=20240527T100510Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=d9c0734ef607127404ad7a48e36d032097b10f2f562aa996b6d7c8d4108f1a1a', 'first_name': 'Rhushikesh', 'last_name': 'Ingole', 'full_name': 'Rhushikesh Ingole', 'follower_count': 51, 'occupation': 'Associate Consultant at Eviden', 'headline': 'Python Developer || Software Developer || Generative AI || Cloud Administrator || PLSQL Developer', 'country': 'IN', 'country_full_name': 'India', 'city': 'Pune', 'state': 'Maharashtra', 'experiences': [{'starts_at': {'day': 1, 'month': 9, 'year': 2022}, 'ends_at': None, 'company': 'Eviden', 'company_linkedin_profile_url': 'https://www.linkedin.com/company/eviden', 'company_facebook_profile_url': None, 'title': 'Associate Consultant', 'description': None, 'location': 'Pune, Maharashtra, India', 'logo_url': 'https://s3.us-west-000.backblazeb2.com/proxycurl/company/eviden/profile?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=0004d7f56a0400b0000000001%2F20240527%2Fus-west-000%2Fs3%2Faws4_request&X-Amz-Date=20240527T100510Z&X-Amz-Expires=1800&X-Amz-SignedHeaders=host&X-Amz-Signature=0fa51b287e006b507c3cf4bd1c2245af045a6aaa6c99a73b3d73d383d4334ce7'}], 'education': [{'starts_at': {'day': 1, 'month': 1, 'year': 2017}, 'ends_at': {'day': 31, 'month': 12, 'year': 2022}, 'field_of_study': 'Electrical and Electronics Engineering', 'degree_name': 'Bachelor of Engineering - BE', 'school': 'P.r.pote collage of Engineering and management , Amaravati', 'school_linkedin_profile_url': None, 'school_facebook_profile_url': None, 'description': None, 'logo_url': None, 'grade': None, 'activities_and_societies': None}], 'connections': 51, 'groups': [{'name': 'Artificial Intelligence Investors Group: Robotics, Machine Learning, NLP, Computer Vision & IoT', 'url': 'https://www.linkedin.com/groups/4376214'}, {'name': 'Machine Learning, Artificial Intelligence, Deep Learning, Computer Vision, Robotics, DataOps, Gen AI', 'url': 'https://www.linkedin.com/groups/6773411'}]}
        """
        summary_template = """
        given input information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        """

        summary_prompt_template = PromptTemplate(input_variables = ["information"],template = summary_template) 
        llm = ChatCohere()  
        chain = LLMChain(llm=llm, prompt = summary_prompt_template)
        return st.write(chain.run(information=linkedin_data))
    