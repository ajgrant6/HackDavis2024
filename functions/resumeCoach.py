from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the absolute path to the file
path = os.path.join(script_dir, "data/resumeCoachPrompts/")

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

f = open(path + "software_in.txt", "r")
software_in = f.read()
f.close()

f = open(path + "software_out.txt", "r")
software_out = f.read()
f.close()

f = open(path + "accountant_in.txt", "r")
finance_in = f.read()
f.close()

f = open(path + "accountant_out.txt", "r")
finance_out = f.read()
f.close()

prompt = "You are an assistant that takes a given resume and job description and provides feedback as to whether the job is a good fit. If it is not, provide tips to improve."

messages = [
    {"role" : "system", "content" : prompt},
    {"role" : "user", "content" : software_in},
    {"role" : "system", "content" : software_out},
    {"role" : "user", "content" : finance_in},
    {"role" : "system", "content" : finance_out}
]

begin_resume = "============BEGIN RESUME============"
end_resume = "==========END RESUME=========="
begin_job_description = "====================BEGIN JOB DESCRIPTION===================="
end_job_description = "==================END JOB DESCRIPTION=================="

def resumeCoach(resume: str, job_description: str):

    new_messages = messages.copy()
    input = begin_resume + resume.replace('\n', '') + end_resume + begin_job_description + job_description.replace('\n', '') + end_job_description
    new_messages.append({"role" : "user", "content" : input})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=new_messages,

        max_tokens=500
    )
    text = str(completion.choices[0].message)
    # Remove ChatCompletionMessage(content=" from the beginning
    text = text[31:]
    # Remove , role='assistant', function_call=None, tool_calls=None) from the end
    text = text[:-57]


    # Use regex to remove \n and replace with a new line
    text = re.sub(r'\\n', '<br>', text)

    return text