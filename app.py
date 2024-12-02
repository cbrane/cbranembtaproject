from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp
import mbta_helper


app = Flask(__name__)
# Required for CSRF protection in WTForms
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key


class LocationForm(FlaskForm):
    """Form for validating location input."""
    place_name = StringField('Place Name', validators=[
        DataRequired(message="Please enter a place name or address."),
        Length(min=2, max=100, 
               message="Location must be between 2 and 100 characters."),
        Regexp(r'^[a-zA-Z0-9\s\.,#-]+$', 
               message="Please enter a valid location (letters, numbers, spaces, and basic punctuation only).")
    ])


@app.route("/", methods=["GET"])
def index():
    """Render the main page with the search form."""
    form = LocationForm()
    return render_template("index.html", form=form)


@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    """Handle the form submission and display nearest MBTA stations."""
    form = LocationForm()
    
    if not form.validate_on_submit():
        return render_template(
            "error.html",
            error=next(iter(form.place_name.errors), "Invalid input")
        )
    
    try:
        # Use our mbta_helper to find nearest stations
        stations = mbta_helper.find_stop_near(form.place_name.data)
        
        return render_template(
            "mbta_station.html",
            place_name=form.place_name.data,
            stations=stations
        )
        
    except Exception as e:
        return render_template(
            "error.html",
            error=f"An error occurred: {str(e)}"
        )


if __name__ == "__main__":
    app.run(debug=True)
