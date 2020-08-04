from statbus.wsgi import application

if __name__ == "__main__":
    application.run(port=8080, debug=True)
