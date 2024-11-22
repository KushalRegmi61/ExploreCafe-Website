from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, URL, Email
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import func, Column, Integer, String, Boolean
from flask_ckeditor import CKEditorField, CKEditor
from dotenv import load_dotenv
import os
from smtplib import SMTP

# Load environment variables from a .env file
load_dotenv()

# Environment variables for email credentials and database URL
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
DB_URL = os.getenv("DB_URL", "sqlite:///cafes.db")  # Default to SQLite if no DB URL is provided

# Initialize Flask app
app = Flask(__name__)

# Set up Bootstrap and CKEditor for better UI and text editing capabilities
Bootstrap5(app)
ckeditor = CKEditor(app)

# Configure the Flask app
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "8BYkEfBA")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Define the database model for cafes
class Cafes(db.Model):
    __tablename__ = "cafe"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)
    map_url = Column(String(250), nullable=False)
    img_url = Column(String(250), nullable=False)
    location = Column(String(250), nullable=False)
    has_sockets = Column(Boolean, nullable=False)
    has_toilet = Column(Boolean, nullable=False)
    has_wifi = Column(Boolean, nullable=False)
    can_take_calls = Column(Boolean, nullable=False)
    seats = Column(String(250), nullable=False)
    coffee_price = Column(String(250), nullable=False)
    country = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)

# Define the form for adding a new cafe
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, URL

class AddCafeForm(FlaskForm):
    name = StringField(
        "Cafe Name", 
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter the cafe's name"}
    )
    map_url = StringField(
        "Map URL", 
        validators=[DataRequired(), URL()],
        render_kw={"class": "form-control", "placeholder": "Enter the Google Maps URL"}
    )
    img_url = StringField(
        "Image URL", 
        validators=[DataRequired(), URL()],
        render_kw={"class": "form-control", "placeholder": "Enter an image URL"}
    )
    location = StringField(
        "Location", 
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter the cafe's location"}
    )
    city = StringField(
        "City", 
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter the city"}
    )
    country = StringField(
        "Country", 
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Enter the country"}
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
        render_kw={"class": "form-control", "placeholder": "Enter the number of seats"}
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
    


# Define the form for editing a cafe (inherits from AddCafeForm)
class EditCafeForm(AddCafeForm):

    # Override the submit field with a new label
    submit = SubmitField("Update Cafe", render_kw={"class": "btn btn-primary"})


# Define the form for collecting feedback
class FeedbackForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired()])
    message = CKEditorField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Feedback")

# Route for the homepage
@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')

# Route to explore cafes by country and city
@app.route('/explore_cafe')
def explore_cafe():
    """Render a page to explore cafes based on countries and cities."""
    countries = db.session.query(Cafes.country).distinct()
    country_city_dict = {
        country[0]: [city[0] for city in db.session.query(Cafes.city).filter(Cafes.country == country[0]).distinct()]
        for country in countries
    }
    return render_template('explore_cafe.html', countries=country_city_dict)

# Route to add a new cafe
@app.route('/add_cafe', methods=['GET', 'POST'])
def add_cafe():
    """Add a new cafe to the database."""
    form = AddCafeForm()
    if form.validate_on_submit():
        try:
            new_cafe = Cafes(
                name=form.name.data,
                map_url=form.map_url.data,
                img_url=form.img_url.data,
                location=form.location.data,
                has_sockets=form.has_sockets.data == 'True',
                has_toilet=form.has_toilet.data == 'True',
                has_wifi=form.has_wifi.data == 'True',
                can_take_calls=form.can_take_calls.data == 'True',
                seats=form.seats.data,
                coffee_price=form.coffee_price.data,
                city=form.city.data,
                country=form.country.data
            )
            db.session.add(new_cafe)
            db.session.commit()
            flash("Cafe added successfully!", "success")
            return redirect(url_for('cafe_details', cafe_id=new_cafe.id))
        except Exception as e:
            db.session.rollback()
            flash("Error adding cafe: " + str(e), "danger")
    return render_template('add_cafe.html', form=form)

# Route to view details of a specific cafe
@app.route('/cafe/<int:cafe_id>')
def cafe_details(cafe_id):
    """Render details of a specific cafe."""
    cafe = Cafes.query.get_or_404(cafe_id)
    return render_template('cafe_details.html', cafe=cafe)

# Route to update cafe details
@app.route('/update_cafe', methods=['GET', 'POST'])
def update_cafe():
    """Update details of an existing cafe."""
    cafe_id = request.args.get('cafe_id')
    cafe = Cafes.query.get_or_404(cafe_id)
    form = EditCafeForm(obj=cafe)
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
            cafe.city = form.city.data
            cafe.country = form.country.data

            # Commit changes to the database
            db.session.commit()
            # Set success message
            flash("Cafe updated successfully!", "success")
            # Redirect to the cafe details page
            return redirect(url_for('cafe_details', cafe_id=cafe.id))
        except Exception as e:
            db.session.rollback()
            flash("Error updating cafe: " + str(e), "danger")
    return render_template('update_cafe.html', form=form, cafe=cafe)

# # Route to delete a cafe
# @app.route('/delete_cafe/<int:cafe_id>', methods=['POST'])
# def delete_cafe(cafe_id):
#     """Delete a cafe from the database."""
#     cafe = Cafes.query.get_or_404(cafe_id)
#     db.session.delete(cafe)
#     db.session.commit()
#     flash("Cafe deleted successfully!", "success")
#     return redirect(url_for('explore_cafe'))

# Route to search cafes by city
@app.route('/search_cafe', methods=['GET', 'POST'])
def search_cafe():
    """Search cafes in a specific city."""
    if request.method == 'POST':
        city_name = request.form.get('city_name').lower()
    else:
        city_name = request.args.get('city_name', '').lower()
    cafes = db.session.query(Cafes).filter(func.lower(Cafes.city) == city_name).all()
    return render_template('cafe_list.html', cafes=cafes)



#Delete cafe route
@app.route('/delete_cafe/<int:cafe_id>', methods=['GET'])
def delete_cafe(cafe_id):
    """Delete a cafe from the database."""
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
    return redirect(url_for('home'))

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

# Initialize the database and create tables if they don't exist
with app.app_context():
    db.create_all()

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
