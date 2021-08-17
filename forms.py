from flask_wtf import FlaskForm 
from datetime import date 
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField  # also from pip install flask-wtf
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, NumberRange, DataRequired, Length, Email, EqualTo, Optional, ValidationError, Regexp # self explanatory validators

def ZipRequired(form, field):
    if len(field.data) != 5 or not field.data.isnumeric():
        raise ValidationError('Please enter a five digit numeric zip code')
        
    
class NoRequiredForm(FlaskForm):
    class Meta:
        def render_field(self, field, render_kw):
            render_kw.setdefault('required', False)
            return super().render_field(field, render_kw)

class AddressForm(NoRequiredForm):
    address1 = StringField('Address', validators=[InputRequired(), Length(max=255)]) # arg1 is namelabel used in html, arg2 is validators
    address2 = StringField('Address Continued', validators=[Length(max=255)])
    city = StringField('City', validators=[InputRequired(), Length(max=255)])
    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
              'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD', 
              'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
              'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
              'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    state = SelectField('State (Abbreviation)', choices=states)
    zipcode = StringField('Zip Code', validators=[InputRequired(), ZipRequired])
    submit = SubmitField('Add')


class DrugForm(NoRequiredForm):
    ndc_regexp = '^[0-9]{5}-[0-9]{4}-[0-9]{1}|^[0-9]{5}-[0-9]{3}-[0-9]{2}|^[0-9]{4}-[0-9]{4}-[0-9]{2}'
    nationalDrugCode = StringField('National Drug Code', validators=[InputRequired(), Regexp(regex=ndc_regexp, message='Please enter a 10 digit numeric NDC in the format 4-4-2, 5-3-2, or 5-4-1')]) # arg1 is namelabel used in html, arg2 is validators
    
    genericName = StringField('Generic Name', validators=[InputRequired(), Length(max=255)])
    brandName = StringField('Brand Name', validators=[InputRequired(), Length(max=255)])
    strength = StringField('Strength', validators=[InputRequired(), Length(max=255)])
    quantityAvailable = IntegerField('Quantity Available', validators=[InputRequired(), NumberRange(min=0, message='Please enter a numerical value greater than 0')])
    submit = SubmitField('Add')

class PrescriptionForm(NoRequiredForm):
    patientID = SelectField('Patient ID')
    shipDate = DateField('Ship Date', validators=[Optional()])
    nationalProviderIdentifier = SelectField('NPI')
    nationalDrugCode = SelectField('NDC')
    submit = SubmitField('Add')

class PatientForm(FlaskForm):
    patientID = StringField('Patient ID')
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    phoneNumber = StringField('Phone Number', validators=[DataRequired()])
    addressID = SelectField('Address ID')
    birthDate = DateField('DOB', validators=[DataRequired()])
    submit = SubmitField('Add')

class PatientSearch(FlaskForm):
    findPatientID = StringField('Patient ID')
    findFirstName = StringField('First Name')
    findLastName = StringField('Last Name')
    findPhoneNumber = StringField('Phone Number')
    findAddressID = SelectField('Address ID')
    findBirthDate = DateField('DOB', validators=[Optional()])
    search = SubmitField('Search')

class ProviderForm(FlaskForm):
    npi_regexp = '^[0-9]{10}'
    nationalProviderIdentifier = StringField('NPI', validators=[DataRequired(), Regexp(regex=npi_regexp, message='Please enter a 10 digit numeric NPI')])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    specialty = StringField('Specialty', validators=[DataRequired()])
    submit = SubmitField('Add')


class PatientProviderForm(FlaskForm):
    patientID = SelectField('Patient ID') 
    nationalProviderIdentifier = SelectField('NPI')
    submit = SubmitField('Add')