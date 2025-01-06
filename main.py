"""
PROJECT NAME : TALENTSCOUT HIRING ASSISTANT CHATBOT
PROJECT DESCRIPTION : This is a chatbot that helps recruiters to conduct technical interviews with candidates. The chatbot asks the candidate for their full name, email, phone number, experience, desired position, current location, and tech stack. It then generates technical interview questions based on the candidate's tech stack and evaluates the candidate's answers. The chatbot saves the candidate's information and average score in a text file.
NEME : TAMARAI SELVAN
DATE : 5-01-2025
EMAIL : tamaraiselvan98@gmail.com
PHONE : +91 9688814221
EXPERIENCE : 1
DESIRED POSITION : ASSOCIATE SOFTWARE ENGINEER
LINKEDIN : https://www.linkedin.com/in/tamarai-selvan-ravi-6b5311213/
DEPLOY : https://tamaraiselva-talentscout-hiring-chatbot-main-ub96d1.streamlit.app/
"""

import streamlit as st
import google.generativeai as genai
import re
import os
from datetime import datetime
import boto3
import json
import phonenumbers
from phonenumbers import geocoder, carrier

def get_api_key():
    secret_name = "TalentScoutAPIKey"
    region_name = "eu-north-1"  

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret)
        return secret_dict['API_KEY']
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None

API_KEY = get_api_key() or os.getenv("GOOGLE_API_KEY", "AIzaSyCX3ALsPKSIWOg8cYcX8P1KffxU1yF_SsE")



#if you want to run on local host comment out the get_api_key()function and hardcoded your API_KEY as below
#API_KEY = ""

def generate_questions(tech_stack):
    prompt = f"Generate 5 short and fundamental technical interview questions for a candidate with skills in {', '.join(tech_stack)}. Always try to give different types of questions. Questions should test basic knowledge in that field. Do not ask multiple choice questions and also do not give any other extra information. Only ask a question. Questions should be short or possible of 2-3-4 word answerable.Always ask different question from your previously asked on that tech-stack"
    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        response = model.generate_content(prompt)
        if response and hasattr(response, 'candidates'):
            content = response.candidates[0].content.parts[0].text
            questions = [q.strip() for q in content.split('\n') if q.strip()]
            return questions
        else:
            st.warning("No valid response received from the model.")
            return []
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return []

def evaluate_answer(question, user_answer):
    prompt = f"Evaluate the following answer to the question: '{question}'. Answer: '{user_answer}'. Score this answer on a scale of 1 to 10, and return only the score without any additional text."
    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        response = model.generate_content(prompt)
        if response and hasattr(response, 'candidates'):
            score_text = response.candidates[0].content.parts[0].text.strip()
            try:
                score = int(score_text.split('/')[0].strip())
                return max(1, min(10, score))
            except (ValueError, IndexError):
                return 1
        else:
            return 1
    except Exception as e:
        return 1

def is_valid_full_name(full_name):
    return re.match(r'^[A-Z][a-zA-Z\s]+$', full_name) is not None

country_codes = {
    "+1": "United States",
    "+44": "United Kingdom",
    "+91": "India",
    "+61": "Australia",
    "+81": "Japan",
    "+33": "France",
    "+49": "Germany",
    "+39": "Italy",
    # Add more country codes as needed
}

def is_valid_phone_number(phone_number, country_code):
    try:
        # Combine the country code with the phone number
        full_number = country_code + phone_number
        parsed_number = phonenumbers.parse(full_number)

        # Check if the phone number is valid
        if phonenumbers.is_valid_number(parsed_number):
            # You can also check the carrier or location if needed
            # carrier_name = carrier.name_for_number(parsed_number, "en")
            # location_name = geocoder.description_for_number(parsed_number, "en")
            return True
        else:
            return False
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

def save_candidate_data(candidate_info, average_score):
    try:
        if not os.path.exists("candidate_data"):
            os.makedirs("candidate_data")
        filename = f"candidate_data/{candidate_info['full_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as file:
            file.write("Candidate Information:\n")
            for key, value in candidate_info.items():
                file.write(f"{key.capitalize()}: {value}\n")
            file.write(f"Average Score: {average_score:.2f}\n")
        return filename
    except Exception as e:
        st.error(f"Error saving candidate data: {e}")
        return None

