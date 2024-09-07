'''
The parsing functions.
'''

from typing import cast

import regex

from ._models import Command, OptionOrArgument
from ._patterns import command, option_or_argument, suggestion_values


type _SuggestionDefinitions = dict[str, list[str]]


class _UnexpectedFormatException(ValueError):
	'''
	Raised when the script is not in the expected format.
	'''


def _parse_value_list(content: str) -> list[str]:
	matches = suggestion_values.fullmatch(content)
	
	if matches is None:
		message = f'Suggestion definition is malformed: {content}'
		raise _UnexpectedFormatException(message)
	
	return [value.strip('"') for value in matches.captures('value')]


def _parse_suggestion_definitions(match: regex.Match[str]) -> _SuggestionDefinitions:
	ids = match.captures('suggestion_definition_id')
	value_lists = match.captures('suggestion_definition_values')
	
	definitions: _SuggestionDefinitions = {}
	
	for (definition_id, value_list) in zip(ids, value_lists, strict = True):
		definitions[definition_id] = _parse_value_list(value_list)
	
	return definitions


def _parse_fragments(content: str) -> list[str]:
	return regex.split(r'\s+', content.strip())


def _parse_option(match: regex.Match[str], suggestion_definitions: _SuggestionDefinitions) -> OptionOrArgument:
	name = cast(str, match['name'])
	alias = cast(str | None, match['alias'])
	value_type = cast(str | None, match['type'])
	variadic = match['variadic'] is not None
	optional = match['optional'] is not None
	description = cast(str | None, match['description'])
	
	suggestion_id = cast(str | None, match['suggestion_id'])
	suggestions = (
		suggestion_definitions[suggestion_id]
		if suggestion_id is not None
		else None
	)
	
	return OptionOrArgument(
		name = name,
		alias = alias,
		type = value_type,
		variadic = variadic,
		optional = optional,
		suggestions = suggestions,
		description = description
	)


def _parse_options(content: str, suggestion_definitions: _SuggestionDefinitions) -> list[OptionOrArgument]:
	lines = content.splitlines()
	options_and_arguments = list[OptionOrArgument]()
	
	for line in lines:
		match = option_or_argument.search(line)
		
		if match is None:
			message = f'Option/argument is malformed: {content}'
			raise _UnexpectedFormatException(message)
		
		options_and_arguments.append(_parse_option(match, suggestion_definitions))
	
	return options_and_arguments


def _parse_command(match: regex.Match[str]) -> Command:
	suggestion_definitions = _parse_suggestion_definitions(match)
	fragment_group = match['fragments']
	options_and_arguments_group = match['options_and_arguments']
	
	if not isinstance(fragment_group, str) or not isinstance(options_and_arguments_group, str):
		message = f'Command is malformed: {match[0]}'
		raise _UnexpectedFormatException(message)
	
	fragments = _parse_fragments(fragment_group)
	options_and_arguments = _parse_options(options_and_arguments_group, suggestion_definitions)
	
	return Command(fragments = fragments, options_and_arguments = options_and_arguments)


def parse_commands(script: str) -> list[Command]:
	'''
	Parse a given script and return a list of :class:`Command`s.
	
	:param script: The script to parse.
	:return: All commands included in that script.
	'''
	
	matches = command.finditer(script)
	
	return [_parse_command(match) for match in matches]
