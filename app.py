from flask import Flask, render_template, url_for, flash, redirect, json, request, jsonify
from forms import *
import database.db_connector as db


app = Flask(__name__)

app.config['SECRET_KEY'] = '276ed92195282973'  # secret key to protect against modifying cookies, cross site attacks, etc.


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/patients", methods=['GET', 'POST'])
def patients():
    db_connection = db.connect_to_database()
    form = PatientForm()
    find = PatientSearch()
    
    form.addressID.choices = [choice["addressID"] for choice in db.execute_query(db_connection=db_connection, query="SELECT addressID FROM Addresses;").fetchall()]
    find.findAddressID.choices = [choice["addressID"] for choice in db.execute_query(db_connection=db_connection, query="SELECT addressID FROM Addresses;").fetchall()]
    find.findAddressID.choices.insert(0, "")
    
    query = "SELECT * FROM Patients;"

    if find.search.data and find.validate():
        query = 'SELECT * FROM Patients WHERE'
        if find.findPatientID.data:
            query = query + ' patientID = ' + find.findPatientID.data + ' AND'
        if find.findFirstName.data:
            query = query + ' firstName = ' + "'" + find.findFirstName.data + "'" + ' AND'
        if find.findLastName.data:
            query = query + ' lastName = ' + "'" + find.findLastName.data + "'" + ' AND'
        if find.findPhoneNumber.data:
            query = query + ' phoneNumber = ' + "'" + find.findPhoneNumber.data + "'" + ' AND'
        if find.findAddressID.data:
            query = query + ' addressID = ' + find.findAddressID.data + ' AND'
        if find.findBirthDate.data:
            date = str(find.findBirthDate.data)
            query = query + ' birthDate = ' + "'" + date + "'" + ' AND'
        if query == 'SELECT * FROM Patients WHERE':
            query = 'SELECT * FROM Patients;'
        else:
            query = query[0:-4] + ';'

    elif form.submit.data and form.validate():
        insert_query = 'INSERT INTO Patients (firstName, lastName, phoneNumber, addressID, birthDate) VALUES (%s, %s, %s, %s, %s);'
        if form.addressID.data == '':
            form.addressID.data = None
        data = (form.firstName.data, form.lastName.data, form.phoneNumber.data, form.addressID.data, form.birthDate.data)
        try:
            db.execute_query(db_connection=db_connection, query=insert_query, query_params=data)
        except:
            flash('ERROR IN SUBMITTING PATIENT - MAKE SURE ADDRESS ID EXISTS', 'danger')
    
    result = db.execute_query(db_connection=db_connection, query=query).fetchall()
    return render_template("patients.html", title="Patients", form=form, find=find, rows=result, urlroot=request.url_root)

@app.route("/update_patient/<int:id>", methods=['GET', 'POST'])
def update_patient(id):
    db_connection = db.connect_to_database()
    form = PatientForm()
    form.addressID.choices = [choice["addressID"] for choice in db.execute_query(db_connection=db_connection, query="SELECT addressID FROM Addresses;").fetchall()]
    update_query = 'UPDATE Patients SET firstName = %s, lastName = %s, phoneNumber = %s, addressID = %s, birthDate = %s ' \
        'WHERE patientID = %s;'
    select_query = 'SELECT patientID, firstName, lastName, phoneNumber, addressID, birthDate ' \
            'FROM Patients WHERE patientID = %s;' % id

    if form.validate_on_submit():
        if form.addressID.data == '':
            form.addressID.data = None
        data = (form.firstName.data, form.lastName.data, form.phoneNumber.data,
                form.addressID.data, form.birthDate.data, id)
        db.execute_query(db_connection=db_connection, query=update_query, query_params=data)
        flash('UPDATE SUCESSFUL!', 'success')
        return redirect(url_for('patients'))

    result = db.execute_query(db_connection=db_connection, query=select_query).fetchone()

    if result == None:
        return render_template('update_patient.html', title='PATIENT NOT FOUND', form=form, data=result)

    return render_template('update_patient.html', title='Update Patient', form=form, data=result)


