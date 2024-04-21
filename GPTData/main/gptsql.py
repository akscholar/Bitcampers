from dotenv import load_dotenv
import os
import openai
import subprocess
import sqlite3
import csv

class gpts:
    def do(self, user_query):
        load_dotenv()

        with open('GPTData/main/database-info.txt', 'r') as file:
            database_info = file.read()

        openai.api_key = os.getenv("OPENAI_API_KEY")


        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a sql expert in data analysis"},
                {"role": "user", "content": 
                f'''
                    Pretend you are a sql data analsyis,

                    My database break down is as follows:

                    {database_info}
                    
                    where 1 = single, 2 = married, 3 = widower, 4 = divorced, 5 = facto 
                    union, and 6 = legally seperated from Maritalstatus

                    where 33 = Biofuel Production Technologies, 171 = Animation and Multimedia
                    Design, 8014 = Social Service (evening attendance), 9003 = Agronomy,
                    9070 = Communication Design, 9085 = Veterinary Nursing, 9119 = Informatics
                    Engineering (includes Computer Science), 9130 = Equinculture, 
                    9147 = Management, 9238 = Social Service, 9254 = Tourism, 9500 = Nursing,
                    9556 = Oral Hygiene, 9670 = Advertising and Marketing Management, 9773 = 
                    Journalism and Communication, 9853 = Basic Education, and 9991 = Management
                    (evening attendance) from Course

                    where 1 = daytime and 0 = evening from Daytime/eveningattendance

                    where 1 = High Level Education (after secondary education), 
                    2 = Not Completed High School, 3 = middle school drop out, 4 = technical education

                    where 1 = Portugese, 2 = German, 6 = Spanish, 11 = Italian,
                    13 = Dutch, 14 = English, 17 = Lithuanian, 21 = Angolan, 22 = Cape Verdean,
                    24 = Guinean, 25 = Mozambican, 26 = Santomean, 32 = Turkish, 41 = Brazilian,
                    62 = Romanian, 100 = Moldova(Republic of), 101 = Mexican, 103 = Ukranian, 
                    105 = Russian, 108 = Cuban, and 109 = Columbian from Nacionality 

                    where 1 = yes and 0 = no from Displaced
                    
                    where 1 = yes and 0 = no from Educationspecialneeds

                    where 1 = yes and 0 = no from Debtor

                    where 1 = yes and 0 = no from Tuitionfeesuptodate
                    
                    where 1 = male and 0 = female for Gender from education_stats

                    where 1 = yes and 0 = no from Scholarshipholder
                    
                    where 1 = yes and 0 = no from International

                    where Dropout = Dropout and Graduate = Graduate from Result

                    I want you to give only the sql code as a output so for example:

                    Input: Tell me how many dropouts are girls
                    Output: 
                    SELECT Gender FROM education_stats;

                    Input: How likely is a 19-year old girl to drop out of college?
                    Output:
                    SELECT age and gender from education_stats and convert to a percent. Give the probability.
                
                    For less than 30 percent, output not likely
                    For less than 60 percent but greater than 30 percent, output slightly likely
                    For less than 80 percent but greater than 60 percent, output more likely
                    And for greater than 80 percent, output more likeley

                    If the output data is 0, say not likeley. Don't mention that there's a 0% likelihood

                    BE SURE NOT TO OUTPUT ANY FORMATTING OR MARKDOWN FORMATTING (like backticks). I want JUST the SQL CODE:


                    {user_query}'''}
                ]
            )

        query = chat_completion['choices'][0]['message']['content']

        conn = sqlite3.connect('GPTData/main/education.db')
        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()
        print(rows)

        with open('GPTData/main/extracted-data.csv', 'w', newline='') as f:
            #f.write("\n")
            writer = csv.writer(f)
            writer.writerows(rows)

        conn.close()


        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a expert in explaining data analysis to non technical audience"},
                {"role": "user", "content": 
                f''' Given this user query:

                    {user_query}

                    And this output:
                    {rows}

                    Explain the output data to me in letters, dont go into much technical details, your tagret audience is non technical. Just explain the output data and context
                    
        '''}
                ]
            )

        query_explain = chat_completion['choices'][0]['message']['content']

        return query_explain