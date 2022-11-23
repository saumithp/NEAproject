import sqlite3 as sql
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

app = Flask(__name__)

#Key will be used for encryption
app.config['SECRET_KEY'] = 'DJHIJHyi872yuhdj342342dddfwf'
Bootstrap(app)


class LoginForm(FlaskForm): #We inherit from FlaskForm which we inported above from flask_wtf
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    #DataRequired validator means field cannot be left blanked



class BudgetForm(FlaskForm):
    budget_input = IntegerField('Budget', validators=[DataRequired(), NumberRange(min=500, max=5000)])
    #Number range sets what numbers are allowed; values shown can be used
class PartsForm(FlaskForm):
    cpu_field = SelectField('cpu_parts', choices=[])
    gpu_field = SelectField('gpu_parts', choices=[])
    mobo_field = SelectField('mobo_parts', choices=[])
    ram_field = SelectField('ram_parts', choices=[])




@app.route('/', methods=['POST', 'GET'])
#This is the root page, i.e. with no file name after the URL
def form():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        with sql.connect("PCParts_db.db") as con: #connecting to our database
            global username_global #this variable has to be global as it is being called in multiple functions

            cursor = con.cursor()

            cursor.execute("SELECT * FROM User WHERE username = '"+ form.username.data + "'")
            #form.username.data is the username the user has inputted on the webpage
            data = cursor.fetchall()
            if len(data) != 0:
                cursor.execute(
                    "SELECT * FROM User WHERE username = '" + form.username.data + "' AND password = '" + form.password.data + "'"
                )
                data = cursor.fetchall()
                if len(data) != 0: #This means there is a record in our database with the same username and password as inputted
                    print("user found")
                    cursor.execute('SELECT * FROM UserSelection WHERE Username = ?', (form.username.data,))
                    selection_exists = cursor.fetchall()
                    if len(selection_exists) != 0:

                        username_global = form.username.data
                        row, row2, row3, row4, row5, row6, row7, row8, total = user_parts_list(cursor)
                        #We are getting all the row variables from the user_parts_list function

                        return render_template('list.html', row=row, row2=row2, row3=row3, row4=row4, row5=row5,
                                               row6=row6, row7=row7, row8=row8, total=total)
                        #This calls the webpage list.html to the page the user is currently on

                    username_global = form.username.data #Setting the global variable to the current username
                    return budget_splitter()
                else:
                    flash('Incorrect password')
                    error_message = "Incorrect password"
                    return render_template('form.html', form=form, message=error_message)
            else:
                cursor.execute("INSERT INTO User (username,password)VALUES(?,?)",
                               (form.username.data, form.password.data))
                con.commit()
                cursor.execute("INSERT INTO UserSelection (Username)VALUES(?)", (form.username.data,))
                con.commit()

                username_global = form.username.data





            username = form.username.data
            return redirect(url_for('budget', username=form.username.data)) #Calls the /budget url


    return render_template('form.html', form=form)



@app.route('/budget', methods=['POST', 'GET']) #Methods are needed to get the user input
def budget():

    # print("In budget") (This was a print statement used for checking my position in the code when error checking)
    budget_input = BudgetForm()
    username_input = str(LoginForm.username)
    global budget_global


    if budget_input.validate_on_submit(): #Once submit has been clicked, this happens

        with sql.connect("PCParts_db.db") as con:
            cursor = con.cursor()


            cursor.execute('UPDATE UserSelection SET Budget = (?) WHERE Username = ?', (budget_input.budget_input.data, username_global,))

            print("I am here")
            con.commit()
            budget_global = budget_input.budget_input.data



        return budget_splitter()


    return render_template('budget.html', form=budget_input)


