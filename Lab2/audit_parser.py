import re

#using regular expresions to parse properly the .audit file
regexes = {
  'open': re.compile('^[ \t]*<(item|custom_item|if|then|else|condition)[ \t>]'),
  'close': re.compile('^[ \t]*</(item|custom_item|if|then|else|condition)[ \t>]'),
  #'info': re.compile('^[ \t]*(type|description|info|Note|Note #2|solution|reference|see_also|reg_option|value_type|value_data|reg_key|reg_item|check_type)[ \t]*:[ \t]*["\']*'),
  'info': re.compile('^[ \t]*(description)[ \t]*:[ \t]*["\']*'),
}

def parse_audit_file(content=None):
    global regexes
    lines = []
    audit = []
    stack = []

    if content is not None:
        lines = [l.strip() for l in content.split('\n')] #analyzing every line
        for n in range(len(lines)):
            if regexes['open'].match(lines[n]): #search words suitable for open regex and apend to stack and audit arrays
                finds = regexes['open'].findall(lines[n])
                #audit.append((n + 1, len(stack), lines[n]))
                stack.append(finds[0])
            elif regexes['close'].match(lines[n]): #search words suitable for close regex
                finds = regexes['close'].findall(lines[n])
                #audit.append((n + 1, len(stack), lines[n]))
                if len(stack) == 0:
                    msg = 'Ran out of stack closing tag: {} (line {})'
                    display(msg.format(finds[0], n), exit=1)
                elif finds[0] == stack[-1]:
                    stack = stack[:-1]
                else:
                    msg = 'Unbalanced tag: {} - {} (line {})'
                    display(msg.format(stack[-1], finds[0], n), exit=2)
            elif regexes['info'].match(lines[n]): #search info between open and close tags
                #audit.append((n + 1, len(stack), lines[n]))
                info = ':'.join(lines[n].split(':')[1:]).strip()[1:-1]
                audit.append((n + 1, len(stack), info))
        audit = audit[2:-1]
    return audit