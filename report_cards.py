import pandas as pd
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import sys

pdf_w=210
pdf_h=297

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(__file__)

temp_path = os.path.join(BASE_DIR, "temp")
if not os.path.exists(temp_path):
    os.mkdir(temp_path)

def create_margin(pdf): 
    pdf.set_fill_color(32.0, 47.0, 250.0) 
    pdf.rect(3.0, 3.0, 204.0,291.0,'DF')
    pdf.set_fill_color(255, 255, 255) 
    pdf.rect(5.0, 5.0, 200.0,287.0,'FD')  

def create_logo(pdf):
    pdf.set_xy(90,6)
    pdf.image(os.path.join(BASE_DIR,'school_logo.jpg'),w=30,h=25)
    pdf.set_xy(94,33)
    pdf.set_font("Arial",'I', size = 15)
    pdf.cell(0,0, txt = allstudents.iloc[0,7])
    pdf.line(8,36,202,36)

def create_studentpic(pdf):
    BASE_DIR2=os.path.join(BASE_DIR,'Pics for assignment')
    file='ABC'+str(i)+' XYZ'+str(i)+'.png'
    with Image.open(os.path.join(BASE_DIR2,file)) as img:
        img_array=np.array(img)
    img = Image.fromarray(np.uint8(img_array))
    img.save(os.path.join(BASE_DIR, "temp",file))
    pdf.set_xy(130,40)
    pdf.image(os.path.join(BASE_DIR, "temp",file),w=60,h=55)
    os.remove(os.path.join(BASE_DIR, "temp",file))
    
def create_studentinfo(pdf):
    col=list(allstudents.columns[1:13])
    val=list(allstudents.iloc[0,1:13])
    all={}
    for key in col:
        for value in val:
            all[key] = value
            val.remove(value)
            break  
    x1,y1=10,40
    x2,y2=60,40
    for key,value in all.items():
        pdf.set_xy(x1,y1)
        pdf.set_font('Arial','B',11)
        pdf.cell(0,0, txt = key+ ':',ln=1)
        pdf.set_xy(x2,y2)
        pdf.set_font('Arial','',11)
        pdf.cell(0,0, txt = str(value),ln=1)
        y1+=7.5
        y2+=7.5

def create_table(pdf):
    alldata=list(allstudents.columns[13:19])
    allvalue=[]
    numberofrows=len(allstudents.index)
    for i in range(numberofrows):
        allvalue.append(list(allstudents.iloc[i,13:19]))
    pdf.set_xy(90,125)
    pdf.cell(1,1,'Final Exam Result', border=0)
    pdf.set_xy(10,128)
    epw = pdf.w - pdf.l_margin
    col_width = epw/6.3
    th = pdf.font_size*1.26
    pdf.set_fill_color(75,172,198)
    for datum in alldata:                 
        if datum==alldata[3]:   
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.multi_cell(col_width, th+2, str(datum), border=1,fill=True)
            pdf.set_xy(x+31.75,y)                   
        elif datum<alldata[4]:
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.cell(col_width, th+16,str(datum),border=1,fill=True)
            pdf.set_xy(x+31.75,y)         
        else:
            x = pdf.get_x()
            y = pdf.get_y()  
            pdf.cell(col_width, th+16,str(datum),border=1,fill=True)
            pdf.set_xy(x+31.75,y) 
    pdf.set_xy(10,148.7)
    for row in allvalue:       
        for datum in row:
            pdf.cell(col_width, th, str(datum), border=1)
        pdf.ln(th)
    pdf.set_xy(185,275)
    pdf.set_font('Arial','',8)
    pdf.cell(1,1,'Page 1 of 2', border=0)

def create_studentgraphs(pdf):
    correct=0
    incorrect=0
    unattempted=0
    outcome=['Correct','Incorrect','Unattempted']
    lst=allstudents['Outcome (Correct/Incorrect/Not Attempted)'].tolist()
    for i in lst:
        if i=='Correct':
            correct+=1
        elif i=='Incorrect':
            incorrect+=1
        else:
            unattempted+=1
    values=[correct,incorrect,unattempted]
    plt.figure(figsize = (10, 5))
    plt.bar(outcome, values, color ='maroon', width = 0.4)
    plt.xlabel("Outcome For Questions",fontsize = 15)
    plt.ylabel("Nos Of Questions Answered",fontsize = 15)
    plt.title("Student Attempts",fontweight ='bold',fontsize = 18)
    plt.axis([-0.5,2.5,0,25])
    plt.savefig(os.path.join(temp_path,'student.png'))
    pdf.set_xy(30,40)
    pdf.image(os.path.join(temp_path,'student.png') , w=150, h=75)
    os.remove(os.path.join(temp_path,'student.png')) 

