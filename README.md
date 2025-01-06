# TalentScout Hiring Assistant Chatbot

## Project Overview

The TalentScout Hiring Assistant Chatbot is designed to streamline the technical interview process for recruiters. It assists by collecting candidate information and evaluating their technical knowledge based on their skills and experience. It generates interview questions tailored to the candidate's tech stack and evaluates the candidate's responses on a scale of 1 to 10.

The chatbot asks the candidate for the following information:

- Full Name
- Email Address
- Phone Number
- Experience
- Desired Position
- Current Location
- Tech Stack

Once the information is gathered, the chatbot generates technical questions, evaluates answers, and provides an average score for the candidate's performance. The candidate's details and the evaluation score are saved in a text file for future reference.

## Features

- **Personalized Candidate Information Collection**: The chatbot collects all necessary details about the candidate including their full name, email, phone number, experience, desired position, and tech stack.
- **Technical Interview Questions Generation**: Based on the candidate's tech stack, the chatbot generates a set of 5 tailored interview questions.
- **Evaluation of Candidate Responses**: The chatbot evaluates the candidate's answers on a scale of 1 to 10.
- **Candidate Data Storage**: The candidate's personal information and their interview performance (average score) are saved in a text file for future review.
- **Customizable Tech Stack**: The candidate can select from a wide variety of tech stacks related to frontend, backend, database, version control, tools, and hardware.

## Technologies Used

- **Streamlit**: A Python library for building interactive web applications.
- **Google Generative AI (Gemini-1.5-Flash)**: Used to generate the technical interview questions and evaluate the answers.
- **AWS Secrets Manager**: To securely retrieve API keys.
- **Phone Numbers**: The `phonenumbers` library to validate phone numbers.
- **Boto3**: AWS SDK for Python used to interact with AWS services.
- **Python**: The programming language used to implement the application.

## Setup and Installation

### Prerequisites

- Python 3.7+
- Install the following Python libraries:

## Installation Models

```bash
pip install -r requirements.txt
```

## Configuration

- Set up your API key in the AWS Secrets Manager and ensure it's accessible via the `TalentScoutAPIKey` secret name.
- If not using Secrets Manager, you can hardcode your API key by replacing `API_KEY` in the code with your actual key.

## Running the Application

```bash
streamlit run app.py
```

## Workflow

- The chatbot begins by collecting basic candidate information (name, email, phone number, etc.).

- Based on the tech stack selected, the chatbot generates interview questions tailored to the candidate's skills.

- The candidate answers each question, and the chatbot evaluates the responses.

- At the end of the interview, the chatbot calculates the average score and saves the candidate's data in a text file.

- The chatbot allows the option to restart the process or end the chat.

## Example Candidate Flow
- **Step 1:** Enter Full Name
- **Step 2:** Enter Email Address
- **Step 3:** Enter Phone Number (with country code)
- **Step 4:** Enter Experience
- **Step 5:** Select Desired Position
- **Step 6:** Enter Current Location
- **Step 7:** Select Tech Stack (Frontend, Backend, Database, etc.)
- **Step 8:** Answer Technical Interview Questions
- **Step 9:** Receive Evaluation Score and Save Data

## Contributing

If you'd like to contribute to this project, feel free to submit a pull request. We welcome any improvements, bug fixes, and additional features.

## License

This project is licensed under the MIT `License`