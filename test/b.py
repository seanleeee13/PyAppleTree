class HelpFormatter(object):
    """Formatter for generating usage messages and argument help strings.

    Only the name of this class is considered a public API. All the methods
    provided by the class are considered an implementation detail.
    """

    def __init__(
        self,
        prog,
        indent_increment=2,
        max_help_position=24,
        width=None,
    ):
        # default setting for width
        if width is None:
            import shutil
            width = shutil.get_terminal_size().columns
            width -= 2

        self._prog = prog
        self._indent_increment = indent_increment
        self._max_help_position = min(max_help_position,
                                      max(width - 20, indent_increment * 2))
        self._width = width

        self._current_indent = 0
        self._level = 0
        self._action_max_length = 0

        self._root_section = self._Section(self, None)
        self._current_section = self._root_section

        self._whitespace_matcher = _re.compile(r'\s+', _re.ASCII)
        self._long_break_matcher = _re.compile(r'\n\n\n+')

        self._set_color(False)

    def _set_color(self, color, *, file=None):
        # Set a new color setting and file, clear caches for theme and decolor
        self._theme_color = color
        self._theme_file = file
        self._cached_theme = None
        self._cached_decolor = None

    def _get_theme_and_decolor(self):
        # If self._theme_color is false, this prevents _colorize from importing
        if self._theme_color and _colorize.can_colorize(file=self._theme_file):
            self._cached_theme = _colorize.get_theme(force_color=True).argparse
            self._cached_decolor = _colorize.decolor
        else:
            self._cached_theme = _colorless_theme
            self._cached_decolor = _identity

    @property
    def _theme(self):
        if self._cached_theme is None:
            self._get_theme_and_decolor()
        return self._cached_theme

    @property
    def _decolor(self):
        if self._cached_decolor is None:
            self._get_theme_and_decolor()
        return self._cached_decolor

    # ===============================
    # Section and indentation methods
    # ===============================

    def _indent(self):
        self._current_indent += self._indent_increment
        self._level += 1

    def _dedent(self):
        self._current_indent -= self._indent_increment
        assert self._current_indent >= 0, 'Indent decreased below 0.'
        self._level -= 1

    class _Section(object):

        def __init__(self, formatter, parent, heading=None):
            self.formatter = formatter
            self.parent = parent
            self.heading = heading
            self.items = []

        def format_help(self):
            # format the indented section
            if self.parent is not None:
                self.formatter._indent()
            join = self.formatter._join_parts
            item_help = join([func(*args) for func, args in self.items])
            if self.parent is not None:
                self.formatter._dedent()

            # return nothing if the section was empty
            if not item_help:
                return ''

            # add the heading if the section was non-empty
            if self.heading is not SUPPRESS and self.heading is not None:
                current_indent = self.formatter._current_indent
                heading_text = _('%(heading)s:') % dict(heading=self.heading)
                t = self.formatter._theme
                heading = (
                    f'{" " * current_indent}'
                    f'{t.heading}{heading_text}{t.reset}\n'
                )
            else:
                heading = ''

            # join the section-initial newline, the heading and the help
            return join(['\n', heading, item_help, '\n'])

    def _add_item(self, func, args):
        self._current_section.items.append((func, args))

    # ========================
    # Message building methods
    # ========================

    def start_section(self, heading):
        self._indent()
        section = self._Section(self, self._current_section, heading)
        self._add_item(section.format_help, [])
        self._current_section = section

    def end_section(self):
        self._current_section = self._current_section.parent
        self._dedent()

    def add_text(self, text):
        if text is not SUPPRESS and text is not None:
            self._add_item(self._format_text, [text])

    def add_usage(self, usage, actions, groups, prefix=None):
        if usage is not SUPPRESS:
            args = usage, actions, groups, prefix
            self._add_item(self._format_usage, args)

    def add_argument(self, action):
        if action.help is not SUPPRESS:

            # find all invocations
            get_invocation = lambda x: self._decolor(self._format_action_invocation(x))
            invocation_lengths = [len(get_invocation(action)) + self._current_indent]
            for subaction in self._iter_indented_subactions(action):
                invocation_lengths.append(len(get_invocation(subaction)) + self._current_indent)

            # update the maximum item length
            action_length = max(invocation_lengths)
            self._action_max_length = max(self._action_max_length,
                                          action_length)

            # add the item to the list
            self._add_item(self._format_action, [action])

    def add_arguments(self, actions):
        for action in actions:
            self.add_argument(action)

    # =======================
    # Help-formatting methods
    # =======================

    def format_help(self):
        help = self._root_section.format_help()
        if help:
            help = self._long_break_matcher.sub('\n\n', help)
            help = help.strip('\n') + '\n'
        return help

    def _join_parts(self, part_strings):
        return ''.join([part
                        for part in part_strings
                        if part and part is not SUPPRESS])

    def _format_usage(self, usage, actions, groups, prefix):
        t = self._theme

        if prefix is None:
            prefix = _('usage: ')

        # if usage is specified, use that
        if usage is not None:
            usage = (
                t.prog_extra
                + usage
                % {"prog": f"{t.prog}{self._prog}{t.reset}{t.prog_extra}"}
                + t.reset
            )

        # if no optionals or positionals are available, usage is just prog
        elif usage is None and not actions:
            usage = f"{t.prog}{self._prog}{t.reset}"

        # if optionals and positionals are available, calculate usage
        elif usage is None:
            prog = '%(prog)s' % dict(prog=self._prog)

            parts, pos_start = self._get_actions_usage_parts(actions, groups)
            # build full usage string
            usage = ' '.join(filter(None, [prog, *parts]))

            # wrap the usage parts if it's too long
            text_width = self._width - self._current_indent
            if len(prefix) + len(self._decolor(usage)) > text_width:

                # break usage into wrappable parts
                opt_parts = parts[:pos_start]
                pos_parts = parts[pos_start:]

                # helper for wrapping lines
                def get_lines(parts, indent, prefix=None):
                    lines = []
                    line = []
                    indent_length = len(indent)
                    if prefix is not None:
                        line_len = len(prefix) - 1
                    else:
                        line_len = indent_length - 1
                    for part in parts:
                        part_len = len(self._decolor(part))
                        if line_len + 1 + part_len > text_width and line:
                            lines.append(indent + ' '.join(line))
                            line = []
                            line_len = indent_length - 1
                        line.append(part)
                        line_len += part_len + 1
                    if line:
                        lines.append(indent + ' '.join(line))
                    if prefix is not None:
                        lines[0] = lines[0][indent_length:]
                    return lines

                # if prog is short, follow it with optionals or positionals
                prog_len = len(self._decolor(prog))
                if len(prefix) + prog_len <= 0.75 * text_width:
                    indent = ' ' * (len(prefix) + prog_len + 1)
                    if opt_parts:
                        lines = get_lines([prog] + opt_parts, indent, prefix)
                        lines.extend(get_lines(pos_parts, indent))
                    elif pos_parts:
                        lines = get_lines([prog] + pos_parts, indent, prefix)
                    else:
                        lines = [prog]

                # if prog is long, put it on its own line
                else:
                    indent = ' ' * len(prefix)
                    parts = opt_parts + pos_parts
                    lines = get_lines(parts, indent)
                    if len(lines) > 1:
                        lines = []
                        lines.extend(get_lines(opt_parts, indent))
                        lines.extend(get_lines(pos_parts, indent))
                    lines = [prog] + lines

                # join lines into usage
                usage = '\n'.join(lines)

            usage = usage.removeprefix(prog)
            usage = f"{t.prog}{prog}{t.reset}{usage}"

        # prefix with 'usage:'
        return f'{t.usage}{prefix}{t.reset}{usage}\n\n'

    def _is_long_option(self, string):
        return len(string) > 2

    def _get_actions_usage_parts(self, actions, groups):
        """Get usage parts with split index for optionals/positionals.

        Returns (parts, pos_start) where pos_start is the index in parts
        where positionals begin.
        This preserves mutually exclusive group formatting across the
        optionals/positionals boundary (gh-75949).
        """
        actions = [action for action in actions if action.help is not SUPPRESS]
        # group actions by mutually exclusive groups
        action_groups = dict.fromkeys(actions)
        for group in groups:
            for action in group._group_actions:
                if action in action_groups:
                    action_groups[action] = group
        # positional arguments keep their position
        positionals = []
        for action in actions:
            if not action.option_strings:
                group = action_groups.pop(action)
                if group:
                    group_actions = [
                        action2 for action2 in group._group_actions
                        if action2.option_strings and
                           action_groups.pop(action2, None)
                    ] + [action]
                    positionals.append((group.required, group_actions))
                else:
                    positionals.append((None, [action]))
        # the remaining optional arguments are sorted by the position of
        # the first option in the group
        optionals = []
        for action in actions:
            if action.option_strings and action in action_groups:
                group = action_groups.pop(action)
                if group:
                    group_actions = [action] + [
                        action2 for action2 in group._group_actions
                        if action2.option_strings and
                           action_groups.pop(action2, None)
                    ]
                    optionals.append((group.required, group_actions))
                else:
                    optionals.append((None, [action]))

        # collect all actions format strings
        parts = []
        t = self._theme
        pos_start = None
        for i, (required, group) in enumerate(optionals + positionals):
            start = len(parts)
            if i == len(optionals):
                pos_start = start
            in_group = len(group) > 1
            for action in group:
                # produce all arg strings
                if not action.option_strings:
                    default = self._get_default_metavar_for_positional(action)
                    part = self._format_args(action, default)
                    # if it's in a group, strip the outer []
                    if in_group:
                        if part[0] == '[' and part[-1] == ']':
                            part = part[1:-1]
                    part = t.summary_action + part + t.reset

                # produce the first way to invoke the option in brackets
                else:
                    option_string = action.option_strings[0]
                    if self._is_long_option(option_string):
                        option_color = t.summary_long_option
                    else:
                        option_color = t.summary_short_option

                    # if the Optional doesn't take a value, format is:
                    #    -s or --long
                    if action.nargs == 0:
                        part = action.format_usage()
                        part = f"{option_color}{part}{t.reset}"

                    # if the Optional takes a value, format is:
                    #    -s ARGS or --long ARGS
                    else:
                        default = self._get_default_metavar_for_optional(action)
                        args_string = self._format_args(action, default)
                        part = (
                            f"{option_color}{option_string} "
                            f"{t.summary_label}{args_string}{t.reset}"
                        )

                    # make it look optional if it's not required or in a group
                    if not (action.required or required or in_group):
                        part = '[%s]' % part

                # add the action string to the list
                parts.append(part)

            if in_group:
                parts[start] = ('(' if required else '[') + parts[start]
                for i in range(start, len(parts) - 1):
                    parts[i] += ' |'
                parts[-1] += ')' if required else ']'

        if pos_start is None:
            pos_start = len(parts)
        return parts, pos_start

    def _format_text(self, text):
        if '%(prog)' in text:
            text = text % dict(prog=self._prog)
        text_width = max(self._width - self._current_indent, 11)
        indent = ' ' * self._current_indent
        text = self._fill_text(text, text_width, indent)
        text = self._apply_text_markup(text)
        return text + '\n\n'

    def _apply_text_markup(self, text):
        """Apply color markup to text.

        Supported markup:
          `...` or ``...`` - inline code (rendered with prog_extra color)

        When colors are disabled, backticks are preserved as-is.
        """
        t = self._theme
        if not t.reset:
            return text
        text = _re.sub(
            r'(`{1,2})([^`]+)\1',
            rf'{t.prog_extra}\2{t.reset}',
            text,
        )
        return text

    def _format_action(self, action):
        # determine the required width and the entry label
        help_position = min(self._action_max_length + 2,
                            self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = self._format_action_invocation(action)
        action_header_no_color = self._decolor(action_header)

        # no help; start on same line and add a final newline
        if not action.help:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup

        # short action name; start on the same line and pad two spaces
        elif len(action_header_no_color) <= action_width:
            # calculate widths without color codes
            action_header_color = action_header
            tup = self._current_indent, '', action_width, action_header_no_color
            action_header = '%*s%-*s  ' % tup
            # swap in the colored header
            action_header = action_header.replace(
                action_header_no_color, action_header_color
            )
            indent_first = 0

        # long action name; start on the next line
        else:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup
            indent_first = help_position

        # collect the pieces of the action help
        parts = [action_header]

        # if there was help for the action, add lines of help text
        if action.help and action.help.strip():
            help_text = self._expand_help(action)
            if help_text:
                help_lines = self._split_lines(help_text, help_width)
                parts.append('%*s%s\n' % (indent_first, '', help_lines[0]))
                for line in help_lines[1:]:
                    parts.append('%*s%s\n' % (help_position, '', line))

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith('\n'):
            parts.append('\n')

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

        # return a single string
        return self._join_parts(parts)

    def _format_action_invocation(self, action):
        t = self._theme

        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            return (
                t.action
                + ' '.join(self._metavar_formatter(action, default)(1))
                + t.reset
            )

        else:

            def color_option_strings(strings):
                parts = []
                for s in strings:
                    if self._is_long_option(s):
                        parts.append(f"{t.long_option}{s}{t.reset}")
                    else:
                        parts.append(f"{t.short_option}{s}{t.reset}")
                return parts

            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                option_strings = color_option_strings(action.option_strings)
                return ', '.join(option_strings)

            # if the Optional takes a value, format is:
            #    -s, --long ARGS
            else:
                default = self._get_default_metavar_for_optional(action)
                option_strings = color_option_strings(action.option_strings)
                args_string = (
                    f"{t.label}{self._format_args(action, default)}{t.reset}"
                )
                return ', '.join(option_strings) + ' ' + args_string

    def _metavar_formatter(self, action, default_metavar):
        if action.metavar is not None:
            result = action.metavar
        elif action.choices is not None:
            result = '{%s}' % ','.join(map(str, action.choices))
        else:
            result = default_metavar

        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            else:
                return (result, ) * tuple_size
        return format

    def _format_args(self, action, default_metavar):
        get_metavar = self._metavar_formatter(action, default_metavar)
        if action.nargs is None:
            result = '%s' % get_metavar(1)
        elif action.nargs == OPTIONAL:
            result = '[%s]' % get_metavar(1)
        elif action.nargs == ZERO_OR_MORE:
            metavar = get_metavar(1)
            if len(metavar) == 2:
                result = '[%s [%s ...]]' % metavar
            else:
                result = '[%s ...]' % metavar
        elif action.nargs == ONE_OR_MORE:
            result = '%s [%s ...]' % get_metavar(2)
        elif action.nargs == REMAINDER:
            result = '...'
        elif action.nargs == PARSER:
            result = '%s ...' % get_metavar(1)
        elif action.nargs == SUPPRESS:
            result = ''
        else:
            try:
                formats = ['%s' for _ in range(action.nargs)]
            except TypeError:
                raise ValueError("invalid nargs value") from None
            result = ' '.join(formats) % get_metavar(action.nargs)
        return result

    def _expand_help(self, action):
        help_string = self._get_help_string(action)
        if '%' not in help_string:
            return self._apply_text_markup(help_string)
        params = dict(vars(action), prog=self._prog)
        for name in list(params):
            value = params[name]
            if value is SUPPRESS:
                del params[name]
            elif hasattr(value, '__name__'):
                params[name] = value.__name__
        if params.get('choices') is not None:
            params['choices'] = ', '.join(map(str, params['choices']))

        t = self._theme

        result = help_string % params

        if not t.reset:
            return result

        # Match format specifiers like: %s, %d, %(key)s, etc.
        fmt_spec = r'''
            %
            (?:
                %                           # %% escape
                |
                (?:\((?P<key>[^)]*)\))?     # key
                [-#0\ +]*                   # flags
                (?:\*|\d+)?                 # width
                (?:\.(?:\*|\d+))?           # precision
                [hlL]?                      # length modifier
                [diouxXeEfFgGcrsa]          # conversion type
            )
        '''

        def colorize(match):
            spec, key = match.group(0, 'key')
            if spec == '%%':
                return '%'
            if key is not None:
                # %(key)... - format and colorize
                formatted = spec % {key: params[key]}
                return f'{t.interpolated_value}{formatted}{t.reset}'
            # bare %s etc. - format with full params dict, no colorization
            return spec % params

        return self._apply_text_markup(
            _re.sub(fmt_spec, colorize, help_string, flags=_re.VERBOSE)
        )

    def _iter_indented_subactions(self, action):
        try:
            get_subactions = action._get_subactions
        except AttributeError:
            pass
        else:
            self._indent()
            yield from get_subactions()
            self._dedent()

    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(' ', text).strip()
        # The textwrap module is used only for formatting help.
        # Delay its import for speeding up the common usage of argparse.
        import textwrap
        return textwrap.wrap(text, width)

    def _fill_text(self, text, width, indent):
        text = self._whitespace_matcher.sub(' ', text).strip()
        import textwrap
        return textwrap.fill(text, width,
                             initial_indent=indent,
                             subsequent_indent=indent)

    def _get_help_string(self, action):
        return action.help

    def _get_default_metavar_for_optional(self, action):
        return action.dest.upper()

    def _get_default_metavar_for_positional(self, action):
        return action.dest
