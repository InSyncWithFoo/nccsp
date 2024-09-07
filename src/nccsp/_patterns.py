import regex


suggestion_values = regex.compile(
	r'''(?x)
	\[\s*
	(?P<value>"[^"]+")
	(?:\s*(?P<value>"[^"]+"))*
	\s*]
	'''
)
option_or_argument = regex.compile(
	r'''(?mx)
	^\x20{4}
	(?P<name>
		[-a-zA-Z0-9]+
	|
		(?P<variadic>\.{3})?
		[a-zA-Z0-9]+
		(?P<optional>\?)?
	)
	(?:\((?P<alias>[^()\n]+)\))?
	(?:
		:[^\S\r\n]*
		(?P<type>[a-zA-Z]+)
		(?:@"(?P<suggestion_id>[^"\n]+)")?
	)?
	(?:[^\S\r\n]*\#[^\S\r\n]*(?P<description>.+))?
	'''
)
command = regex.compile(
	r'''(?mx)
	(?:
		^\x20{2}def\x20"(?P<suggestion_definition_id>[^"]+)"\x20\[]\x20\{
		\s*(?P<suggestion_definition_values>[\s\S]+?)\s*
		}\n\n
	)*
	(?:^\x20{2}\#\x20(?P<description>.+)\n)?
	\x20{2}export\x20extern\x20
	(?:(?P<fragments>[a-zA-Z0-9]+)|"(?P<fragments>[^"]+)")
	\x20\[\n
	(?P<options_and_arguments>(?:.+\n)*?)
	\x20{2}]
	'''
)