@app.route('/list')
def budget_splitter():
    #Distributes budgets between all the parts
    user_budget = int(budget_global)
    RAM_price = round(user_budget * 0.07, 2)
    MOBO_price = round(user_budget * 0.15, 2)
    PSU_price = round(user_budget * 0.05, 2)
    Case_price = round(user_budget * 0.07, 2)
    if user_budget < 600:
        CPU_price = round(user_budget * 0.45, 2)
        GPU_price = round(user_budget * 0, 2)
        SSD_price = round(user_budget * 0.1, 2)
        HDD_price = 0
    else:
        CPU_price = round(user_budget * 0.3, 2)
        GPU_price = round(user_budget * 0.3, 2)
        if user_budget < 1000:
            SSD_price = round(user_budget * 0.1, 2)
            HDD_price = 0
        else:
            SSD_price = round(user_budget * 0.07, 2)
            HDD_price = round(user_budget * 0.04, 2)
    list_username = username_global

    with sql.connect("PCParts_db.db") as con:
        cursor = con.cursor()

        if user_budget > 600:
            cursor.execute(
                'UPDATE UserSelection SET CPUCode = (SELECT CPUcode FROM(SELECT CPUcode, MAX(Price) FROM CPU WHERE Price <= ?)) WHERE Username = ?',
                (CPU_price, username_global,)
            )

        else:
            cursor.execute(
                'UPDATE UserSelection SET CPUCode = (SELECT CPUcode FROM(SELECT CPUcode, MAX(Price) FROM CPU WHERE Price <= ? '
                'AND Manufacturer = "Intel")) WHERE Username = ?',
                (CPU_price, username_global,)
            )

        cursor.execute(
            'UPDATE UserSelection SET GPUCode = (SELECT GPUcode FROM(SELECT GPUcode, MAX(Price) FROM GPU WHERE Price <= ?)) WHERE Username = ?',
            (GPU_price, username_global,)
        )

        cursor.execute(
            "SELECT CPUCode FROM UserSelection WHERE Username = ? AND CPUCode LIKE '%Ryzen%'",
            (username_global,)
        )
        CPU_code = cursor.fetchall()

        if len(CPU_code) == 0:

            cursor.execute(
                'UPDATE UserSelection SET RAMCode = (SELECT RAMcode FROM(SELECT RAMcode, MAX(Price) FROM RAM WHERE PRICE <= ?)) WHERE Username = ?',
                           (RAM_price, username_global,)
                )
        else:
            cursor.execute(
                'UPDATE UserSelection SET RAMCode = (SELECT RAMcode FROM(SELECT RAMcode, Speed, MAX(Price) FROM RAM WHERE PRICE <= ? '
                'AND Speed >= 3000)) WHERE Username = ?',
                           (RAM_price, username_global,)
                )

        cursor.execute(
            'UPDATE UserSelection SET MoboCode = (SELECT Mobocode FROM(SELECT Mobocode, MAX(Price) FROM Motherboard '
            'WHERE Socket IN (SELECT Socket FROM CPU WHERE CPUcode = UserSelection.CPUCode) AND PRICE <= ?)) WHERE Username = ?',
                       (MOBO_price, username_global,)
            )

        cursor.execute(
            'UPDATE UserSelection SET SSDCode = (SELECT SSDcode FROM(SELECT SSDcode, MAX(Price) FROM SSD WHERE Price <= ?)) WHERE Username = ?',
            (SSD_price, username_global,)
        )

        cursor.execute(
            'UPDATE UserSelection SET HDDCode = (SELECT HDDcode FROM(SELECT HDDcode, MAX(Price) FROM HDD WHERE Price <= ?)) WHERE Username = ?',
            (HDD_price, username_global,)
        )

        cursor.execute(
            'UPDATE UserSelection SET PSUCode = (SELECT PSUcode FROM(SELECT PSUcode, MAX(Price) FROM PSU WHERE Price <= ?)) WHERE Username = ?',
            (PSU_price, username_global,)
        )

        cursor.execute(
            'UPDATE UserSelection SET CaseCode = (SELECT Casecode FROM(SELECT Casecode, MAX(Price) FROM PCCase WHERE Price <= ?)) WHERE Username = ?',
            (Case_price, username_global,)
        )

        row, row2, row3, row4, row5, row6, row7, row8, total = user_parts_list(cursor)

        return render_template('list.html', row=row, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, row7=row7, row8=row8, total=total)

