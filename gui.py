import sys
import os
from tkinter import *
import wiki
import script_tag_answer

tk = Tk()
def generate_fill_in_the_blanks(filename):
    fr= open(filename, "r")
    for line in fr:
    	count = 0
    	line = [word.split("|") for word in line.strip().split(" ")]
    	for i in line:
    		if i[-1] == "A":
    			count += 1
    	if count:
    		for i in line:
    			if i[-1] == 'A':
    		    		print("_"*8,end=" ")
    		    		print("("+i[0]+")",end=" ")
    			else:
    		    		print(i[0],end=" ")
    		print("\n")

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
        display(frame=frame, label="", buttons_list=["Submit"], quit=True, back=True)

        text = [input_field.get()]
        #split . if only ner

        #print(text)
        frame.destroy()
        filename="input.txt"

        if(scrape): 
        	text = wiki.scrape(text[0])
        	#preprocess
        script_tag_answer.preprocess(text, filename)

        print("preprocessing done")
        option = display(label="Choose Question Type", buttons_list=["Wh Question"\
                    , "Fill in the blanks"], quit=True, back=True)

        if option < 0 or option > 1:
            return 0
        if option == 0:
            #generate_question(file)
            pass
        elif option == 1:
            generate_fill_in_the_blanks(filename)
        tk.destroy()
        return 0 
    tk.destroy()


if __name__ == '__main__':
    main()
