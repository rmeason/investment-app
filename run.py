from app import create_app

# Create an instance of the Flask app
app = create_app()

if __name__ == "__main__":
    # Run the app on all available interfaces, on port 5000, with debug mode enabled
    app.run(host='0.0.0.0', port=5000, debug=True)
