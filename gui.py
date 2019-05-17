import sys
import os
from tkinter import *
from tkinter import font
import wiki
import script_tag_answer
import random
import pickle
from multilistbox import MultiListBox

tk = Tk()
helv = font.Font(family='Helvetica', size=16, weight='bold')
helv1 = font.Font(family='Helvetica', size=38, weight='bold')
txt = font.Font(family='Helvetica', size=16)
canvas = Canvas(tk)

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))

def generate_fill_in_the_blanks(filename):
    fr= open(filename, "r")
    count = 1
    questions = []
    for line in fr:
        question = ""
        for i in line.strip().split(" "):
            j = i.strip().split("|")
            if j[-1] == 'A':
                question += "_"*8+" "
            else:
                question += j[0]+" "
        question += "\n"
        questions.append(question)
        count += 1
    return questions

def display_boxes(frame, geometry="1700x1010", label="", texts=[], w=26,
        parallel=True):
    if not len(texts):
        print("No questions sent to display_boxes()")
        exit(0)
    if label != "":
        Label(frame, text=label,font=helv1).pack(pady=20)
    i = 2
    boxes = []
    for t in texts:
        Label(frame, text=t,font=txt,wraplength=1100).grid(sticky=W)
        if not parallel:
            i += 1
        boxes.append(Entry(frame, width=w+2, bg='white',font=txt))
        boxes[-1].grid(row = i, column = 1 if parallel else 0, sticky = E)
        i += 1
    return boxes

def display(frame=None, geometry = "1700x1010", label="", buttons_list=[], w=26,
        back = False, quit = False, k = 0):
    if not (len(buttons_list) or back or quit):
        print("No buttons sent to display()")
        exit(0)
    choice = IntVar()
    destroy_frame = False
    if not frame:
        tk.geometry(geometry)
        frame = Frame()
        frame.pack(anchor=CENTER)
        destroy_frame = True
    if label != "":
        Label(frame, text=label,font=helv1).grid(pady=20)
    i = 0
    buttons = []
    for button in buttons_list:
        buttons.append(Button(frame,text=button, width=w,command=lambda
            i=i:choice.set(i),font=helv,pady=20))
        buttons[-1].grid(row = i+k+2, padx=10,pady=10,column = 0, sticky = "news")
        i += 1

    if back:
        buttons.append(Button(frame, pady=20,font=helv,text="Back", width=w,command=lambda:choice.set(-1)))
        buttons[-1].grid(row = i+k+2, padx=10,pady=10,column = 0, sticky ='news')
        i+=1
    if quit:
        buttons.append(Button(frame, pady=20,font=helv,text="QUIT", width=w,command=lambda:choice.set(-2)))
        buttons[-1].grid(row = i+k+2, padx=10,pady=10,column = 0, sticky ='news')
    
    buttons[0].wait_variable(choice)
    if destroy_frame:
        frame.destroy()
    return choice.get()


