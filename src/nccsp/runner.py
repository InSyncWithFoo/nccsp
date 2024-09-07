'''
The CLI of the tool.
'''

# ruff: noqa: S603

import json
import subprocess
from pathlib import Path
from subprocess import CalledProcessError

import typer

from nccsp import parse_commands


def _get_script_from_executable(executable: Path) -> str:
	try:
		arguments = [executable, 'generate-shell-completion', 'nushell']
		output_stream = subprocess.check_output(arguments)
		
		return output_stream.decode('utf-8')
	except CalledProcessError as error:
		raise typer.Exit from error


def _script(script: str = typer.Argument(help = 'The script to parse')) -> None:
	'''
	Parse a script.
	'''
	
	try:
		commands = parse_commands(script)
	except ValueError as error:
		raise typer.Exit from error
	
	typer.echo(json.dumps([command.model_dump() for command in commands], indent = 4))


def _executable(executable: Path = typer.Argument(help = 'The executable to invoke.')) -> None:  # noqa: B008
	'''
	Retrieve the script from an executable, then parse it.
	'''
	
	script = _get_script_from_executable(executable)
	
	_script(script)


def main() -> None:  # noqa: D103
	app = typer.Typer()
	
	app.command('script')(_script)
	app.command('executable')(_executable)
	
	app()


if __name__ == '__main__':
	main()