@app.route("/delete_patient/<int:id>", methods=['GET', 'POST'])
def delete_patient(id):
    db_connection = db.connect_to_database()
    patient_query = 'DELETE FROM Patients WHERE patientID = %s;' % id
    prescription_query = 'DELETE FROM Prescriptions WHERE patientID = %s;' % id
    hcppt_query = 'DELETE FROM Patients_Providers WHERE patientID = %s;' % id

    db.execute_query(db_connection=db_connection , query=prescription_query)
    db.execute_query(db_connection=db_connection , query=hcppt_query)
    db.execute_query(db_connection=db_connection, query=patient_query)
    flash('PATIENT DELETED!', 'success')

    return redirect(url_for('patients'))

@app.route("/delete_address", methods=['POST'])
def delete_address():
    """
    Handles Delete Address Post requests from client side to the DB
    """
    db_connection = db.connect_to_database()

    # id of row to be deleted and Query creation
    currID = request.form['id']
    delete_query = "DELETE FROM Addresses WHERE addressID = " + currID + ";"

    # tries to execute query, returns 1 for success and flashes success message on reload
    try:
        db.execute_query(db_connection=db_connection, query=delete_query)
        flash("Address Deleted Successfully", "success")
        success = 1
    except:
        # flashes failure message on reload
        flash("Address Deletion Failed. Please ensure there are no patients tied to this address.", "danger")
        success = 0
    return jsonify(success)


@app.route("/update_address", methods=['POST'])
def update_address():
    """
    Handles Delete Address Post requests from client side to the DB
    """
    db_connection = db.connect_to_database()

    # gets values to be sent via update query
    currID = request.form['id']
    currAddr1 = request.form['line1']
    currAddr2 = request.form['line2']
    currCity = request.form['city']
    currState = request.form['state']
    currZip = request.form['zip']

    update_query = ("UPDATE Addresses "
                    "SET address1 = %s, address2 = %s, city = %s, state = %s, zip = %s "
                    "WHERE addressID = %s;")

    # nulls currAddr2 if blank
    if currAddr2 == "":
        currAddr2 = None
    data = (currAddr1, currAddr2, currCity, currState, currZip, currID)

    # updates query execute, flashes success or failure message on reload
    try:
        db.execute_query(db_connection=db_connection, query=update_query, query_params=data)
        flash("Address Updated Successfully", "success")
        success = 1
    except:
        flash("Address Update Failed. Please ensure accurate information was input.", "danger")
        success = 0

    return jsonify(success)

@app.route("/addresses", methods=['GET', 'POST'])
def addresses():
    """
    Handles Address POST and GET requests from client side to the DB
    """
    db_connection = db.connect_to_database()

    # uses wtform for form validation to submit insert query
    form = AddressForm()
    if form.validate_on_submit():
        insert_query = 'INSERT INTO Addresses (address1, address2, city, state, zip) VALUES (%s, %s, %s, %s, %s);'
        if form.address2.data == "":
            form.address2.data = None
        data = (form.address1.data, form.address2.data, form.city.data, form.state.data, form.zipcode.data)
        try:
            db.execute_query(db_connection=db_connection, query=insert_query, query_params=data)
            flash("New Address Added Successfully", "success")
        except:
            flash("New Address Add Failure. Please ensure accurate information was input", "danger")


    # displays table
    display_query = "SELECT * FROM Addresses;"
    try:
        address_result = db.execute_query(db_connection=db_connection, query=display_query).fetchall()
        return render_template("addresses.html", title="Addresses", form=form, rows=address_result)
    except:
        return '<h1>Sorry there was a database error, the connection may need to be restarted. Please contact the admin and reload the page.<h1>'

@app.route("/delete_drug", methods=['POST'])
def delete_drug():
    """
    Handles Delete Drug Post requests from client side to the DB
    """
    db_connection = db.connect_to_database()

    # id of row to be deleted and Query creation
    nationalDrugCode = request.form['ndc']
    delete_query = "DELETE FROM Drugs WHERE nationalDrugCode = '" + nationalDrugCode + "';"

    # tries to execute query, returns 1 for success and flashes success message on reload
    try:
        db.execute_query(db_connection=db_connection, query=delete_query)
        flash("Drug Deleted Successfully", "success")
        success = 1
    except:
        # flashes failure message on reload
        flash("Drug Deletion Failed. Please ensure there are no prescriptions tied to this drug.", "danger")
        success = 0
    return jsonify(success)

