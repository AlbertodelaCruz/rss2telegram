default:
	@printf "$$HELP"
docker-build:
	docker build . -t python-dev
docker-tests:
	docker run --rm -v "${PWD}:/usr/src/app" python-dev make tests
tests:
	mamba specs
unit-tests:
	mamba specs -t unit
integration-tests:
	mamba specs -t integration
acceptance-tests:
	mamba specs -t acceptance

define HELP
# Local commands
	- make tests\tRun all tests using Python3 and Mamba
	- make unit-tests\tRun unit tests
	- make integration-tests\tRun integration tests
	- make acceptance-tests\tRun acceptance tests
 Please execute "make <command>". Example make help

endef

export HELP
