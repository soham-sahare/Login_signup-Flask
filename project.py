import pandas as pd
from fpdf import FPDF 
from datetime import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass

def clean():
    import os, re, os.path
    mypath = "myfolder"

    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))

    return "Mail Sent Successfully"

def mail(df):
   
    #from_, password = "sohamsaharego2@gmail.com", "Soham@123"
    from_, password = "soham.sahare@vit.edu.in", "QCgch772"
    #from_ = input("Enter your email : ")
    #password = getpass.getpass("Enter your password : ")

    print("\n")

    to = df['Email'].to_list()
    name = df['Name'].to_list()
    success = False

    try:
        server = smtplib.SMTP('smtp.outlook.com', 587)
        server.starttls()
        server.login(from_, password)
        success = True
    except :

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_, password)
            success = True
        except:

            try:
                server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
                server.starttls()
                server.login(from_, password)
                success = True
            except:
                
                try:
                    server = smtplib.SMTP('smtp.rediffmailpro.com', 587)
                    server.starttls()
                    server.login(from_, password)
                    success = True
                except:
                    
                    try:
                        server = smtplib.SMTP('smtp.rediffmail.com', 25)
                        server.starttls()
                        server.login(from_, password)
                        success = True
                    except:
                        success = False
                        print("Login Unsuccessfull")
                        
    if (success == True):

        print("Logged in successfully as : "+from_+"\n")            

        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        for i, j in zip(to, name) :

            data = MIMEMultipart()
            data['To'] = i
            data['From'] = from_
            data['Subject'] = "IA1"

            body = "Your Report"

            data.attach(MIMEText(body, 'plain'))

            p = "myfolder/{}.pdf".format(j)
            filename = p

            attachment = open(filename, "rb")

            p = MIMEBase('application', 'octet-stream')

            p.set_payload((attachment).read())

            encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            data.attach(p)
            
            print("Sending to : ", i)

            text = data.as_string()
            server.sendmail(from_, i, text)
            attachment.close()
            print("SENT\n")

        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        server.quit()

    else:
        print("Enter valid email and password")

    return clean()

def process(df):

    li = df.columns

    now = datetime.now()
    dt_time = now.strftime("%d/%m/%Y %H:%M:%S")

    for i in df.values:
    
        name, email, roll, m1, m2, m3, m4, m5 = i
        
        l = []
        
        for j in [m1, m2, m3, m4, m5]:
            if j < 16:
                remark = "You need {} marks in IA2 to pass".format(16-j)
                l.append(remark)
            else:
                remark = "You have passed in IA1 and IA2"
                l.append(remark)
        
        name = "{} : {}".format(li[0], name)
        email = "{} : {}".format(li[1], email)
        roll = "{} : {}".format(li[2], roll)
        m_1 = "{} : {}  ({})".format(li[3], m1, l[0])
        m_2 = "{} : {}  ({})".format(li[4], m2, l[1])
        m_3 = "{} : {}  ({})".format(li[5], m3, l[2])
        m_4 = "{} : {}  ({})".format(li[6], m4, l[3])
        m_5 = "{} : {}  ({})".format(li[7], m5, l[4])
        
        pdf = FPDF() 
        
        pdf.add_page() 
        pdf.set_font("Arial", size = 20) 
        
        pdf.cell(200, 10, txt = "VIDYALANKAR INSTITUTE OF TECHNOLOGY, MUMBAI",  ln = 1, align = 'C')
        pdf.set_font("Arial", size = 18) 

        pdf.cell(200, 10, txt = "INFORMATION TECHNOLOGY DEPARTMENT",  ln = 2, align = 'C')
        
        pdf.set_font("Arial", size = 15) 
        pdf.cell(200, 10, txt = " ",  ln = 3, align = 'L') 
        pdf.cell(200, 10, txt = "Date : {}".format(dt_time),  ln = 4, align = 'R')
        pdf.cell(200, 10, txt = " ",  ln = 5, align = 'L') 
        
        pdf.cell(200, 10, txt = name,  ln = 6, align = 'L') 
        pdf.cell(200, 10, txt = email, ln = 7, align = 'L') 
        pdf.cell(200, 10, txt = roll, ln = 8, align = 'L')
        
        pdf.cell(200, 10, txt = " ", ln = 9, align = 'L')
        
        pdf.cell(200, 10, txt = m_1, ln = 10, align = 'L') 
        pdf.cell(200, 10, txt = m_2, ln = 11, align = 'L') 
        pdf.cell(200, 10, txt = m_3, ln = 12, align = 'L') 
        pdf.cell(200, 10, txt = m_4, ln = 13, align = 'L') 
        pdf.cell(200, 10, txt = m_5, ln = 14, align = 'L') 
        pdf.cell(200, 10, txt = "Total : {} of 100".format(m1+m2+m3+m4+m5), ln = 15, align = 'L') 
        
        p = "myfolder/{}.pdf".format(i[0])
        pdf.output(p)

    return mail(df)

def readfile(l):

    try:
        df = pd.read_csv(l)
    except:
        try:
            df = pd.read_excel(l)
        except:
            return "Failed"

    
    return process(df)

def arrangement(l1, l2):
    
    try:
        df = pd.read_csv(l2)
    except:
        try:
            df = pd.read_excel(l2)
        except:
            return "Failed"

    #from_, password = "sohamsaharego2@gmail.com", "Soham@123"
    from_, password = "soham.sahare@vit.edu.in", "QCgch772"
    #from_ = input("Enter your email : ")
    #password = getpass.getpass("Enter your password : ")

    print("\n")

    to = df['Email'].to_list()
    success = False

    try:
        server = smtplib.SMTP('smtp.outlook.com', 587)
        server.starttls()
        server.login(from_, password)
        success = True
    except :

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_, password)
            success = True
        except:

            try:
                server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
                server.starttls()
                server.login(from_, password)
                success = True
            except:
                
                try:
                    server = smtplib.SMTP('smtp.rediffmailpro.com', 587)
                    server.starttls()
                    server.login(from_, password)
                    success = True
                except:
                    
                    try:
                        server = smtplib.SMTP('smtp.rediffmail.com', 25)
                        server.starttls()
                        server.login(from_, password)
                        success = True
                    except:
                        success = False
                        print("Login Unsuccessfull")
                        
    if (success == True):

        print("Logged in successfully as : "+from_+"\n")            

        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        for i in to:

            data = MIMEMultipart()
            data['To'] = i
            data['From'] = from_
            data['Subject'] = "IA Seating Arrangement"

            body = "Be sure to be 30 minutes before the exam. All the best!"

            data.attach(MIMEText(body, 'plain'))

            filename = l1

            attachment = open(filename, "rb")

            p = MIMEBase('application', 'octet-stream')

            p.set_payload((attachment).read())

            encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            data.attach(p)
            
            print("Sending to : ", i)

            text = data.as_string()
            server.sendmail(from_, i, text)
            attachment.close()
            print("SENT\n")

        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        server.quit()

    else:
        print("Enter valid email and password")

    return clean()