@app.route("/update_drug", methods=['POST'])
def update_drug():
    """
    Handles Update Drug Post requests from client side to the DB
    """
    db_connection = db.connect_to_database()

    # gets values to be sent via update query
    nationalDrugCode = request.form['ndc']
    genericName = request.form['gN']
    brandName = request.form['bN']
    strength = request.form['sT']
    quantityAvailable = request.form['qA']

    update_query = ("UPDATE Drugs "
                    "SET genericName = %s, brandName = %s, strength = %s, quantityAvailable = %s "
                    "WHERE nationalDrugCode = %s;")

    data = (genericName, brandName, strength, quantityAvailable, nationalDrugCode)

    # updates query execute, flashes success or failure message on reload
    try:
        db.execute_query(db_connection=db_connection, query=update_query, query_params=data)
        flash("Drug Updated Successfully", "success")
        success = 1
    except:
        flash("Drug Update Failed. Please ensure accurate information was input.", "danger")
        success = 0

    return jsonify(success)

@app.route("/drugs", methods=['GET', 'POST'])
def drugs():
    """
    Handles Drug POST and GET requests from client side to the DB
    """
    db_connection = db.connect_to_database()

    # uses wtform for form validation to submit insert query
    form = DrugForm()
    if form.validate_on_submit():
        insert_query = 'INSERT INTO Drugs (nationalDrugCode, genericName, brandName, strength, quantityAvailable) VALUES (%s, %s, %s, %s, %s);'
        data = (form.nationalDrugCode.data, form.genericName.data, form.brandName.data, form.strength.data, form.quantityAvailable.data)
        try:
            db.execute_query(db_connection=db_connection, query=insert_query, query_params=data)
            flash("New Drug Added Successfully", "success")
        except:
            flash("New Drug Add Failure. Please ensure a duplicate NDC was not entered.", "danger")

    # displays table
    display_query = "SELECT * FROM Drugs;"
    try:
        drug_result = db.execute_query(db_connection=db_connection, query=display_query).fetchall()
        return render_template("drugs.html", title="Drugs", form=form, rows=drug_result)
    except:
        return '<h1>Sorry there was a database error, the connection may need to be restarted. Please contact the admin and reload the page.<h1>'

@app.route("/delete_prescription", methods=['POST'])
def delete_prescription():
    """
    Handles Delete Prescription Post requests from client side to the DB
    """
    db_connection = db.connect_to_database()

    # id of row to be deleted and Query creation
    scriptID = request.form['sid']
    delete_query = "DELETE FROM Prescriptions WHERE scriptID = " + scriptID + ";"

    # tries to execute query, returns 1 for success and flashes success message on reload
    try:
        db.execute_query(db_connection=db_connection, query=delete_query)
        flash("Prescription Deleted Successfully", "success")
        success = 1
    except:
        # flashes failure message on reload
        flash("Prescription Deletion Failed. Please ensure there is no foreign key constraints to this row.", "danger")
        success = 0
    return jsonify(success)

@app.route("/update_prescription", methods=['POST'])
def update_prescription():
    """
    Handles Update Drug Post requests from client side to the DB
    """
    db_connection = db.connect_to_database()

    # gets values to be sent via update query
    scriptID = request.form['sid']
    scriptDate = request.form['sD']
    if scriptDate == "":
        scriptDate = None
    scriptPID = request.form['sPID']
    scriptNDC = request.form['sNDC']
    scriptNPI = request.form['sNPI']

    update_query = ("UPDATE Prescriptions "
                    "SET shipDate = %s, patientID = %s, nationalDrugCode = %s, nationalProviderIdentifier = %s "
                    "WHERE scriptID = %s;")

    data = (scriptDate, scriptPID, scriptNDC, scriptNPI, scriptID)

    # updates query execute, flashes success or failure message on reload
    try:
        db.execute_query(db_connection=db_connection, query=update_query, query_params=data)
        flash("Prescription Updated Successfully", "success")
        success = 1
    except:
        flash("Prescription Update Failed. Please ensure accurate information was input.", "danger")
        success = 0

    return jsonify(success)

