freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

clean:
	rm -rf __pycache__


