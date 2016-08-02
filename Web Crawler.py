import requests
from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup

def spider(search):

    #Delete last printed on screen
    output.delete(0, END)

    url = "http://cyro.se/search.php?dayq="

    #Search input
    url = url + search
    trimmed_url = str.replace(url, " ", "+")
    print("\n")

    # Fetching data from the server
    source_code = requests.get(trimmed_url)
    plain_text = source_code.text
    bs = BeautifulSoup(plain_text, "html.parser")
    data = bs.findAll('div', {'class': "imgWrap"})

    for div in data:
        link = div.find('a')
        print(len(link))
        value = "http://cyro.se/" + link['href']
        pv = link['href']
        cpv = pv[11:]
        print(cpv.replace("-", " "))
        cpv_print=cpv.replace("-", " ")
        print_value(cpv_print)
        get_data_from_website(value)

def get_data_from_website(item_url):

    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    #print(len(soup.findAll('a', {'id': 'tmg'})))
    for item in soup.findAll('a', {'id': 'tmg'}):
        href = item.get('href')
        print(href + "\n")
        print_value(href)

#Printing the value on Screen
def print_value(item):
    output.insert(END, item)
    output.insert(END, " ")
    return

def clickCopy(event):
    widget = event.widget
    selection = widget.curselection()
    print("selection:", selection)
    value = widget.get(selection[0])
    print ("value:", value)
    root.clipboard_clear()  # clear clipboard contents
    root.clipboard_append(value)  # append new value to clipbaord

#Passing value to the spider
def pass_value(*args):
    text=value.get()
    spider(text)

#Application layout design
def application_layout():
    global root
    root = Tk()
    root.iconbitmap(default='ico.ico')
    root.config(height=425, width=630)
    root.title('WC : TV Series & Movies')
    # root.resizable(False, False)

    global value,output
    value= StringVar()

    ttk.Label(root,font=("Minion Pro", 18),text='Search for latest TV Series & Movies').place(x=140, y=20)

    entrybox=ttk.Entry(root, width=70, textvariable=value)
    entrybox.focus()
    entrybox.bind("<Return>", pass_value)
    entrybox.place(x=50, y=80)

    buttonSearch = ttk.Button(root,width=15, text='Search',command=pass_value)
    buttonSearch.place(y=78,x=480)

    output=Listbox(root,width=615,height=1000)
    output.place(x=-2,y=150)
    output.bind("<<ListboxSelect>>", clickCopy)
    output.insert(END, " ")
    output.insert(END, "                                                                       Crawling the web may take some time")

    root.mainloop()

#Running the main application
application_layout()



