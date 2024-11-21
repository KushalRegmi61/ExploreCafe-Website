from flask import Flask, render_template, request, redirect, session, flash, url_for
from datetime import datetime
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, ValidationError, Email, Length
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Column, func
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, URL, ValidationError, Email, Length
from flask_ckeditor import CKEditorField, CKEditor
from smtplib import SMTP
from dotenv import load_dotenv
import os

#loading the environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD= os.getenv("EMAIL_PASSWORD")
DB_URL = os.getenv("DB_URL", "sqlite:///cafes.db")

#creating a flask app
app = Flask(__name__)

# initilizing the bootstrap
Bootstrap5(app)

#initializing the ckeditor
ckeditor = CKEditor(app)

#creating a secret key
app.config['SECRET_KEY'] = "8BYkEfBA"

#creating a declarative database
class Base(DeclarativeBase):
    pass
    

#creating a database
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(model_class=Base)
db.init_app(app)

#creating a table for cafes
class Cafes(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)
    country = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(250), nullable=False)

#creating a form for adding a new cafe
class AddCafeForm(FlaskForm):
    id = StringField(
        "Cafe ID",
        render_kw={"readonly": True, "class": "form-control", "placeholder": "Auto-generated ID"}
    )
    name = StringField(
        "Cafe Name",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter the cafe name"}
    )
    map_url = StringField(
        "Map URL",
        validators=[DataRequired(), URL()],
        render_kw={"class": "form-control", "placeholder": "Enter the Google Maps URL"}
    )
    img_url = StringField(
        "Image URL",
        validators=[DataRequired(), URL()],
        render_kw={"class": "form-control", "placeholder": "Enter the image URL"}
    )
    location = StringField(
        "Location",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter the location"}
    )
    has_sockets = RadioField(
        "Has Sockets?",
        choices=[('True', 'Yes'), ('False', 'No')],
        validators=[DataRequired()],
        render_kw={"class": "form-check-input"}
    )
    has_toilet = RadioField(
        "Has Toilet?",
        choices=[('True', 'Yes'), ('False', 'No')],
        validators=[DataRequired()],
        render_kw={"class": "form-check-input"}
    )
    has_wifi = RadioField(
        "Has WiFi?",
        choices=[('True', 'Yes'), ('False', 'No')],
        validators=[DataRequired()],
        render_kw={"class": "form-check-input"}
    )
    can_take_calls = RadioField(
        "Can Take Calls?",
        choices=[('True', 'Yes'), ('False', 'No')],
        validators=[DataRequired()],
        render_kw={"class": "form-check-input"}
    )
    seats = StringField(
        "Number of Seats (e.g., 20-40 seats)",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter the seating capacity"}
    )
    coffee_price = StringField(
        "Coffee Price (e.g., $5.99)",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter the coffee price"}
    )
    submit = SubmitField(
        "Add Cafe",
        render_kw={"class": "btn btn-primary"}
    )


#creating a form for editing a cafefrom flask_wtf import FlaskForm
class EditCafeForm(FlaskForm):
    id = StringField(
        "Cafe ID",
        render_kw={"readonly": True, "class": "form-control", "placeholder": "Auto-generated ID"}
    )
    name = StringField(
        "Cafe Name",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter the cafe name"}
    )
    map_url = StringField(
        "Map URL",
        validators=[DataRequired(), URL()],
        render_kw={"class": "form-control", "placeholder": "Enter the Google Maps URL"}
    )
    img_url = StringField(
        "Image URL",
        validators=[DataRequired(), URL()],
        render_kw={"class": "form-control", "placeholder": "Enter the image URL"}
    )
    location = StringField(
        "Location",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter the location"}
    )
    has_sockets = RadioField(
        "Has Sockets?",
        choices=[('True', 'Yes'), ('False', 'No')],
        validators=[DataRequired()],
        render_kw={"class": "form-check-input"}
    )
    has_toilet = RadioField(
        "Has Toilet?",
        choices=[('True', 'Yes'), ('False', 'No')],
        validators=[DataRequired()],
        render_kw={"class": "form-check-input"}
    )
    has_wifi = RadioField(
        "Has WiFi?",
        choices=[('True', 'Yes'), ('False', 'No')],
        validators=[DataRequired()],
        render_kw={"class": "form-check-input"}
    )
    can_take_calls = RadioField(
        "Can Take Calls?",
        choices=[('True', 'Yes'), ('False', 'No')],
        validators=[DataRequired()],
        render_kw={"class": "form-check-input"}
    )
    seats = StringField(
        "Number of Seats (e.g., 20-40 seats)",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter the seating capacity"}
    )
    coffee_price = StringField(
        "Coffee Price (e.g., $5.99)",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter the coffee price"}
    )
    submit = SubmitField(
        "Update Cafe",
        render_kw={"class": "btn btn-primary"}
    )


#creating a Feedback form
class FeedbackForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter your name"}
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control", "placeholder": "Enter your email address"}
    )
    phone = StringField(
        "Phone",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter your phone number"}
    )
    message = CKEditorField(
        "Message",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter your message"}
    )
    submit = SubmitField(
        "Send Feedback",
        render_kw={"class": "btn btn-primary"}
    )


#initializing the database
with app.app_context():
    db.create_all() 


#home route
@app.route('/')
def home():
    return render_template('index.html')

