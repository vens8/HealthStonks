from app import app

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print("Error occured:", e)
        log_backend(f"Error: {e}")
        app.sendErrorMessage(e)