def user_parts_list(cursor):
    #Since we have cursor as a parameter here, we do not need to connect the database again in this function
    total = 0
    #Defining the variable total to be used later in this function
    cursor.execute(
        'SELECT CPUName, Cores, Threads, Price FROM CPU WHERE CPUcode = (SELECT CPUCode FROM UserSelection WHERE Username = ?)',
        (username_global,)
    )
    row = cursor.fetchall()
    cursor.execute('SELECT Price FROM CPU WHERE CPUcode = (SELECT CPUCode FROM UserSelection WHERE Username = ?)',
        (username_global,))
    cpu_price_input = cursor.fetchall()
    if len(cpu_price_input) != 0: #This is needed as some parts may not be present in certain builds so the code would crash without this
        cpu_price = cpu_price_input[0]
        total += cpu_price[0]


    cursor.execute(
        'SELECT GPUName, Price FROM GPU WHERE GPUcode = (SELECT GPUCode FROM UserSelection WHERE Username = ?)',
        (username_global,)
    )
    row2 = cursor.fetchall()

    cursor.execute('SELECT Price FROM GPU WHERE GPUcode = (SELECT GPUCode FROM UserSelection WHERE Username = ?)',
                   (username_global,))
    gpu_price_input = cursor.fetchall() #There is only 1 value it is fetching as each User only has max 1 of each component stored
    if len(gpu_price_input) != 0:
        gpu_price = gpu_price_input[0]
        total += gpu_price[0]


    cursor.execute(
        'SELECT MoboName, Price FROM Motherboard WHERE Mobocode = (SELECT MoboCode FROM UserSelection WHERE Username = ?)',
        (username_global,)
    )
    row3 = cursor.fetchall()

    cursor.execute('SELECT Price FROM Motherboard WHERE Mobocode = (SELECT MoboCode FROM UserSelection WHERE Username = ?)',
                   (username_global,))
    mobo_price_input = cursor.fetchall()
    if len(mobo_price_input) != 0:
        mobo_price = mobo_price_input[0]
        total += mobo_price[0]


    cursor.execute(
        'SELECT RAMName, Price FROM RAM WHERE RAMcode = (SELECT RAMCode FROM UserSelection WHERE Username = ?)',
        (username_global,)
    )
    row4 = cursor.fetchall()

    cursor.execute('SELECT Price FROM RAM WHERE RAMcode = (SELECT RAMCode FROM UserSelection WHERE Username = ?)',
                   (username_global,))
    ram_price_input = cursor.fetchall()
    if len(ram_price_input) != 0:
        ram_price = ram_price_input[0]
        total += ram_price[0]


    cursor.execute(
        'SELECT SSDName, Price FROM SSD WHERE SSDcode = (SELECT SSDCode FROM UserSelection WHERE Username = ?)',
        (username_global,)
    )
    row5 = cursor.fetchall()

    cursor.execute('SELECT Price FROM SSD WHERE SSDcode = (SELECT SSDCode FROM UserSelection WHERE Username = ?)',
                   (username_global,))
    ssd_price_input = cursor.fetchall()
    if len(ssd_price_input) != 0:
        ssd_price = ssd_price_input[0]
        total += ssd_price[0]


    cursor.execute(
        'SELECT HDDName, Price FROM HDD WHERE HDDcode = (SELECT HDDCode FROM UserSelection WHERE Username = ?)',
        (username_global,)
    )
    row6 = cursor.fetchall()

    cursor.execute('SELECT Price FROM HDD WHERE HDDcode = (SELECT HDDCode FROM UserSelection WHERE Username = ?)',
                   (username_global,))
    hdd_price_input = cursor.fetchall()
    if len(hdd_price_input) != 0:
        hdd_price = hdd_price_input[0]
        total += hdd_price[0]



    cursor.execute(
        'SELECT PSUName, Price FROM PSU WHERE PSUcode = (SELECT PSUCode FROM UserSelection WHERE Username = ?)',
        (username_global,)
    )
    row7 = cursor.fetchall()

    cursor.execute('SELECT Price FROM PSU WHERE PSUcode = (SELECT PSUCode FROM UserSelection WHERE Username = ?)',
                   (username_global,))
    psu_price_input = cursor.fetchall()
    if len(psu_price_input) != 0:
        psu_price = psu_price_input[0]
        total += psu_price[0]

    cursor.execute(
        'SELECT CaseName, Price FROM PCCase WHERE Casecode = (SELECT CaseCode FROM UserSelection WHERE Username = ?)',
        (username_global,)
    )
    row8 = cursor.fetchall()

    cursor.execute('SELECT Price FROM PCCase WHERE Casecode = (SELECT CaseCode FROM UserSelection WHERE Username = ?)',
                   (username_global,))
    case_price_input = cursor.fetchall()
    if len(case_price_input) != 0:
        case_price = case_price_input[0]
        total += case_price[0]
        total = round(total, 2) #We are rounding as python breaks otherwise and shows multiple dp more than it should


    return (row, row2, row3, row4, row5, row6, row7, row8, total)


