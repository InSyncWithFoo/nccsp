from pydantic import BaseModel


class OptionOrArgument(BaseModel):
	name: str
	alias: str | None
	variadic: bool
	optional: bool
	type: str | None
	suggestions: list[str] | None
	description: str | None


class Command(BaseModel):
	fragments: list[str]
	description: str | None
	options_and_arguments: list[OptionOrArgument]
