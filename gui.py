import copy
import time
from numpy import arange,pi
from methods import Bisection_method, False_position_method, Secant_method, Fixed_point_iteration_method, \
    Newton_raphson_method, Brige_vieta_method
from appJar import gui
from Parsing import Parser
from sympy import *


def showPlot(current_mode,(x,y)):
    if (current_mode == "Fast Mode"):
        axes = app.updatePlot("fast_plot",x,y)
        showLabels("fast_plot",axes)
    elif (current_mode == "Single Step Mode"):
        axes = app.updatePlot("single_step_plot", x,y)
        showLabels("single_step_plot",axes)

fast_tables = []
fast_tables_copy = []
def show_fast_mode_table():
    print(data)
    tables_copy = copy.deepcopy(fast_tables)
    app.openScrollPane("fast_table_pane")
    for table_label in tables_copy:
        app.removeTable(table_label)
        fast_tables.remove(table_label)
    for table_data in data:
        label = "fast_table_" + str(len(fast_tables))
        fast_tables.append(label)
        app.addTable(label,table_data,border="sunken",colspan=2)
        app.setTableWidth(label,700)
    app.stopScrollPane()

last_table_label = ""
step_count = 1
single_step_tables = []
single_step_tables_copy = []
navigation_buttons_exist = False
def show_single_step_mode_table():
    single_step_tables_copy = copy.deepcopy(single_step_tables)
    app.openScrollPane("single_step_table_pane")
    global navigation_buttons_exist
    if not navigation_buttons_exist:
        app.addButton("prev", navigate_steps, 0, 0)
        styleButton("prev")
        app.setButtonStickey("prev", "left")
        app.addButton("next", navigate_steps, 0, 1)
        styleButton("next")
        app.setButtonStickey("next", "right")
        navigation_buttons_exist = True
    for table_label in single_step_tables_copy:
        app.removeTable(table_label)
        single_step_tables.remove(table_label)
    for table_data in data:
        label = "single_step_table_" + str(len(single_step_tables))
        single_step_tables.append(label)
        app.addTable(label,table_data,border="sunken",colspan=2)
        app.setTableWidth(label, 700)
    global last_table_label
    last_table_label = "single_step_table_" + str(len(single_step_tables)-1)
    app.deleteAllTableRows(last_table_label)
    global step_count
    step_count = 1
    app.stopScrollPane()
    print("singlestepmode")

def navigate_steps(button):
    global step_count
    global last_table_label
    if button == "next":
        if step_count >= len(data[len(data) - 1]):
            pass
        else:
            print(data[len(data)-1][step_count])
            app.addTableRow(last_table_label, data[len(data)-1][step_count])
            step_count += 1
    if button == "prev":
        if step_count <= 1:
            pass
        else:
            print (step_count-2)
            app.deleteTableRow(last_table_label ,step_count-2)
            step_count -= 1


def get_plot_xy():
    x = arange(-3.14, 3.14, 0.05)
    y = x
    return x,y

def showLabels(plot_label, axes):
    axes.legend(['The curve'])
    axes.set_xlabel("X Axes")
    axes.set_ylabel("Y Axes")
    app.refreshPlot(plot_label)

def styleButton(btn):
    app.setButtonBg(btn, "#337ab7")
    app.setButtonFg(btn, "white")
    app.setButtonCursor(btn,"hand2")
    app.setButtonRelief(btn,"groove")

# TODO: read the file then fill the entries
def readFile():
    print("read File")


def checkParameters(method, params):
    error_message = "you must specify the following:\n"
    error = False
    for key in list(params.keys()):
        if (key == "fileEntry"):
            continue
        elif (key == "Second Initial Guess" and (method=="Fixed Point" or method == "Newton-Raphson" or method =="Bierge Vieta")):
            continue
        elif (key == "f(x)=" and params[key] == ""):
            error = True
            error_message += "Function\n"
        elif (params[key] == None):
            error = True
            error_message += key + "\n"

    if (error):
        app.errorBox("Empty Entries", error_message)

    if (params["Max Iterations"] < 0):
        app.errorBox("Invalid Parameters", "Max Iterations can't be negative!")

    if (params["Epsilon"] < 0):
        app.errorBox("Invalid Parameters", "Epsilon can't be negative!")

