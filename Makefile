default:
	@printf "$$HELP"
tests:
	mamba -f documentation specs
unit-tests:
	mamba -f documentation specs -t unit
integration-tests:
	mamba -f documentation specs -t integration
acceptance-tests:
	mamba -f documentation specs -t acceptance

define HELP
# Local commands
	- make tests\tRun all tests using Python3 and Mamba
	- make unit-tests\tRun unit tests
	- make integration-tests\tRun integration tests
	- make acceptance-tests\tRun acceptance tests
 Please execute "make <command>". Example make help

endef

export HELP