@app.route("/prescriptions", methods=['GET', 'POST'])
def prescriptions():
    """
    Handles Prescriptions POST and GET requests from client side to the DB
    """
    db_connection = db.connect_to_database()
    form = PrescriptionForm()
    form.patientID.choices = [choice["patientID"] for choice in db.execute_query(db_connection=db_connection, query="SELECT patientID FROM Patients;").fetchall()]
    form.nationalProviderIdentifier.choices = [choice["nationalProviderIdentifier"] for choice in db.execute_query(db_connection=db_connection, query="SELECT nationalProviderIdentifier FROM Healthcare_Providers;").fetchall()]
    form.nationalDrugCode.choices = [choice["nationalDrugCode"] for choice in db.execute_query(db_connection=db_connection, query="SELECT nationalDrugCode FROM Drugs;").fetchall()]
    

    if form.validate_on_submit():
        insert_query = 'INSERT INTO Prescriptions (shipDate, patientID, nationalDrugCode, nationalProviderIdentifier) VALUES (%s, %s, %s, %s);'
        if form.shipDate.data == "":
            form.shipDate.data = None
        data = (form.shipDate.data, form.patientID.data, form.nationalDrugCode.data, form.nationalProviderIdentifier.data)
        try:
            db.execute_query(db_connection=db_connection, query=insert_query, query_params=data)
            flash("New Prescription Added Successfully", "success")
        except:
            flash("New Prescription Add Failure", "danger")

    # display table
    display_query = "SELECT * FROM Prescriptions;"
    expand_query = ("SELECT Prescriptions.scriptID, Prescriptions.shipDate, Patients.patientID, Patients.firstName, Patients.lastName, Healthcare_Providers.nationalProviderIdentifier, "+
                    "Healthcare_Providers.firstName AS prfirstName, Healthcare_Providers.lastName AS prlastName, Healthcare_Providers.specialty, Drugs.genericName, Drugs.brandName, Drugs.strength "+
                    "FROM Prescriptions "+
                    "LEFT JOIN Patients "+
                    "ON Prescriptions.patientID = Patients.patientID "+
                    "LEFT JOIN Healthcare_Providers "+
                    "ON Prescriptions.nationalProviderIdentifier = Healthcare_Providers.nationalProviderIdentifier "+
                    "LEFT JOIN Drugs "+
                    "ON Prescriptions.nationalDrugCode = Drugs.nationalDrugCode;")
    try:
        prescription_result = db.execute_query(db_connection=db_connection, query=display_query).fetchall()
        expand_result = db.execute_query(db_connection=db_connection, query=expand_query).fetchall()
        return render_template("prescriptions.html", title="Prescriptions", form=form, rows=prescription_result, expand_rows=expand_result)
    except:
        return '<h1>Sorry there was a database error, the connection may need to be restarted. Please contact the admin and reload the page.<h1>'

@app.route("/hcp", methods=['GET', 'POST'])
def providers():
    db_connection = db.connect_to_database()
    form = ProviderForm()
    if form.validate_on_submit():
        insert_query = 'INSERT INTO Healthcare_Providers (nationalProviderIdentifier, firstName, lastName, specialty) VALUES (%s, %s, %s, %s);'
        try:
            data = (form.nationalProviderIdentifier.data, form.firstName.data, form.lastName.data, form.specialty.data)
            db.execute_query(db_connection=db_connection, query=insert_query, query_params=data)
            flash("New Prescriber Added Successfully", "success")
        except:
            flash("New Presciber Add Failure, ensure NPI is not a duplicate.", "danger")
    query = "SELECT * FROM Healthcare_Providers;"
    result = db.execute_query(db_connection=db_connection, query=query).fetchall()
    return render_template("providers.html", title="Healthcare Providers", form=form, rows=result, urlroot=request.url_root)


@app.route("/update_provider/<string:id>", methods=['GET', 'POST'])
def update_provider(id):

    db_connection = db.connect_to_database()
    form = ProviderForm()
    update_query = 'UPDATE Healthcare_Providers SET nationalProviderIdentifier = %s, firstName = %s, lastName = %s, specialty = %s WHERE nationalProviderIdentifier = %s;'
    select_query = 'SELECT nationalProviderIdentifier, firstName, lastName, specialty FROM Healthcare_Providers WHERE nationalProviderIdentifier = %s;' % id

    if form.validate_on_submit():
        data = (form.nationalProviderIdentifier.data, form.firstName.data, form.lastName.data, form.specialty.data)
        db.execute_query(db_connection=db_connection, query=update_query, query_params=data)
        flash('UPDATE SUCESSFUL!')
        return redirect(url_for('providers'))

    result = db.execute_query(db_connection=db_connection, query=select_query).fetchone()

    if result == None:
        return render_template('update_provider.html', title='PATIENT NOT FOUND', form=form, data=result)

    return render_template('update_provider.html', title='Update Provider', form=form, data=result)


