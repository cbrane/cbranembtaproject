# MBTA Station Finder Web Application - OIM3640 Project 3 - Connor Raney

A Flask-based web application developed as part of the OIM3640 Problem Solving & Software Design course at Babson College. This application helps users find the nearest MBTA stations and real-time transit information for locations in the Greater Boston area, along with current weather information for the searched location. You can find the project reflection in the reflection.md file.

## Course Information
- **Course**: OIM3640 Problem Solving & Software Design
- **Institution**: Babson College
- **Project Type**: Project 3: Web App Project

## Project Overview
This project demonstrates the practical application of Python programming concepts learned in OIM3640, including:
- Web API integration
- Flask web framework implementation
- Object-oriented programming
- Error handling
- User input validation
- Web development fundamentals

## Features

- Search for any location in the Greater Boston area
- Find the nearest subway station and bus stop
- View real-time arrival predictions for both subway and bus services
- Check wheelchair accessibility status for stations
- Get current weather information including:
  - Temperature and "feels like" temperature
  - Weather description with icon
  - Humidity levels
  - Wind speed
- Form validation with user-friendly error messages
- Responsive design that works on both desktop and mobile devices

## Technologies Used

- **Backend:**
  - Python 3.x
  - Flask web framework
  - Flask-WTF for form handling and validation
  - python-dotenv for environment variable management

- **Frontend:**
  - HTML5
  - CSS3 with modern features (CSS variables, Flexbox, Grid)
  - Responsive design principles

- **APIs:**
  - MBTA V3 API for transit information
  - Mapbox API for geocoding
  - OpenWeather API for weather data

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mbta-station-finder.git
cd mbta-station-finder
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API keys:
```
MAPBOX_TOKEN=your_mapbox_token
MBTA_API_KEY=your_mbta_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

## Usage

1. Make sure your virtual environment is activated
2. Run the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

4. Enter a location in the Greater Boston area (e.g., "Fenway Park", "Harvard Square")

## Project Structure

- `app.py`: Main Flask application file containing routes and form validation
- `mbta_helper.py`: Helper module for API interactions and data processing
- `templates/`: Directory containing HTML templates
  - `index.html`: Home page with search form
  - `mbta_station.html`: Results page showing station and weather information
  - `error.html`: Error page for handling and displaying errors

## Key Components

### Form Validation
The application uses Flask-WTF for form validation, ensuring:
- Required field validation
- Length constraints (2-100 characters)
- Character validation (letters, numbers, spaces, basic punctuation)
- CSRF protection

### API Integration
- **Mapbox API**: Converts location names to coordinates
- **MBTA API**: Finds nearest stations and real-time arrival predictions
- **OpenWeather API**: Provides current weather information

### Error Handling
- Graceful handling of API errors
- User-friendly error messages
- Easy navigation back to search

## Design Features

- Modern, clean interface
- Responsive design that adapts to different screen sizes
- Clear visual hierarchy
- Accessibility indicators
- Weather information with icons
- Status alerts for transit arrivals
- Consistent color scheme and styling

## Environment Variables

The following environment variables are required:
- `MAPBOX_TOKEN`: Your Mapbox API access token
- `MBTA_API_KEY`: Your MBTA V3 API key
- `OPENWEATHER_API_KEY`: Your OpenWeather API key

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Academic Integrity
This project was completed as part of OIM3640 coursework at Babson College. While the code is available for reference, students should follow their institution's academic integrity policies when working on their own projects.

## Acknowledgments

- Professor and teaching assistants of OIM3640 at Babson College
- MBTA for providing the transit API
- Mapbox for geocoding services
- OpenWeather for weather data
- Flask and its contributors for the web framework

## Future Enhancements

- Add support for filtering by transit type
- Include real-time service alerts
- Implement route planning functionality
- Add favorite locations feature
- Integrate with more local services
