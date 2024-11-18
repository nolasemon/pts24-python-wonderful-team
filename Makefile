all: check_and_test lint format

check_and_test: FORCE
	mypy stone_age --strict
	mypy test --strict
	python3 -m unittest 

lint: FORCE
	pylint stone_age/
	pylint test/

format: FORCE
	autopep8 -i stone_age/*.py
	autopep8 -i stone_age/player_board/*.py
	autopep8 -i stone_age/game_board/*.py
	autopep8 -i stone_age/game_phase_controller/*.py
	autopep8 -i test/*.py
	autopep8 -i test/test_integration/*.py
	autopep8 -i test/player_board/*.py
	autopep8 -i test/game_board/*.py
	autopep8 -i test/game_phase_controller/*.py
	autopep8 -i test/player_board/test_integration/*.py
	autopep8 -i test/game_board/test_integration/*.py
	autopep8 -i test/game_phase_controller/test_integration/*.py
FORCE: ;
