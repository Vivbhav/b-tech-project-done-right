import sys
import os
from tkinter import *
import wiki
import script_tag_answer

tk = Tk()
def generate_fill_in_the_blanks(filename):
    fr= open(filename, "r")
    count = 1
    for line in fr:
        print(count,")",end=" ")
        for i in line.strip().split(" "):
            j = i.strip().split("|")
            if j[-1] == 'A':
                print("_"*8,end=" ")
                print("("+j[0]+")",end=" ")
            else:
                print(j[0],end=" ")
        print("\n")
        count += 1

def display(frame=None, geometry = "250x200", label="", buttons_list=[], w=26, back = False, quit = False):
    if not (len(buttons_list) or back or quit):
        return -3
    choice = IntVar()
    destroy_frame = False
    if not frame:
        tk.geometry(geometry)
        frame = Frame()
        frame.pack(anchor=CENTER)
        destroy_frame = True
    Label(frame, text=label,font='none 12 bold').pack()
    i = 0
    buttons = []
    for button in buttons_list:
        buttons.append(Button(frame,text=button, width=w,command=lambda i=i:choice.set(i)))
        buttons[i].pack(fill=X, side=TOP)
        i += 1

    if back:
        buttons.append(Button(frame, text="Back", width=w,command=lambda:choice.set(-1)))
        buttons[-1].pack(fill=X, side=TOP)
    if quit:
        buttons.append(Button(frame, text="QUIT", width=w,command=lambda:choice.set(-2)))
        buttons[-1].pack(fill=X, side=BOTTOM)
    
    buttons[0].wait_variable(choice)
    if destroy_frame:
        frame.destroy()
    return choice.get()


def main():
    tk.title("Question Generation")
    choice = IntVar()
    choice.set(1)
    while choice.get() == 1:
        option = display(label="Choose", buttons_list=["Enter Topic", "Enter Paragraph"], quit=True)
        scrape = 0
        if option < 0 or option > 1:
            return 0
        elif option == 0:
            scrape = 1
        elif option == 1:
            pass

        frame = Frame()
        frame.pack(anchor=CENTER)
        #render text box
        Label(frame, text="Enter Text", bg='black', fg='white', font='none 12 \
                bold').pack(fill=X, side=TOP)
        input_field = Entry(frame, width=10, bg='white')
        input_field.pack(fill=X, side=TOP)
        
        #submit button
        option = display(frame=frame, label="", buttons_list=["Submit"], quit=True, back=True)

        if option != 0 :
            return 0

        text = [input_field.get()]
        #split . if only ner

        frame.destroy()
        filename="input.for.test/new_input.txt"

        file_exists = False
        if(scrape): 
            filename = "input.for.test/"+text[0].replace(" ","_") + ".txt"
            file_exists = os.path.isfile(filename)
            if not file_exists:
                frame = Frame()
                frame.pack(anchor=CENTER)
                Label(frame, text="Fetching data",font='none 12\
                        bold').pack()
                frame.update()
                text = wiki.scrape(text[0])
                frame.destroy()
        #preprocess
        if not file_exists:
            frame = Frame()
            frame.pack(anchor=CENTER)
            Label(frame, text="Preprocessing", bg='black', fg='white', font='none 12 \
                    bold').pack(fill=X, side=TOP)
            frame.update()
            script_tag_answer.preprocess(text, filename)
            frame.destroy()

        option = display(label="Choose Question Type", buttons_list=["Wh Question"\
                    , "Fill in the blanks"], quit=True, back=True)

        if option < 0 or option > 1:
            return 0
        if option == 0:
            os.system("bash qg_reproduce_LS.sh "+filename)
            pass
        elif option == 1:
            generate_fill_in_the_blanks(filename)
    tk.destroy()
    return 0


if __name__ == '__main__':
    main()