@app.route("/delete_provider/<string:id>", methods=['GET', 'POST'])
def delete_provider(id):

    db_connection = db.connect_to_database()
    provider_query = 'DELETE FROM Healthcare_Providers WHERE nationalProviderIdentifier = "%s";' % id
    prescription_query = 'DELETE FROM Prescriptions WHERE nationalProviderIdentifier = "%s";' % id
    hcppt_query = 'DELETE FROM Patients_Providers WHERE nationalProviderIdentifier = "%s";' % id

    db.execute_query(db_connection=db_connection , query=hcppt_query)
    db.execute_query(db_connection=db_connection, query=prescription_query)
    db.execute_query(db_connection=db_connection, query=provider_query)
    flash('PROVIDER DELETED!', 'success')

    return redirect(url_for('providers'))


@app.route("/hcppt", methods=['GET', 'POST'])
def hcp_pt():

    db_connection = db.connect_to_database()
    form = PatientProviderForm()
    form.patientID.choices = [choice["patientID"] for choice in db.execute_query(db_connection=db_connection, query="SELECT patientID FROM Patients;").fetchall()]
    form.nationalProviderIdentifier.choices = [choice["nationalProviderIdentifier"] for choice in db.execute_query(db_connection=db_connection, query="SELECT nationalProviderIdentifier FROM Healthcare_Providers;").fetchall()]
    if form.validate_on_submit():
        npi = form.nationalProviderIdentifier.data
        patient_id = form.patientID.data
        insert_query = 'INSERT INTO Patients_Providers (nationalProviderIdentifier, patientID) VALUES (%s, %s);'
        data = (form.nationalProviderIdentifier.data, form.patientID.data)
        try:
            db.execute_query(db_connection=db_connection, query=insert_query, query_params=data)
        except:
            flash('PATIENT AND/OR PROVIDER DO NOT EXIST, OR THIS IS A DUPLICATE ENTRY', 'danger')

    query = 'SELECT Patients_Providers.patientID, Patients_Providers.nationalProviderIdentifier, Patients.firstName as ptFirstName, Patients.lastName as ptLastName, \
    Healthcare_Providers.FirstName as hcpFirstName, Healthcare_Providers.LastName as hcpLastName \
    FROM Patients_Providers \
    LEFT JOIN Patients ON Patients_Providers.patientID = Patients.patientID \
    LEFT JOIN Healthcare_Providers ON Patients_Providers.nationalProviderIdentifier = Healthcare_Providers.nationalProviderIdentifier;'

    result = db.execute_query(db_connection=db_connection, query=query).fetchall()

    return render_template("providerpatient.html", title="Patient Provider Portal", form=form, rows=result, urlroot=request.url_root)


@app.route("/delete_hcppt/<string:npi>/<int:id>", methods=['GET', 'POST'])
def delete_hcppt(npi, id):

    db_connection = db.connect_to_database()
    query = 'DELETE FROM Patients_Providers WHERE nationalProviderIdentifier = %s AND patientID = %s;'
    data = (npi, id)

    db.execute_query(db_connection=db_connection, query=query, query_params=data)

    return redirect(url_for('hcp_pt'))

@app.route("/hcppt/expanded", methods=['GET', 'POST'])
def expand_hcppt():

    db_connection = db.connect_to_database()
    form = ProviderForm()
    query = 'SELECT Patients_Providers.patientID, Patients_Providers.nationalProviderIdentifier, Patients.firstName as ptFirstName, Patients.lastName as ptLastName, Healthcare_Providers.firstName, Healthcare_Providers.lastName, Healthcare_Providers.specialty FROM Patients_Providers LEFT JOIN Patients ON Patients_Providers.patientID = Patients.patientID LEFT JOIN Healthcare_Providers ON Patients_Providers.nationalProviderIdentifier = Healthcare_Providers.nationalProviderIdentifier;'
    result = db.execute_query(db_connection=db_connection, query=query)

    return render_template('providers.html', title='expanded', form=form, rows=result)

if __name__ == "__main__":
    app.run(debug=True)
