# Hi I am Jesse Vogt - jessevogt.com

## Demo Project
__github.com/jessevogt/mke-python-demo-get-my-ip__
- get my public ip address by checking against a number of public services
- `services.py`
	- holds endpoint url
	- can make request through a provided `ClientSession`
	- can extract ip address from service response
	- service.txt
- `myp.py`
    - main entry point
	- requests my ip from each defined service
	- return ip address if they all give back same, otherwise except
	

## Needs tests!
### [pytest](https://docs.pytest.org/en/latest/)

`test_myp.py`
- test text service
- test json service
- test different ip addresses returned

### [doctest](https://docs.python.org/3/library/doctest.html)
`services.py`
- parse_service


## Continuous Integration:
- Docker
- TravisCI
```
sudo: required
services:
    - docker
before_install:
    - docker build -t jessevogt/get-my-ip:$TRAVIS_COMMIT .
script:
    - docker run --rm jessevogt/get-my-ip:$TRAVIS_COMMIT pytest
```

Badge me!

References for TravisCI
- [TravisCI: Using Docker in Builds](https://docs.travis-ci.com/user/docker/)
- [Example from Heroku Logplx (docker-compose)](https://github.com/heroku/logplex)