st.set_page_config(
        page_title="TalentScout Hiring Chatbot",
        page_icon="✍️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

st.title("TalentScout Hiring Chatbot")

if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.candidate_info = {}
    st.session_state.questions = []
    st.session_state.user_answers = []
    st.session_state.scores = []

genai.configure(api_key=API_KEY)

if st.session_state.step == 0:
    st.write("Hello! I'm the TalentScout Hiring Assistant. Let's start with some basic information.")
    with st.form(key="candidate_info_form"):
        full_name = st.text_input("ENTER YOUR FULL NAME")
        submit_name = st.form_submit_button("Next")
        if submit_name:
            if not is_valid_full_name(full_name):
                st.error("Please enter a valid full name (start with a capital letter, no numbers or special characters).")
            else:
                st.session_state.candidate_info['full_name'] = full_name
                st.session_state.step += 1
                st.rerun()

elif st.session_state.step == 1:
    with st.form(key="email_form"):
        email = st.text_input(f"ENTER YOUR EMAIL ADDRESS")
        submit_email = st.form_submit_button("Next")
        if submit_email:
            if not is_valid_email(email):
                st.error("Please enter a valid email address in the format username@gmail.com.")
            else:
                st.session_state.candidate_info['email'] = email
                st.session_state.step += 1
                st.rerun()

elif st.session_state.step == 2:
    with st.form(key="phone_form"):
        # Dropdown for selecting country code
        country_code = st.selectbox("Select your country code", options=list(country_codes.keys()))
        phone = st.text_input("Enter your phone number (without country code)")
        
        submit_phone = st.form_submit_button("Next")
        if submit_phone:
            if not phone.strip():
                st.error("Please enter your phone number.")
            elif not is_valid_phone_number(phone.strip(), country_code):
                st.error("Please enter a valid phone number.")
            else:
                full_phone_number = country_code + phone.strip()
                st.session_state.candidate_info['phone'] = full_phone_number
                st.session_state.step += 1
                st.rerun()

elif st.session_state.step == 3:
    with st.form(key="experience_form"):
        experience = st.number_input("SELECT YOUR EXPERIENCE", min_value=0)
        submit_experience = st.form_submit_button("Next")
        if submit_experience:
            st.session_state.candidate_info['experience'] = experience
            st.session_state.step += 1
            st.rerun()

elif st.session_state.step == 4:
    with st.form(key="position_form"):
        positions = ["Software Engineer", "Data Scientist", "Artificial Intelligent Intern", "Machine Learning Intern", "UI/UX Designer", "Product Manager", "Full Stack Developer","Cloud Engineer", "DevOps Engineer", "Business Analyst", "Systems Architect", "software Developer", "System Engineer", "Associate Software Engineer", "Data Analytics"]
        desired_position = st.selectbox("SELECT YOUR DESIRED POSITION", positions)
        submit_position = st.form_submit_button("Next")
        if submit_position:
            st.session_state.candidate_info['desired_position'] = desired_position
            st.session_state.step += 1
            st.rerun()

elif st.session_state.step == 5:
    with st.form(key="location_form"):
        current_location = st.text_input("WHERE YOU ARE CURRENTLY LOCATED WITH CITY NAME WITH COUNTRY NAME") 
        submit_location = st.form_submit_button("Next")
        if submit_location:
            st.session_state.candidate_info['current_location'] = current_location
            st.session_state.step += 1
            st.rerun()

elif st.session_state.step == 6:
    with st.form(key="tech_stack_form"):
        frontend_tech_stack = st.multiselect(
            "Select Frontend Tech Stack",
            options=[
                "HTML", "CSS", "JavaScript", "React.js", "Angular", "Vue.js", "Svelte", "jQuery",
                "Sass", "LESS", "Material-UI", "Bootstrap", "Tailwind CSS", "Ant Design",
                "Webpack", "Babel", "Parcel", "Vite", "Redux", "MobX", "Vuex", "Zustand", "Recoil",
                "NPM/Yarn", "TypeScript", "Storybook", "Next.js", "Nuxt.js"
            ],
            help="Select the frontend technologies you are familiar with."
        )
        
        backend_tech_stack = st.multiselect(
            "Select Backend Tech Stack",
            options=[
                "JavaScript (Node.js)", "Python (Django, Flask)", "Ruby (Ruby on Rails)", "Java (Spring Boot)",
                "PHP (Laravel)", "C# (ASP.NET Core)", "Go (Golang)", "C++", "Rust", "Express.js",
                "Django", "Flask", "Ruby on Rails", "Spring Boot", "Laravel", "ASP.NET Core", "FastAPI",
                "Koa.js", "RESTful APIs", "GraphQL", "gRPC", "OAuth", "JWT", "Passport.js", "Kafka", 
                "RabbitMQ", "Redis Pub/Sub"
            ],
            help="Select the backend technologies you are familiar with."
        )
        
        database_tech_stack = st.multiselect(
            "Select Database Tech Stack",
            options=[
                "MySQL", "PostgreSQL", "Oracle Database", "SQLite", "Microsoft SQL Server", "MongoDB",
                "Redis", "Cassandra", "CouchDB", "Firebase Realtime Database", "DynamoDB", "Neo4j", 
                "ArangoDB", "OrientDB", "Elasticsearch", "Solr", "Sequelize", "SQLAlchemy", "TypeORM", 
                "Mongoose"
            ],
            help="Select the database technologies you are familiar with."
        )
        
        version_control_tech_stack = st.multiselect(
            "Select Version Control Tech Stack",
            options=[
                "Git", "SVN (Subversion)", "Mercurial", "GitHub", "GitLab", "Bitbucket", "Azure DevOps", 
                "GitKraken", "SourceTree", "Git CLI", "Git LFS"
            ],
            help="Select the version control technologies you are familiar with."
        )
        
        tools_tech_stack = st.multiselect(
            "Select Tools Tech Stack",
            options=[
                "Visual Studio Code", "Sublime Text", "Atom", "IntelliJ IDEA", "PyCharm", "Eclipse", 
                "Xcode", "Android Studio", "Jenkins", "CircleCI", "Travis CI", "GitLab CI", "Bamboo", 
                "Docker", "Kubernetes", "Terraform", "Ansible", "Puppet", "Jest", "Mocha", "PyTest", 
                "Selenium", "Cypress", "Postman", "JUnit", "Jira", "Trello", "Asana", "Monday.com", 
                "Slack", "Confluence", "Figma", "Adobe XD", "Sketch", "InVision"
            ],
            help="Select the tools and CI/CD technologies you are familiar with."
        )
        
        hardware_tech_stack = st.multiselect(
            "Select Hardware Tech Stack",
            options=[
                "AWS EC2", "Google Cloud Compute Engine", "Microsoft Azure Virtual Machines", 
                "DigitalOcean Droplets", "IBM Cloud Virtual Servers", "Docker", "Kubernetes", 
                "VirtualBox", "VMware", "Routers (Cisco, Juniper)", "Switches", "Firewalls (Palo Alto, Fortinet)", 
                "NVIDIA GPUs", "Google TPUs", "Raspberry Pi", "Arduino", "Jetson Nano"
            ],
            help="Select the hardware technologies you are familiar with."
        )

        submit_tech_stack = st.form_submit_button("Submit Tech Stack")
        
        if submit_tech_stack:
            # Combine all selected tech stacks into one list
            tech_stack = frontend_tech_stack + backend_tech_stack + database_tech_stack + version_control_tech_stack + tools_tech_stack + hardware_tech_stack
            tech_stack = [tech.strip() for tech in tech_stack if tech.strip()]
            if tech_stack:
                questions_with_answers = generate_questions(tech_stack)
                for q in questions_with_answers:
                    question_text = q.strip()
                    if question_text:
                        st.session_state.questions.append(question_text)
                if len(st.session_state.questions) > 0:
                    st.session_state.step += 1
                    st.rerun()
            else:
                st.error("Please provide a valid tech stack.")


elif st.session_state.step == 7:
    if len(st.session_state.questions) > 0:
        question = st.session_state.questions[0]
        user_answer = st.text_input(question)
        if user_answer and st.button("Submit Answer"):
            score = evaluate_answer(question, user_answer)
            st.write(f"Score based on your answer is: {score} out of 10 (10 being the maximum score and 1 being the minimum score).")
            if len(st.session_state.questions) > 1:  
                st.write("Now, let's move to the next question. Press **Submit Answer** button again")
            st.session_state.user_answers.append(user_answer)
            st.session_state.scores.append(score)
            del (st.session_state.questions[0])
            if len(st.session_state.questions) == 0:
                average_score = sum(st.session_state.scores) / len(st.session_state.scores) if len(st.session_state.scores) > 0 else 0
                st.write(f"Average Score of your performance is: {average_score:.2f} out of 10")
                filename = save_candidate_data(st.session_state.candidate_info, average_score)
                if filename:
                    st.success(f"Thanks you have completed the test.Come Again because **Consistency is the key of success**")
                else:
                    st.warning("Failed to save your details.")
                if st.button("Finish the Test"):
                    st.session_state.step += 1
                    st.rerun()

        
        
elif st.session_state.step == 8:
    st.write("Thank you for participating!")
    if st.button("Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    st.write("You have answered all the questions.")
    st.session_state.step += 1
    st.rerun()

if 'step' in st.session_state and (st.session_state.step < 8):
    if st.button("End Chat"):
        st.session_state.step = 8
        st.write("Chat ended. Thank you!")
        st.rerun()