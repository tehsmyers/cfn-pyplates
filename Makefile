sdist:
	./setup.py sdist

upload:
	./setup.py sdist bdist_wheel upload

clean:
	rm -rf AUTHORS build ChangeLog dist *.egg-info __pycache__ *.egg .coverage

test:
	py.test --cov cfn_pyplates --cov-report term-missing tests
