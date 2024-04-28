from openai import OpenAI

client = OpenAI()

f = open("resumeCoachPrompts/software_in.txt", "r")
software_in = f.read()
f.close()

f = open("resumeCoachPrompts/software_out.txt", "r")
software_out = f.read()
f.close()

f = open("resumeCoachPrompts/accountant_in.txt", "r")
finance_in = f.read()
f.close()

f = open("resumeCoachPrompts/accountant_out.txt", "r")
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

begin_resume = "============\nBEGIN RESUME\n============\n"
end_resume = "==========\nEND RESUME\n==========\n"
begin_job_description = "====================\nBEGIN JOB DESCRIPTION\n====================\n"
end_job_description = "==================\nEND JOB DESCRIPTION\n==================\n"

def resumeCoach(resume: str, job_description: str):

    new_messages = messages.copy()
    input = begin_resume + resume + end_resume + begin_job_description + job_description + end_job_description
    new_messages.append({"role" : "user", "content" : input})

    response = client.create_chat(messages=new_messages)
    return response["choices"][0]["message"]["content"]