def solve():
    method = app.getOptionBox("Method")
    if(method == None):
        app.errorBox("Invalid Method","You must specify the method")
    else :
        params = app.getAllEntries()
        print(params)  # debugging
        checkParameters(method, params)
        parser = Parser()
        if(parser.set_func(params["f(x)="])):
            func = parser.f()
            first_guess = params["First Initial Guess"]
            second_guess = params["Second Initial Guess"]
            max_iterations = params["Max Iterations"]
            epsilon = params["Epsilon"]
            print(func) #debugging
            if(method == "Bisection"):
                call_func = Bisection_method.BracketingMethod(func, second_guess, first_guess, max_iterations, epsilon)
            elif (method == "False Position"):
                call_func = False_position_method.FalsePosition(func, second_guess, first_guess, max_iterations, epsilon)
            elif (method == "Fixed Point"):
                call_func = Fixed_point_iteration_method.FixedPointIteration(func, first_guess, max_iterations, epsilon)
            elif (method == "Newton-Raphson"):
                call_func = Newton_raphson_method.NewtonRaphson(func, first_guess, max_iterations, epsilon)
            elif(method == "Secant"):
                call_func = Secant_method.Secant(func, second_guess, first_guess, max_iterations, epsilon)
            elif(method == "Bierge Vieta"):
                call_func = Brige_vieta_method.BrigeVeta(func, first_guess, parser.poly_coeffs(), max_iterations, epsilon)
            bool1 = call_func.verify_there_is_a_root()
            print(bool(bool1))  #debugging
            num_of_iterations = call_func.determine_number_of_iterations()
            print(num_of_iterations)    #debugging
            global data
            data, root = call_func.compute_root()
            print(root) #debugging
            app.setLabel("root","root of f(x) = " + str(root))
            app.setLabel("iterations","number of iterations = " + str(num_of_iterations))
            current_mode = app.getTabbedFrameSelectedTab("TabbedFrame")
            showPlot(current_mode,call_func.get_x_y())
            if(current_mode == "Fast Mode"):
                show_fast_mode_table()
            elif(current_mode == "Single Step Mode"):
                show_single_step_mode_table()

        else:
            app.errorBox("Invalid Function","f(x)=" + parser.func + " is an invalid function")

def updateInitialGuesses():
    while (True):
        method = app.getOptionBox("Method")
        if(method=="Bisection" or method=="False Position"):
            secondGuessLabel.config(state = "normal")
            secondGuessEntry.config(state="normal")
            # xl , xu
            app.enableEntryTooltip("Second Initial Guess")
            app.setEntryTooltip("First Initial Guess","Xl")
            app.setEntryTooltip("Second Initial Guess", "Xu")

        elif(method=="Secant"):
            secondGuessLabel.config(state="normal")
            secondGuessEntry.config(state="normal")
            app.enableEntryTooltip("Second Initial Guess")
            # xi , xi+1
            app.setEntryTooltip("First Initial Guess", "Xi")
            app.setEntryTooltip("Second Initial Guess", "Xi+1")
        elif(method=="Fixed Point" or method == "Newton-Raphson" or method =="Bierge Vieta"):
            app.disableEntryTooltip("Second Initial Guess")
            secondGuessLabel.config(state="disabled")
            secondGuessEntry.config(state="disabled")
            # x0
            app.setEntryTooltip("First Initial Guess", "X0")
        time.sleep(0.5)


# setup GUI
app = gui("Root Finder")
#app.setIcon("assets/logo.gif")
app.setBg("#e2edff",override=True)
app.setFont(family="inherit")
#app.setSticky("new")
#app.setStretch("both")
app.setSticky("nesw")
app.setStretch("")

# Function Frame
app.startLabelFrame("Function",0,0)
app.setPadding([10,5])
app.addLabelEntry("f(x)=")
app.addLabel("orLabel","Or")
app.addFileEntry("fileEntry")
app.addButton("Load",readFile)
styleButton("Load")
app.stopLabelFrame()

# Method Frame
app.startLabelFrame("Method",0,1,colspan=2)
app.setPadding([10,5])
app.addLabelOptionBox("Method", ["- Bracketing Methods -", "Bisection", "False Position",
                        "- Open Methods -", "Fixed Point", "Newton-Raphson",
                        "Secant", "- Polynomials -", "Bierge Vieta"],0)
app.addLabelNumericEntry("First Initial Guess",1,0)
firstGuessLabel = app.getLabelWidget("First Initial Guess")
firstGuessEntry = app.getEntryWidget("First Initial Guess")
app.addLabelNumericEntry("Second Initial Guess",1,1)
secondGuessLabel = app.getLabelWidget("Second Initial Guess")
secondGuessEntry = app.getEntryWidget("Second Initial Guess")
app.addLabelNumericEntry("Max Iterations",2,0)
app.setEntry("Max Iterations", 50)
app.addLabelNumericEntry("Epsilon",2,1)
app.setEntry("Epsilon", 0.0001)
app.addButton("Solve",solve)
styleButton("Solve")
app.stopLabelFrame()
app.addLabel("iterations","number of iterations = ?",1,0)
app.setLabelBg("iterations","light blue")
app.addLabel("root","root of f(x) = ?",1,1)
app.setLabelBg("root","light blue")

# Output Frame
app.startTabbedFrame("TabbedFrame",3,0,colspan=2)
# Fast Mode Tab
app.startTab("Fast Mode")
axes = app.addPlot("fast_plot", *get_plot_xy(), row=0, column=0, width=4, height=4)
showLabels("fast_plot", axes)
app.startScrollPane("fast_table_pane",0,1)
app.stopScrollPane()
app.stopTab()

# Single Step Mode Tab
app.startTab("Single Step Mode")
axes = app.addPlot("single_step_plot", *get_plot_xy(), row=0, column=0, width=4, height=4)
showLabels("single_step_plot", axes)
app.startScrollPane("single_step_table_pane",0,1)
app.stopScrollPane()
app.stopTab()
app.stopTabbedFrame()
#app.thread(updateInitialGuesses)

app.go()