def main():
    global tk,canvas,txt,helv,helv1
    tk.title("Question Generation")
    choice = IntVar()
    choice.set(1)
    state = 0
    while choice.get() == 1:
        if state == 0:
            option = display(label="Choose", buttons_list=["Enter Topic", \
                    "Enter Paragraph","Enter File Name"], quit=True)
            scrape = False
            readfile = False
            h = 1
            wt = 28
            textfield_text = "Enter Sentences"
            if option == -2:
                tk.destroy()
                return 0
            elif option == 0:
                textfield_text = "Enter Topic"
                scrape = True
            elif option == 1:
                textfield_text = "Enter Paragraph"
                h = 15
                wt = 58
            elif option == 2:
                textfield_text = "Enter relative filepath"
                readfile = True
            state += 1

        if state == 1:
            frame = Frame()
            frame.pack(anchor=CENTER)
            #render text box
            Label(frame, text=textfield_text, bg='black', fg='white',\
                    font=helv1).grid(pady=20)
            input_field = Text(frame, width=wt, height=h,font=txt,bg='white')
            input_field.grid()
            
            #submit button
            option = display(frame=frame, label="", k=1,buttons_list=["Submit"],quit=True, back=True)

            if option == -2:
                tk.destroy()
                return 0
            elif option == -1:
                state -= 2

            text = [input_field.get('1.0','end-1c')]

            frame.destroy()
            filename_q="input.for.test/new_input.txt"
            filename_a="input.for.test/new_input_a.txt"

            file_exists = False
            if readfile and option != -1:
                text = [l.strip().replace("\n","") for l in
                        open(text[0],"r").readlines()]
            elif scrape and option != -1: 
                filename_q = "input.for.test/"+text[0].replace(" ","_") + ".txt"
                filename_a = "input.for.test/"+text[0].replace(" ","_") + "_a.txt"
                file_exists = os.path.isfile(filename_q)
                if not file_exists:
                    frame = Frame()
                    frame.pack(anchor=CENTER)
                    Label(frame, text="Fetching data",font=helv1).grid(pady=20)
                    frame.update()
                    text = wiki.scrape(text[0])
                    frame.destroy()
            #preprocess
            if not file_exists and option != -1:
                frame = Frame()
                frame.pack(anchor=CENTER)
                Label(frame, text="Preprocessing", bg='black', fg='white',
                        font=helv1,justify=CENTER).grid(pady=20)
                frame.update()
                answers = script_tag_answer.preprocess(text, filename_q)
                pickle.dump(answers,open(filename_a,"wb"))
                frame.destroy()
            else:
                try:
                    answers = pickle.load(open(filename_a,'rb'))
                except:
                    pass
            state += 1

        if state == 2:
            option = display(label="Choose Question Type", buttons_list=["Wh Question"\
                        , "Fill in the blanks","Vocabulary", "All"], quit=True, back=True)

            output_filename = "questions_by_qg-net.txt"
            if option == -2:
                tk.destroy()
                return 0
            elif option == 0:
                os.system("bash qg_reproduce_LS.sh {} \
                        {}".format(filename_q,output_filename))
                questions = [q[:-1] for q in open(output_filename,"r").readlines()[1:]]
                os.system("rm "+output_filename)
            elif option == 1:
                questions = generate_fill_in_the_blanks(filename_q)
            elif option == 2:
                questions = pickle.load(open(filename_q[:-4]+"_syn.txt","rb"))
                answers = pickle.load(open(filename_q[:-4]+"_syn_a.txt","rb"))
                questions += pickle.load(open(filename_q[:-4]+"_ant.txt","rb"))
                answers += pickle.load(open(filename_q[:-4]+"_ant_a.txt","rb"))
            elif option == 3:
                os.system("bash qg_reproduce_LS.sh {} \
                        {}".format(filename_q,output_filename))
                questions = [q[:-1] for q in open(output_filename,"r").readlines()[1:]]
                os.system("rm "+output_filename)
                questions += generate_fill_in_the_blanks(filename_q)
            elif option == -1:
                state -= 2
            state += 1

        if state == 3:
            option = display(label="Now or Later?", buttons_list=["Write test now"\
                        , "Give .txt file"], quit=True, back=True)

            if option == -2:
                tk.destroy()
                return 0
            elif option == 0:
                state += 1
            elif option == 1:
                pass
            elif option == -1:
                state -= 2
            state += 1
        if state == 4:
            frame = Frame()
            frame.pack(anchor=CENTER)
            boxes = display_boxes(frame=frame,texts=["Questions File",\
                "Answers File"], parallel = True)
            option = display(frame=frame,label="", k=3,buttons_list=["Submit"], quit=True, back=True)
            if option == -2:
                tk.destroy()
                return 0
            elif option == 0:
                qf = boxes[0].get()
                qf = qf if qf else "q.txt"
                af = boxes[1].get()
                af = af if af else "a.txt"
                q = open(qf,"w")
                for i in questions:
                    q.write(i)
                q.close()
                a = open(af,"w")
                for i in answers:
                    a.write(i+"\n")
                a.close()
            elif option == -1:
                state -= 3
            frame.destroy()
            state += 2
        if state == 5:
            
            frame = Frame()
            frame.grid()
            qs=[]
            for i in range(len(questions[:10])):
                qs.append(str(i+1)+") "+questions[i])


            #canvas = Canvas(frame, scrollregion=(0,0,1900,900),\
            #        width=1200, height=400)
            #boxes = display_boxes(frame=canvas,texts=questions, parallel =False)
            #scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
            #scrollbar.pack(side=RIGHT,fill=Y)
            #scrollbar.config(command=canvas.yview)
            #canvas.config(yscrollcommand = scrollbar.set)
            #canvas.pack(expand=True,fill=BOTH,anchor="center")
            #canvas.config(scrollregion=canvas.bbox("all"),width=1700,height=950)
            #option = display(frame=canvas,label="",\
            #        k=1+2*len(questions),buttons_list=["Submit"], quit=True, back=True)

            boxes = display_boxes(frame=frame,texts=qs, parallel =True)
            option = display(frame=frame,label="",\
                    k=1+2*len(questions),buttons_list=["Submit"], quit=True)

            if option == -2:
                tk.destroy()
                return 0
            elif option == 0:
                recvd_answers = [box.get() for box in boxes]
                canvas.destroy()
                frame.destroy()
                mlb = MultiListBox(tk, (('No.', 5),('Question',90),('Your Answer', 15),\
                      ('Correct Answer', 15), ('Score', 15)),font=txt)
                mlb.pack(expand=YES, fill=BOTH)
                score = 0
                for i,l,j,k in zip(range(1,1+len(questions)),questions,answers, recvd_answers):
                    if k.lower() == j.lower():
                        mark = 1
                    else:
                        mark = 0
                    score += mark
                    mlb.insert(END,(i,l,k,j,mark))
                mlb.insert(END,('','','','','Total: '+str(score)))
                mlb.insert(END,('','','','','Percentage: '+str(score/len(questions))))
                option = display(label="", buttons_list=["OK"])
                tk.destroy()
                tk = Tk()
                helv = font.Font(family='Helvetica', size=16, weight='bold')
                helv1 = font.Font(family='Helvetica', size=20, weight='bold')
                txt = font.Font(family='Helvetica', size=16)
                tk.title("Question Generation")
            elif option == -1:
                state -= 3
                frame.destroy()
            state += 1
        state = state % 6
    tk.destroy()
    return 0


if __name__ == '__main__':
    main()
