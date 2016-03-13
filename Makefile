sdist:
	./setup.py sdist

upload:
	./setup.py sdist bdist_wheel upload

clean:
	rm -rf AUTHORS build ChangeLog dist *.egg-info __pycache__ *.egg .coverage

requirements:
	pip install -Ur requirements.txt

test-requirements: requirements
	pip install -Ur test-requirements.txt

test:
	py.test --cov cfn_pyplates --cov-report term-missing tests