@app.route('/editlist', methods=['POST', 'GET'])
def edit_list():
    with sql.connect("PCParts_db.db") as con:
        cursor = con.cursor()
    form = PartsForm()


    cursor.execute('SELECT CPUName, Price, Socket FROM CPU ORDER BY Socket, Price DESC')
    opt1 = cursor.fetchall()


    cursor.execute(
        'SELECT GPUName, Price FROM GPU ORDER BY Price DESC')
    opt2 = cursor.fetchall()

    cursor.execute(
        'SELECT MoboName, Price, Socket FROM Motherboard ORDER BY Socket, Price DESC')
    opt3 = cursor.fetchall()

    cursor.execute(
        'SELECT RAMName, Price FROM RAM ORDER BY Price DESC')
    opt4 = cursor.fetchall()


    cpu = request.form.get('cpu_parts') #Getting the data inputted in the combo box called 'cpu_parts'
    gpu = request.form.get('gpu_parts')
    mobo = request.form.get('mobo_parts')
    ram = request.form.get('ram_parts')
    cursor.execute(
        'UPDATE UserSelection SET CPUCode = (SELECT CPUcode FROM(SELECT CPUcode, CPUName FROM CPU WHERE CPUName = ?)) '
        'WHERE Username = ?',  (cpu, username_global,))
    cursor.execute(
        'UPDATE UserSelection SET GPUCode = (SELECT GPUcode FROM(SELECT GPUcode, GPUName FROM GPU WHERE GPUName = ?)) WHERE Username = ?',
        (gpu, username_global,))
    cursor.execute(
        'UPDATE UserSelection SET MoboCode = (SELECT Mobocode FROM(SELECT Mobocode, MoboName FROM Motherboard WHERE MoboName = ?)) WHERE Username = ?',
        (mobo, username_global,))
    cursor.execute(
        'UPDATE UserSelection SET RAMCode = (SELECT RAMcode FROM(SELECT RAMcode, RAMName FROM RAM WHERE RAMName = ?)) WHERE Username = ?',
        (ram, username_global,))
    con.commit() #Commits the updates to the database. Without this it would not update and the code above would be useless


    return render_template('editlist.html', form=form, opt1=opt1, opt2=opt2, opt3=opt3, opt4=opt4)

@app.route('/temp', methods=['POST', 'GET'])
def temp():
    with sql.connect("PCParts_db.db") as con:
        cursor = con.cursor()
    row, row2, row3, row4, row5, row6, row7, row8, total = user_parts_list(cursor)
    #The sole purpose of this function is to render the list.html page
    return render_template('list.html', row=row, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, row7=row7,
                           row8=row8, total=total)

if __name__ == '__main__':
    app.run()
