"""A tiny YAML-subset parser so config loading works without PyYAML.

Supports the subset used by museforge configs:
  * `key: value`        (scalar, string, number, bool)
  * `key: value  # cmt` (inline comments)
  * nested indentation  (2-space blocks)
  * block lists `- item`
  * inline lists `[a, b, c]`
"""
from __future__ import annotations


def _strip_comment(line: str) -> str:
    # remove " # comment" only when '#' is preceded by whitespace or at line start
    for i, ch in enumerate(line):
        if ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i].rstrip()
    return line.rstrip()


def _parse_scalar(s: str):
    s = s.strip()
    if s == "":
        return None
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [x.strip() for x in inner.split(",")]
    low = s.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "none", "~"):
        return None
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s


def parse(text: str):
    """Parse a YAML-subset document into nested dicts/lists."""
    lines = [ln.rstrip("\n\r") for ln in text.splitlines()]
    root = {}
    # stack entries: (indent, container, parent_dict, key, pending_placeholder)
    # pending_placeholder=True means `container` is an empty dict we created for
    # `key:` and it should turn into a list on the first `- item`.
    stack = [(-1, root, None, None, False)]
    for raw in lines:
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = _strip_comment(raw.strip())
        if not line:
            continue
        if line.startswith("- "):
            item = _parse_scalar(line[2:])
            while stack and stack[-1][0] >= indent:
                stack.pop()
            if not stack:
                stack = [(-1, root, None, None, False)]
            top = stack[-1]
            container = top[1]
            if isinstance(container, dict) and top[4] is True:
                # pending placeholder -> replace with a list, keeping parent indent
                parent = top[2]
                key = top[3]
                parent_indent = top[0]
                parent[key] = []
                stack[-1] = (parent_indent, parent[key], parent, key, False)
                container = parent[key]
            elif isinstance(container, list):
                pass
            else:
                container = []
                stack.append((indent, container, top[1], top[3], False))
            container.append(item)
            continue
        # key: value
        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            stack = [(-1, root, None, None, False)]
        parent = stack[-1][1]
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest == "":
            # nested block
            child = {}
            parent[key] = child
            stack.append((indent, child, parent, key, True))
        else:
            parent[key] = _parse_scalar(rest)
    return root
