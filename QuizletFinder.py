from googlesearch import search 
import pyautogui
import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate
from tkinter import messagebox
from tkinter import * 
import tkinter as tk

def quit():
	global root
	root.quit()

def write_slogan():
	print("Tkinter is easy to use!")



class possibleAnswer:
	def __init__(self,title, url, question,answer):

		self.url = url
		self.question = question
		self.answer = answer
		self.title = title
	def myfunc(self):
		return {self.title,self.url,self.question,self.answer}
	def formatData(self):
		formattedResult = f"Quiz Title: {self.title}\n\n URL: {self.url} \n\n Question: {self.question} \n\n Answer: {self.answer} "
		return formattedResult


def convert(lst): 
	  
	return ' '.join(lst) 


def getAnswer(pageUrl,question):
	#print(pageUrl)
	page = requests.get(pageUrl)
	soup = BeautifulSoup(page.text, 'html.parser')
	try:
		title = soup.find(class_="UIHeading UIHeading--one").text
		questionText =soup.find(string=re.compile(question, flags=re.I))
		termList = soup.find(class_='SetPageTerm')
		answerList = termList.find_all('SetPageTerm-wordText')
		termWhole= questionText.parent.parent.parent.parent.parent
		answerGroup = termWhole.find(class_='SetPageTerm-definitionText')
		answerCode= answerGroup.find(class_='TermText')
		answer = answerGroup.find_all(text=True)
		answer = ' '.join(map(str, answer)) 
		result = possibleAnswer(title, pageUrl, question,answer)
		return result
	except:
		print("Answer can not be found on quizlet")
				

  # always returns "OK"

	#print(questionText)
def combine_funcs(*funcs):
	def combined_func(*args, **kwargs):
		for f in funcs:
			f(*args, **kwargs)
	return combined_func
	
def askQuestion():
	window_height = 80
	window_width = 500

	
	root=Tk()
	root.title("Quizlet Answer Finder")
	root.resizable(True, True) 
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
		
	x_cordinate = int((screen_width/2) - (window_width/2))
	y_cordinate = int((screen_height/2) - (window_height/2))
	
	def retrieve_input():
		inputValue=textBox.get("1.0","end-1c")
		findAnswers(inputValue)

	textBox=Text(root, height=3, width=120)
	
	textBox.pack()
	buttonCommit=Button(root, height=1, width=10, text="Submit", 
						command=combine_funcs(lambda: retrieve_input(), quit ))

	buttonCommit.pack()
	
	root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

	mainloop()	



def findAnswers(question):
	if not question:
		messagebox.showinfo("Error", "Please enter a question or press quit")
		askQuestion()
		
	window_height = 500
	window_width = 900
	query = "\"{}\"".format(question) + " site:quizlet.com"
	#print(query)




	possibleAnswers = []

	for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
		result = getAnswer(j,question)
		#print(result.myfunc())
		if result:
			possibleAnswers.append(result)
	#print (possibleAnswers)
	tables= []
	for answers in possibleAnswers:
		index = possibleAnswers.index(answers)+1
		tables.append(f"Result {index} \n\n"+answers.formatData()+"\n\n\n\n")

	tables = ' '.join(map(str, tables)) 

	
	root = tk.Tk()
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
		
	x_cordinate = int((screen_width/2) - (window_width/2))
	y_cordinate = int((screen_height/2) - (window_height/2))
	frame = tk.Frame(root)
	root.title("Possible Answers")
	root.resizable(True, True) 

	frame.pack()
	bottomFrame = Frame(root)
	bottomFrame.pack(side=BOTTOM)
	text = tk.Text(root, height=250, width=150)
	text.pack(side=tk.LEFT)
	text.insert(tk.END, tables)
	button = tk.Button(bottomFrame, 
					   text="QUIT", 
					   fg="red",
					   command=quit)
	button.pack(side=tk.LEFT)
	slogan = tk.Button(bottomFrame,
					   text="New Question",
					   command=combine_funcs(root.destroy, askQuestion))
	slogan.pack(side=tk.RIGHT)
	root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


	root.mainloop()


askQuestion()