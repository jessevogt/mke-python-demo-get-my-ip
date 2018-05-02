# Hi I am Jesse Vogt - jessevogt.com

## Demo Project
__github.com/jessevogt/mke-python-demo-get-my-ip__
- get my public ip address by checking against a number of public services
- `Service`
	- holds endpoint url
	- can make request through a provided `ClientSession`
	- can extract ip address from service response
	- service.txt
- `myp`
    - main entry point
	- requests my ip from each defined service
	- return ip address if they all give back same, otherwise except
	

## Needs tests!
- `pytest`
	- test_myp.py
		- test text service
		- test json service
		- test different ip addresses returned
	- doctest
		- services.py::parse_service
Continuous Integration:
- Docker
- TravisCI
sudo: required
services:
		- docker
before_install:
- docker build -t jessevogt/get-my-ip:$TRAVIS_COMMIT .
	
	script:
		- docker run --rm jessevogt/get-my-ip:$TRAVIS_COMMIT pytest