#Explore cafe_route
@app.route('/explore_cafe')
def explore_cafe():    
    # Get distinct countries from the cafes table
    countries = db.session.query(Cafes.country).distinct()
    print(countries)
    # Initialize an empty dictionary to store country -> cities mapping
    country_city_dict = {}
    
    # Loop through each country
    for country_tuple in countries:
        country = country_tuple[0]  # Extract the country name from the tuple
        
        # Get all cities associated with this country
        cities = db.session.query(Cafes.city).filter(Cafes.country == country).distinct().all()
        
        # Create a list of cities for the current country
        city_list = [city[0] for city in cities]  # Extract city names from tuples
        
        # Add the country and its cities to the dictionary
        country_city_dict[country] = city_list
    
    # Print or return the dictionary
    print(country_city_dict)

   
    return render_template('explore_cafe.html', countries=country_city_dict)
    

#Add cafe route
@app.route('/add_cafe', methods=['GET', 'POST'])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        try:
            # Attempt to add the new cafe to the database
            new_cafe = Cafes(
                name=form.name.data,
                map_url=form.map_url.data,
                img_url=form.img_url.data,
                location=form.location.data,
                has_sockets=form.has_sockets.data,
                has_toilet=form.has_toilet.data,
                has_wifi=form.has_wifi.data,
                can_take_calls=form.can_take_calls.data,
                seats=form.seats.data,
                coffee_price=form.coffee_price.data,
                country=form.country.data,
                city=form.city.data
            )
            db.session.add(new_cafe)
            db.session.commit()
            
            # Set success message
            session['message'] = "Cafe added successfully!"
            session['message_type'] = 'success'

        except Exception as e:
            # Handle error, set error message
            session['message'] = "There was an issue adding the cafe. Please try again."
            session['message_type'] = 'error'

        # Pop the session message after setting it, and pass the message to the template
        message = session.pop('message', None)
        message_type = session.pop('message_type', None)

        return render_template('add_cafe.html', form=form, message=message, message_type=message_type)

    # If form not submitted, just render the form with no message
    return render_template('add_cafe.html', form=form)


#Delete cafe route
@app.route('/delete_cafe/<int:cafe_id>', methods=['GET'])
def delete_cafe(cafe_id):
    cafe = db.session.query(Cafes).get(cafe_id)
    if not cafe:
        return render_template("404.html"), 404
    return render_template("delete.html", cafe=cafe)

@app.route('/delete_cafe_confirm/<int:cafe_id>', methods=['POST'])
def delete_cafe_confirm(cafe_id):
    cafe = db.session.query(Cafes).get(cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        flash(f'Cafe "{cafe.name}" has been deleted!', 'success')
    else:
        flash('Cafe not found.', 'danger')
    return redirect(url_for('explore_cafe'))


#search_cafe route
@app.route('/search_cafe', methods=['GET', 'POST'])
def search_cafe():
    # Convert city_name from the URL to lowercase
    if request.method == 'POST':
        city_name = request.form.get('city_name')
        location_lower = city_name.lower()

    else:    
        location_lower = request.args.get('city_name').lower()
    
    # Getting all the cafes from the database with the city_name (case-insensitive)
    cafes = db.session.execute(db.select(Cafes).where(func.lower(Cafes.city) == location_lower)).scalars().all()
    print(cafes)
    return render_template('cafe_list.html', cafes=cafes)


#display_cafe details
@app.route('/cafe/<int:cafe_id>')
def cafe_details(cafe_id):
    cafe = Cafes.query.get_or_404(cafe_id) # Get the cafe with the given ID
    return render_template('cafe_details.html', cafe=cafe)

#update_cafe route
@app.route('/update_cafe', methods=['GET', 'POST'])
def update_cafe():
    post_id = request.args.get('post_id')
    cafe = db.session.query(Cafes).get(post_id)
    if not cafe:
        flash("Cafe not found!", "error")
        return redirect(url_for('home'))  # Redirect to the home page or appropriate view

    form = EditCafeForm(
        id=cafe.id,
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        has_sockets='True' if cafe.has_sockets else 'False',
        has_toilet='True' if cafe.has_toilet else 'False',
        has_wifi='True' if cafe.has_wifi else 'False',
        can_take_calls='True' if cafe.can_take_calls else 'False',
        seats=cafe.seats,
        coffee_price=cafe.coffee_price
    )

    if form.validate_on_submit():
        try:
            # Update cafe details from the form
            cafe.name = form.name.data
            cafe.map_url = form.map_url.data
            cafe.img_url = form.img_url.data
            cafe.location = form.location.data
            cafe.has_sockets = form.has_sockets.data == 'True'  # Convert to boolean
            cafe.has_toilet = form.has_toilet.data == 'True'    # Convert to boolean
            cafe.has_wifi = form.has_wifi.data == 'True'        # Convert to boolean
            cafe.can_take_calls = form.can_take_calls.data == 'True'  # Convert to boolean
            cafe.seats = form.seats.data
            cafe.coffee_price = form.coffee_price.data

            # Commit changes to the database
            db.session.commit()
            flash("Cafe updated successfully!", "success")
            return redirect(url_for('home'))  # Redirect to avoid resubmission
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            flash("An error occurred while updating the cafe. Please try again.", "error")

    return render_template('update_cafe.html', form=form)


# Feedback route
@app.route('/send_feedback', methods=['GET', 'POST'])
def send_feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        # Get form data
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data


        # Send feedback to the admin
        try:
            with SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=PASSWORD)
                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Feedback\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
                )
        except Exception as e:
            print(e)
            flash("An error occurred while sending feedback. Please try again.", "error")
            return redirect(url_for('send_feedback'))

        # Set success message
        flash("Feedback sent successfully!", "success")

        return redirect(url_for('home'))

    return render_template('feedback.html', form=form)

#running the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)