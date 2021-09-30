from src.app import App

if __name__ == '__main__':
    app: App = App('https://books.toscrape.com/')
    app.run()