def create_worldgraphs(pdf):
    barWidth = 0.25
    plt.subplots(figsize =(10, 5))
    correct = [0,0,0,0,0]
    incorrect = [0,0,0,0,0]
    unattempted = [0,0,0,0,0]
    for k in range(5):
        lst=allstudent[k]['Outcome (Correct/Incorrect/Not Attempted)'].tolist()
        for j in lst:
            if j=='Correct':
                correct[k]+=1
            elif j=='Incorrect':
                incorrect[k]+=1
            else:
                unattempted[k]+=1
    br1 = np.arange(len(correct))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    plt.bar(br1, correct, color ='r', width = barWidth,
        edgecolor ='grey', label ='correct')
    plt.bar(br2, incorrect, color ='g', width = barWidth,
            edgecolor ='grey', label ='incorrect')
    plt.bar(br3, unattempted, color ='b', width = barWidth,
            edgecolor ='grey', label ='unattempted')
    plt.xlabel('All Students Name', fontsize = 15)
    plt.ylabel('Nos Of Questions Answered', fontsize = 15)
    plt.title("World Students Attempts",fontweight ='bold',fontsize = 18)
    plt.xticks([r + barWidth for r in range(len(correct))],['ABC1 XYZ1', 'ABC2 XYZ2', 'ABC3 XYZ3', 'ABC4 XYZ4', 'ABC5 XYZ5'])
    plt.legend()
    plt.savefig(os.path.join(temp_path,'worldstudent.png'))
    pdf.set_xy(30,115)
    pdf.image(os.path.join(temp_path,'worldstudent.png') , w=150, h=75)
    os.remove(os.path.join(temp_path,'worldstudent.png'))

def create_score(pdf):
    ls=allstudents['Your score'].tolist()
    lst=sum(ls)
    pdf.set_xy(10,198)
    pdf.set_font('Arial','',12)
    pdf.cell(1,1,'Maximam Mark For Final Exam Is: 100', border=0)
    pdf.set_xy(10,203)
    pdf.set_font('Arial','',12)
    pdf.cell(1,1,'Mark Scored By The Student Is: '+str(lst)+'/100', border=0)
    pdf.set_xy(10,213)
    pdf.set_font('Arial','B',12)
    pdf.cell(1,1,'Final result: ', border=0)
    pdf.set_xy(35,213)
    pdf.set_font('Arial','',12)
    pdf.cell(1,1,(allstudents.iloc[0]['Final result']), border=0)

def create_footer(pdf):
    pdf.set_xy(10,223)
    pdf.set_font('Arial','B',12)
    pdf.cell(1,1,'Any Questions or Comments :', border=0)
    pdf.set_xy(10,227)
    pdf.cell(190,30,' ', border=1)
    pdf.set_xy(10,263)
    pdf.set_font('Arial','B',12)
    pdf.cell(1,1,'Teacher Signature', border=0)
    pdf.set_xy(160,263)
    pdf.set_font('Arial','B',12)
    pdf.cell(1,1,'Parents Signature', border=0)
    pdf.set_xy(185,275)
    pdf.set_font('Arial','',8)
    pdf.cell(1,1,'Page 2 of 2', border=0)

data=pd.read_excel(os.path.join(BASE_DIR,'Dummy Data.xlsx'),header=1)  # Dummy Data.xlsx file as a input
allstudent=[]
for i in range(1,6):
    j =data[data.iloc[:,0] == i]
    allstudents=j
    if i==1:
        for l in range(1,6):
            l =data[data.iloc[:,0] == l]
            allstudent.append(l)
    pdf=FPDF() #class of  FPDF
    pdf.add_page()
    create_margin(pdf)
    create_logo(pdf)
    create_studentpic(pdf)
    create_studentinfo(pdf)
    create_table(pdf)
    pdf.add_page()
    create_margin(pdf)
    create_logo(pdf)
    create_studentgraphs(pdf)
    create_worldgraphs(pdf)
    create_score(pdf)
    create_footer(pdf)
    pdf.output("student"+str(i)+".pdf") 
