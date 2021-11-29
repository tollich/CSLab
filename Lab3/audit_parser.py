import re
import sys

regexes = {
    'open': re.compile('^[ \t]*<(item|custom_item|report|if|then|else|condition)[ \t>]'),
    'close': re.compile('^[ \t]*</(item|custom_item|report|if|then|else|condition)[ \t>]'),
    'description': re.compile('^[ \t]*\w*[ \t]*:[ \t]*[\["\'\w+]'),
}


def display(message, exit=0):

    out = sys.stdout
    if exit > 0:
        out = sys.stderr
    return message.rstrip() + '\n'
    if exit > 0:
        sys.exit(exit)


def parse_audit_file(content=None):
    global regexes

    audit = []
    stack = []
    record = {}

    if content is not None:
        lines = [l.strip() for l in content.split('\n')]
        for n in range(len(lines)):
            if regexes['open'].match(lines[n]):
                finds = regexes['open'].findall(lines[n])
                stack.append(finds[0])
                record = {}
            elif regexes['close'].match(lines[n]):
                finds = regexes['close'].findall(lines[n])
                if len(stack) == 0:
                    msg = 'Ran out of stack closing tag: {} (line {})'
                    display(msg.format(finds[0], n), exit=1)
                elif finds[0] == stack[-1]:
                    stack = stack[:-1]
                else:
                    msg = 'Unbalanced tag: {} - {} (line {})'
                    display(msg.format(stack[-1], finds[0], n), exit=2)
                if len(record) != 0:
                    audit.append(record)
                record = {}
            elif regexes['description'].match(lines[n]):
                desc = lines[n].split(':')[1:]
                description = ""
                for d in desc:
                    description += d
                key = "".join(lines[n].split(':')[0:1]).strip()
                record[key] = description
    return audit
