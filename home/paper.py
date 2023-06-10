# importing the necessary libraries
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  
from django.contrib import messages
import random

# defining the function to convert an HTML file to a PDF file
def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def paper_data(request, course, diff_level):

    m={}
    questions={}
    q1 = q2 = q3 = q4 = q5 = 0
    mcq1 = mcq2 = mcq3 = mcq4 = mcq5 = 0
    mcq1_mark = mcq2_mark = mcq3_mark = mcq4_mark = mcq5_mark = 0
    qall1, qall2, qall3, qall4, qall5, q1a, q1b, q2a, q2b, q3a, q3b, q4a, q4b, q5a, q5b = [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    mcqall, mcqall1, mcqall2, mcqall3, mcqall4, mcqall5 = [], [], [], [], [], []
    q_difficulty = []
    total=1
    easy=medium=hard=0
    qd_easy={10: [6,3,1], 11: [6,4,1], 12: [7,4,1], 13: [8,4,1], 14: [8,5,1], 15: [9,5,1], 16: [9,6,1], 17: [10,6,1], 18: [11,6,1], 19: [11,7,1], 20: [12,7,1], 21: [13,7,1]}
    qd_medium={10: [4,5,1], 11: [4,5,2], 12: [5,5,2], 13: [5,6,2], 14: [6,6,2], 15: [6,7,2], 16: [7,7,2], 17: [7,8,2], 18: [7,8,3], 19: [8,8,3], 20: [8,9,3], 21: [8,10,3]}
    qd_hard={10: [2,4,4], 11: [2,4,5], 12: [2,5,5], 13: [3,5,5], 14: [3,6,5], 15: [3,6,6], 16: [3,6,7], 17: [3,7,7], 18: [4,7,7], 19: [4,8,7], 20: [4,8,8], 21: [4,9,8]}
    d1={'Easy': qd_easy, 'Medium': qd_medium, 'Hard': qd_hard}
    d=d1[diff_level]

    modules=course.module_set.all()
    if len(modules)!=5:
        messages.error(request, "Not enough modules")
        return None
    
    for mod in modules:
        m[mod.modno]=mod
        
    def final():
        nonlocal questions, mcqall, q1a, q1b, q2a, q2b, q3a, q3b, q4a, q4b, q5a, q5b
        final_mcq, final_mcq_mark, final_option1, final_option2, final_option3, final_option4 = [], [], [], [], [], []
        final_q1a, final_q1a_mark, final_q1b, final_q1b_mark = [], [], [], []
        final_q2a, final_q2a_mark, final_q2b, final_q2b_mark = [], [], [], []
        final_q3a, final_q3a_mark, final_q3b, final_q3b_mark = [], [], [], []
        final_q4a, final_q4a_mark, final_q4b, final_q4b_mark = [], [], [], []
        final_q5a, final_q5a_mark, final_q5b, final_q5b_mark = [], [], [], []

        for mcq in mcqall:
            final_mcq.append(mcq.question)
            final_mcq_mark.append(mcq.marks)
            final_option1.append(mcq.option1)
            final_option2.append(mcq.option2)
            final_option3.append(mcq.option3)
            final_option4.append(mcq.option4)

        for q in q1a:
            final_q1a.append(q.question)
            final_q1a_mark.append(q.marks)

        for q in q1b:
            final_q1b.append(q.question)
            final_q1b_mark.append(q.marks)

        for q in q2a:
            final_q2a.append(q.question)
            final_q2a_mark.append(q.marks)

        for q in q2b:
            final_q2b.append(q.question)
            final_q2b_mark.append(q.marks)

        for q in q3a:
            final_q3a.append(q.question)
            final_q3a_mark.append(q.marks)

        for q in q3b:
            final_q3b.append(q.question)
            final_q3b_mark.append(q.marks)

        for q in q4a:
            final_q4a.append(q.question)
            final_q4a_mark.append(q.marks)

        for q in q4b:
            final_q4b.append(q.question)
            final_q4b_mark.append(q.marks)

        for q in q5a:
            final_q5a.append(q.question)
            final_q5a_mark.append(q.marks)

        for q in q5b:
            final_q5b.append(q.question)
            final_q5b_mark.append(q.marks)

        questions={
            'mcq': {'question': final_mcq, 'option1':final_option1, 'option2':final_option2, 'option3':final_option3, 'option4':final_option4, 'mark': final_mcq_mark},
            'q1a': {'question': final_q1a, 'mark':final_q1a_mark},
            'q1b': {'question': final_q1b, 'mark':final_q1b_mark},
            'q2a': {'question': final_q2a, 'mark':final_q2a_mark},
            'q2b': {'question': final_q2b, 'mark':final_q2b_mark},
            'q3a': {'question': final_q3a, 'mark':final_q3a_mark},
            'q3b': {'question': final_q3b, 'mark':final_q3b_mark},
            'q4a': {'question': final_q4a, 'mark':final_q4a_mark},
            'q4b': {'question': final_q4b, 'mark':final_q4b_mark},
            'q5a': {'question': final_q5a, 'mark':final_q5a_mark},
            'q5b': {'question': final_q5b, 'mark':final_q5b_mark},
        }

        return questions
       
    def question_set():
        nonlocal q1, q2, q3, q4, q5
        #print(q_difficulty)
        q1=m['1'].question_set.exclude(id__in=qall1).exclude(difficulty__in=q_difficulty)
        q2=m['2'].question_set.exclude(id__in=qall2).exclude(difficulty__in=q_difficulty)
        q3=m['3'].question_set.exclude(id__in=qall3).exclude(difficulty__in=q_difficulty)
        q4=m['4'].question_set.exclude(id__in=qall4).exclude(difficulty__in=q_difficulty)
        q5=m['5'].question_set.exclude(id__in=qall5).exclude(difficulty__in=q_difficulty)

    def mcq_set():
        nonlocal mcq1, mcq2, mcq3, mcq4, mcq5
        mcq1=m['1'].mcq_set.exclude(id__in=mcqall1)
        mcq2=m['2'].mcq_set.exclude(id__in=mcqall2)
        mcq3=m['3'].mcq_set.exclude(id__in=mcqall3)
        mcq4=m['4'].mcq_set.exclude(id__in=mcqall4)
        mcq5=m['5'].mcq_set.exclude(id__in=mcqall5)

    def check():
        s1 = s2 = s3 = s4 = s5 = 0
        if 0<len(q1.exclude(marks=16))<4 or 0<len(q2.exclude(marks=16))<4 or 0<len(q3.exclude(marks=16))<4 or 0<len(q4.exclude(marks=16))<4 or 0<len(q5.exclude(marks=16))<4:
            messages.error(request, "Not enough 8 mark questions")
            return 'error'
        
        if len(q1.filter(difficulty='Easy'))<4 or len(q2.filter(difficulty='Easy'))<4 or len(q3.filter(difficulty='Easy'))<4 or len(q4.filter(difficulty='Easy'))<4 or len(q5.filter(difficulty='Easy'))<4:
            messages.error(request, "Not enough easy questions. There should be a minimum of 4 easy questions in each module.")
            return 'error'
        if len(q1.filter(difficulty='Medium'))<4 or len(q2.filter(difficulty='Medium'))<4 or len(q3.filter(difficulty='Medium'))<4 or len(q4.filter(difficulty='Medium'))<4 or len(q5.filter(difficulty='Medium'))<4:
            messages.error(request, "Not enough medium questions. There should be a minimum of 4 medium questions in each module.")
            return 'error'
        if len(q1.filter(difficulty='Hard'))<4 or len(q2.filter(difficulty='Hard'))<4 or len(q3.filter(difficulty='Hard'))<4 or len(q4.filter(difficulty='Hard'))<4 or len(q5.filter(difficulty='Hard'))<4:
            messages.error(request, "Not enough hard questions. There should be a minimum of 4 hard questions in each module.")
            return 'error'

        for i in q1:
            s1=s1+int(i.marks)

        for j in q2:
            s2=s2+int(j.marks)

        for k in q3:
            s3=s3+int(k.marks)

        for l in q4:
            s4=s4+int(l.marks)

        for m in q5:
            s5=s5+int(m.marks)

        if s1<32 or s2<32 or s3<32 or s4<32 or s5<32:
            messages.error(request, "Not enough questions")
            return 'error'
        
    def mcq_check():
        s1 = s2 = s3 = s4 = s5 = 0
        if 0<len(mcq1.exclude(marks=2))<4 or 0<len(mcq2.exclude(marks=2))<4 or 0<len(mcq3.exclude(marks=2))<4 or 0<len(mcq4.exclude(marks=2))<4 or 0<len(mcq5.exclude(marks=2))<4:
            messages.error(request, "Not enough 1 mark questions")
            return 'error'

        for i in mcq1:
            s1=s1+int(i.marks)

        for j in mcq2:
            s2=s2+int(j.marks)

        for k in mcq3:
            s3=s3+int(k.marks)

        for l in mcq4:
            s4=s4+int(l.marks)

        for m in mcq5:
            s5=s5+int(m.marks)

        if s1<4 or s2<4 or s3<4 or s4<4 or s5<4:
            messages.error(request, "Not enough mcq questions")
            return 'error'

    def select(q, mod, part):
        nonlocal q_difficulty, total, easy, medium, hard
        total+=1

        # if total<=10:
        #     print("Total: ", total, "E: ", d[10][0], "M: ", d[10][1], "D: ", d[10][2])
        # if total>10:
        #     print("Total: ", total, "E: ", d[total][0], "M: ", d[total][1], "D: ", d[total][2])
        # print("Mod: ",mod,"Part: ", part)
        # for i in q:
        #     print(i.difficulty, end=", ")
        # print()

        qt=q[random.randint(0, len(q)-1)]
        # print("Level: ", qt.difficulty)
        # print()
        q_difficulty=[]

        difficulty=qt.difficulty
        if difficulty=='Easy':
            easy+=1
        elif difficulty=='Medium':
            medium+=1
        elif difficulty=='Hard':
            hard+=1

        if total<=10:
            if easy==d[10][0] and medium==d[10][1] and hard==d[10][2]:
                q_difficulty.append('Easy')
                q_difficulty.append('Medium')
                q_difficulty.append('Hard')
            elif easy==d[10][0] and medium==d[10][1]:
                q_difficulty.append('Easy')
                q_difficulty.append('Medium')
            elif easy==d[10][0] and hard==d[10][2]:
                q_difficulty.append('Easy')
                q_difficulty.append('Hard')
            elif medium==d[10][1] and hard==d[10][2]:
                q_difficulty.append('Medium')
                q_difficulty.append('Hard')
            elif easy==d[10][0]:
                q_difficulty.append('Easy')
            elif medium==d[10][1]:
                q_difficulty.append('Medium')
            elif hard==d[10][2]:
                q_difficulty.append('Hard')

        elif total>10 and total<=20:
            if easy==d[total][0] and medium==d[total][1] and hard==d[total][2]:
                q_difficulty.append('Easy')
                q_difficulty.append('Medium')
                q_difficulty.append('Hard')
            elif easy==d[total][0] and medium==d[total][1]:
                q_difficulty.append('Easy')
                q_difficulty.append('Medium')
            elif easy==d[total][0] and hard==d[total][2]:
                q_difficulty.append('Easy')
                q_difficulty.append('Hard')
            elif medium==d[total][1] and hard==d[total][2]:
                q_difficulty.append('Medium')
                q_difficulty.append('Hard')
            elif easy==d[total][0]:
                q_difficulty.append('Easy')
            elif medium==d[total][1]:
                q_difficulty.append('Medium')
            elif hard==d[total][2]:
                q_difficulty.append('Hard')


        if mod==1:
            if part==1:
                qall1.append(qt.id)
                q1a.append(qt)
                if len(q1a)<2:
                    if int(qt.marks)==8:
                        question_set()
                        q1_temp=q1.exclude(marks=16)
                        select(q1_temp, 1, 1)
                    elif int(qt.marks)==16:
                        question_set()
                        select(q1, 1, 2)
                else:
                    question_set()
                    select(q1, 1, 2)
                    
            elif part==2:
                qall1.append(qt.id)
                q1b.append(qt)
                if len(q1b)<2:
                    if int(qt.marks)==8:
                        question_set()
                        q1_temp=q1.exclude(marks=16)
                        select(q1_temp, 1, 2)
                    elif int(qt.marks)==16:
                        question_set()
                        select(q2, 2, 1)
                else:
                    question_set()
                    select(q2, 2, 1)

        elif mod==2:
            if part==1:
                qall2.append(qt.id)
                q2a.append(qt)
                if len(q2a)<2:
                    if int(qt.marks)==8:
                        question_set()
                        q2_temp=q2.exclude(marks=16)
                        select(q2_temp, 2, 1)
                    elif int(qt.marks)==16:
                        question_set()
                        select(q2, 2, 2)
                else:
                    question_set()
                    select(q2, 2, 2)
                    
            elif part==2:
                qall2.append(qt.id)
                q2b.append(qt)
                if len(q2b)<2:
                    if int(qt.marks)==8:
                        question_set()
                        q2_temp=q2.exclude(marks=16)
                        select(q2_temp, 2, 2)
                    elif int(qt.marks)==16:
                        question_set()
                        select(q3, 3, 1)
                else:
                    question_set()
                    select(q3, 3, 1)

        elif mod==3:
            if part==1:
                qall3.append(qt.id)
                q3a.append(qt)
                if len(q3a)<2:
                    if int(qt.marks)==8:
                        question_set()
                        q3_temp=q3.exclude(marks=16)
                        select(q3_temp, 3, 1)
                    elif int(qt.marks)==16:
                        question_set()
                        select(q3, 3, 2)
                else:
                    question_set()
                    select(q3, 3, 2)
                    
            elif part==2:
                qall3.append(qt.id)
                q3b.append(qt)
                if len(q3b)<2:
                    if int(qt.marks)==8:
                        question_set()
                        q3_temp=q3.exclude(marks=16)
                        select(q3_temp, 3, 2)
                    elif int(qt.marks)==16:
                        question_set()
                        select(q4, 4, 1)
                else:
                    question_set()
                    select(q4, 4, 1)

        elif mod==4:
            if part==1:
                qall4.append(qt.id)
                q4a.append(qt)
                if len(q4a)<2:
                    if int(qt.marks)==8:
                        question_set()
                        q4_temp=q4.exclude(marks=16)
                        select(q4_temp, 4, 1)
                    elif int(qt.marks)==16:
                        question_set()
                        select(q4, 4, 2)
                else:
                    question_set()
                    select(q4, 4, 2)
                    
            elif part==2:
                qall4.append(qt.id)
                q4b.append(qt)
                if len(q4b)<2:
                    if int(qt.marks)==8:
                        question_set()
                        q4_temp=q4.exclude(marks=16)
                        select(q4_temp, 4, 2)
                    elif int(qt.marks)==16:
                        question_set()
                        select(q5, 5, 1)
                else:
                    question_set()
                    select(q5, 5, 1)

        elif mod==5: 
            if part==1:
                qall5.append(qt.id)
                q5a.append(qt)
                if len(q5a)<2:
                    if int(qt.marks)==8:
                        question_set()
                        q5_temp=q5.exclude(marks=16)
                        select(q5_temp, 5, 1)
                    elif int(qt.marks)==16:
                        question_set()
                        select(q5, 5, 2)
                else:
                    question_set()
                    select(q5, 5, 2)
                    
            elif part==2:
                qall5.append(qt.id)
                q5b.append(qt)
                if len(q5b)<2:
                    if int(qt.marks)==8:
                        question_set()
                        q5_temp=q5.exclude(marks=16)
                        select(q5_temp, 5, 2)
                    elif int(qt.marks)==16:
                        question_set()
                        return
                else:
                    question_set()
                    return

    def select_mcq(q, mod):
        nonlocal mcq1_mark, mcq2_mark, mcq3_mark, mcq4_mark, mcq5_mark
        qt=q[random.randint(0, len(q)-1)]
        if mod==1:
            mcqall1.append(qt.id)
            mcqall.append(qt)
            mcq1_mark+=int(qt.marks)

            if mcq1_mark<3:
                mcq_set()
                select_mcq(mcq1, 1)
            elif mcq1_mark==3:
                mcq_set()
                mcq1_temp=mcq1.exclude(marks=2)
                select_mcq(mcq1_temp, 1)
            elif mcq1_mark==4:
                mcq_set()
                select_mcq(mcq2, 2)

        elif mod==2:
            mcqall2.append(qt.id)
            mcqall.append(qt)
            mcq2_mark+=int(qt.marks)

            if mcq2_mark<3:
                mcq_set()
                select_mcq(mcq2, 2)
            elif mcq2_mark==3:
                mcq_set()
                mcq2_temp=mcq2.exclude(marks=2)
                select_mcq(mcq2_temp, 2)
            elif mcq2_mark==4:
                mcq_set()
                select_mcq(mcq3, 3)

        elif mod==3:
            mcqall3.append(qt.id)
            mcqall.append(qt)
            mcq3_mark+=int(qt.marks)

            if mcq3_mark<3:
                mcq_set()
                select_mcq(mcq3, 3)
            elif mcq3_mark==3:
                mcq_set()
                mcq3_temp=mcq3.exclude(marks=2)
                select_mcq(mcq3_temp, 3)
            elif mcq3_mark==4:
                mcq_set()
                select_mcq(mcq4, 4)

        elif mod==4:
            mcqall4.append(qt.id)
            mcqall.append(qt)
            mcq4_mark+=int(qt.marks)

            if mcq4_mark<3:
                mcq_set()
                select_mcq(mcq4, 4)
            elif mcq4_mark==3:
                mcq_set()
                mcq4_temp=mcq4.exclude(marks=2)
                select_mcq(mcq4_temp, 4)
            elif mcq4_mark==4:
                mcq_set()
                select_mcq(mcq5, 5)

        elif mod==5:
            mcqall5.append(qt.id)
            mcqall.append(qt)
            mcq5_mark+=int(qt.marks)

            if mcq5_mark<3:
                mcq_set()
                select_mcq(mcq5, 5)
            elif mcq5_mark==3:
                mcq_set()
                mcq5_temp=mcq5.exclude(marks=2)
                select_mcq(mcq5_temp, 5)
            elif mcq5_mark==4:
                mcq_set()
                return
               
    
    question_set()
    mcq_set()

    if check() == 'error':
        return None

    if mcq_check() == 'error':
        return None
    
    select(q1, 1, 1)
    select_mcq(mcq1, 1)

    return final()

    
                            