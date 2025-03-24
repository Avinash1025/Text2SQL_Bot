
def sql_llm_prompt_function(query_str, schema) -> str:
    
    print(schema)
    
    prompt_str = (f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an AI assistant that generates a `sqlite` query strictly following the user's input. You are given the following inputs:
- User Input: {query_str}
- Schemas: {schema}
**SQL Query Generation Guidelines:**
- Only use the columns listed in the schema of the selected table.
- Avoid using columns or database-specific functions that are not present in the selected table's schema.
- The generated SQL query must strictly follow `sqlite` syntax.

 <|eot_id|>
# question:<|start_header_id|>user<|end_header_id|> : {query_str}

You are strictly required to always give the answer in the following format :
Question: Question here
Table Selected For Query: Table Name
Selected Table Schema: Table Schema
SQLQuery: SQL Query to run
Explanation: Explanation of SQL Query

Give only and only the SQL query, dont give any text with it.
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>""")

    print(prompt_str)
    return prompt_str

import pandas as pd
from math import ceil
def final_response_prompt(query_str, sql_query, data) -> str:
    try:
        data_str = data[0].metadata
        data_str.pop("sql_query", None)
    except Exception as e:
        print(f"Error: {e}")
        data_str = data
         
    if data:
        prompt_str = (
            "You are an AI  assistant designed to provide clear, detailed, and well-structured responses"
            
            f"User's Input: {query_str}\n\n"

            "SQL Query used to answer the user's question:\n"
            f"{sql_query}\n\n"
            
            "Data provided to answer the user's question\n"
            f"{data_str}\n\n"
            
            "Instructions:\n"
            "Synthesize a comprehensive response using the provided data to answer the user's query.\n"
            "Adhere to the date ranges and time formats present in the data.\n"

            "Format the response for clarity:\n"
            "  - Use **bold** for emphasis where needed.\n"
            "  - Utilize bullet points for listing multiple items or findings.\n"
            "  - Use tables to present structured or comparative data.\n"
            
            "Additional Guidelines:\n"
            "- You are strictly advice do not include or reference the SQL query or the table names in the response.\n"
            "- Exclude any extraneous information or statistics that are not available in the data.\n"
            "- The response should be concise, directly address the query, and offer relevant insights or context when appropriate.\n\n"
            
            "Response: "
        )
    else:
        prompt_str = (
            "It seems that the provided data is empty, or the query didn't return any results.\n"
            "User's Query: " + query_str + "\n\n"
            "Unfortunately, no result were able to fetch. This could be due to a few reasons:\n"
            "- There could be missing or incomplete data in the relevant time period or zone.\n"
            "- The query might not have been properly formulated or could lack sufficient information.\n"

            "To proceed, please consider the following suggestions:\n"
            "- Rephrase your question or provide more details to clarify what you're looking for.\n"
            "- Verify the data availability for the specified criteria.\n"
            "- Ensure there are no typos or errors in the query.\n\n"
            "Response: "
        )

    print(prompt_str)
    return prompt_str

      

CONTEXT = [
   f"""
Employee_Name: Full name of the employee.
EmpID: Unique employee identification number.
MarriedID: Indicates if the employee is married (1 = Yes, 0 = No).
MaritalStatusID: Numeric code representing marital status.
GenderID: Numeric code representing gender.
EmpStatusID: Numeric code representing employment status.
DeptID: Numeric code for the department.
PerfScoreID: Numeric code for performance score.
FromDiversityJobFairID: Indicates if hired from a diversity job fair (1 = Yes, 0 = No).
Salary: Employee's salary.
Termd: Indicates if the employee is terminated (1 = Yes, 0 = No).
PositionID: Numeric code for the job position.
Position: Job title of the employee.
State: Employee's work location state.
Zip: Zip code of the work location.
DOB: Date of birth of the employee.
Sex: Gender of the employee.
MaritalDesc: Marital status description.
CitizenDesc: Citizenship status of the employee.
HispanicLatino: Indicates if the employee is Hispanic/Latino (Yes/No).
RaceDesc: Employee's race/ethnicity.
DateofHire: Date when the employee was hired.
DateofTermination: Date when the employee was terminated (if applicable).
TermReason: Reason for employee termination.
EmploymentStatus: Current employment status (e.g., Full-time, Part-time).
Department: Department where the employee works.
ManagerName: Name of the employee's manager.
ManagerID: Unique ID of the manager.
RecruitmentSource: Source through which the employee was hired.
PerformanceScore: Performance rating of the employee.
EngagementSurvey: Employee's engagement survey score.
EmpSatisfaction: Employee satisfaction score.
SpecialProjectsCount: Number of special projects assigned.
LastPerformanceReview_Date: Date of the last performance review.
DaysLateLast30: Days the employee was late in the last 30 days.
Absences: Total number of absences.
"""
]