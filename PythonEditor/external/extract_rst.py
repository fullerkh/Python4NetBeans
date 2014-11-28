##############################################################################
# RST generator from missing APIs.
# This output generates the contents for stub_missing.py which should
# be manually added into the pythonstubs egg to provide defs for the
# missing APIs.
#
# Tor Norbye <tor@netbeans.org> Jan 8, 2009
##############################################################################

import sys

import inspect
from types import StringType

# These are the APIs we already have proper documentation
# for
ALREADY_DOCUMENTED = {
    # This list was generated by CompleteApiTest.testGenerateDocumentedNames
    'complex': ['__abs__', '__add__', '__div__', '__eq__', '__floordiv__', '__ge__', '__gt__', '__le__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__', '__pos__', '__pow__', '__sub__', '__truediv__'],
    'dict': ['__contains__', '__delitem__', '__eq__', '__ge__', '__getitem__', '__gt__', '__init__', '__le__', '__lt__', '__ne__', '__setitem__', 'clear', 'copy', 'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values'],
    'float': ['__abs__', '__add__', '__div__', '__eq__', '__floordiv__', '__ge__', '__gt__', '__le__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__', '__pos__', '__pow__', '__sub__', '__truediv__', 'as_integer_ratio', 'fromhex', 'hex'],
    'int': ['__abs__', '__add__', '__and__', '__div__', '__floordiv__', '__index__', '__invert__', '__lshift__', '__mod__', '__mul__', '__neg__', '__or__', '__pos__', '__pow__', '__rshift__', '__sub__', '__truediv__', '__xor__'],
    'list': ['__add__', '__contains__', '__delitem__', '__delslice__', '__eq__', '__ge__', '__getitem__', '__getslice__', '__gt__', '__iadd__', '__imul__', '__le__', '__lt__', '__mul__', '__ne__', '__setitem__', '__setslice__', 'index'],
    'long': ['__abs__', '__add__', '__and__', '__div__', '__floordiv__', '__index__', '__invert__', '__lshift__', '__mod__', '__mul__', '__neg__', '__or__', '__pos__', '__pow__', '__rshift__', '__sub__', '__truediv__', '__xor__'],
    'str': ['__add__', '__contains__', '__eq__', '__ge__', '__getitem__', '__getslice__', '__gt__', '__le__', '__lt__', '__mod__', '__mul__', '__ne__', 'capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill'],
    'tuple': ['__add__', '__contains__', '__eq__', '__ge__', '__getitem__', '__getslice__', '__gt__', '__le__', '__lt__', '__mul__', '__ne__', 'index'],
    'unicode': ['__add__', '__contains__', '__eq__', '__ge__', '__getitem__', '__getslice__', '__gt__', '__le__', '__lt__', '__mod__', '__mul__', '__ne__', 'index', 'isdecimal', 'isnumeric'],
}

NEW_IN_26 = ["int.__format__", "int.__sizeof__", "int.__subclasshook__", "int.__trunc__", "int.conjugate",
    "int.denominator", "int.imag", "int.numerator", "int.real", "float.__format__", "float.__sizeof__",
    "float.__subclasshook__", "float.__trunc__", "float.as_integer_ratio", "float.conjugate",
    "float.fromhex", "float.hex", "float.imag", "float.is_integer", "float.real", "long.__format__",
    "long.__sizeof__", "long.__subclasshook__", "long.__trunc__", "long.conjugate", "long.denominator",
    "long.imag", "long.numerator", "long.real", "bool.__format__", "bool.__sizeof__", "bool.__subclasshook__",
    "bool.__trunc__", "bool.conjugate", "bool.denominator", "bool.imag", "bool.numerator", "bool.real",
    "complex.__format__", "complex.__sizeof__", "complex.__subclasshook__", "list.__format__", "list.__sizeof__",
    "list.__subclasshook__", "dict.__format__", "dict.__sizeof__", "dict.__subclasshook__", "tuple.__format__",
    "tuple.__sizeof__", "tuple.__subclasshook__", "tuple.count", "tuple.index", "str.__format__",
    "str.__sizeof__", "str.__subclasshook__", "str._formatter_field_name_split", "str._formatter_parser",
    "str.format", "unicode.__format__", "unicode.__sizeof__", "unicode.__subclasshook__",
    "unicode._formatter_field_name_split", "unicode._formatter_parser", "unicode.format"]

def indent(s, indent_str):
    indented = ""
    # @type s str
    lines = s.splitlines(True)
    for line in lines:
        indented += indent_str
        indented += line
    return indented

def is_funclike(attr):
    if inspect.ismethod(attr) or inspect.isbuiltin(attr) or inspect.isfunction(attr) or inspect.isroutine(attr):
        return True
    desc = str(type(attr))
    # Can't find a way for inspect.* to identify builtin methods - it returns false on the
    # above checks
    if desc.startswith("<type 'method"):
        return True
    return False

def compute_args(attr):
    try:
        args, vargs, kwargs, defaults = inspect.getargspec(attr)
        # This fails for all the builtins.. but okay for
        # python code
        args_str = ""
        idx = 0
        deflen = len(defaults)
        argslen = len(args)
        argsstart = argslen-deflen
        for arg in args:
            if len(args_str) > 0:
                args_str += ","
            args_str += str(arg)
            if (idx >= argsstart):
                deflt = defaults[idx-argsstart]
                if (type(deflt) == StringType):
                    deflt = "'" + str(deflt) + "'"
                else:
                    deflt = str(deflt)
                args_str += "=" + deflt
            idx += 1

        if vargs:
            if len(args_str) > 0:
                args_str += ","
            args_str += "*" + vargs
        if kwargs:
            if len(args_str) > 0:
                args_str += ","
            args_str += "**" + kwargs

        return "(" + args_str + ")"

    except TypeError:
        args_str = '()'
        try:
            # From something like
            #   float.fromhex(string) -> float
            # infer args=(string)
            # and from something like
            #   x.__rdivmod__(y) <==> divmod(y, x)
            # attempt to infer args = (y)
            doc = inspect.getdoc(attr)
            if doc and len(doc) > 0:
                i = doc.find("<==>")
                if i == -1:
                    i = doc.find("->")
                if i == -1:
                    i = doc.find("\n")
                if i > 0:
                    s = doc[0:i].strip()
                    prev = s[-1]
                    if prev == ")":
                        begin = s.find("(")
                        if begin != -1:
                            end = s.find("[")
                            if end <= 0:
                                end = len(s)
                            args_str = s[begin:end]
                            if not args_str[-1] == ")":
                                args_str += ")"
                            r = []
                            for i in range(len(args_str)):
                                ch = args_str[i]
                                if (ch == "'"):
                                    ch = ""
                                elif ch == '-' or ch == '.':
                                    ch = '_'
                                r.append(ch)
                            args_str = ''.join(r)
        except:
            return ""
    return args_str


def docify(obj, class_name):
    try:
        exclude = ALREADY_DOCUMENTED[class_name]
    except:
        exclude = []

    print ".. class:: " + class_name
    print
    if (obj.__doc__):
        print indent(obj.__doc__, "   ")
        print "\n"

    for name in dir(obj):
        if exclude.__contains__(name):
            # Skip - we already have RST documentation for this element
            continue
        try:
            attr = getattr(obj, name)
        except:
            # What do I do here
            print "some kind of problem with " + name
            continue

        if is_funclike(attr):
            args = compute_args(attr)
            print ".. method:: " + name + args
        else:
            print ".. attribute:: " + name
        print
        if (attr.__doc__):
            print indent(attr.__doc__, "   ")
            print

        # @type x list
        if NEW_IN_26.__contains__(class_name+"."+name):
            print "   .. versionadded:: 2.6"

        print


# Header
print "NetBeans extra documentation:"
print "Documentation for APIs missing from the RST documentation shipping with Python."
print "This is generated from introspecting python code using extract_rst.py."
print "Python version stats:"
print indent(sys.version, "")
print "\n"

# Builtin important types
docify(5, "int")
docify(5.0, "float")
docify(5L, "long")
docify(1 == 1, "bool")
docify(complex(5, 1), "complex")
docify([], "list")
docify({}, "dict")
docify((1, 2), "tuple")
docify("s", "str")
docify(u"s", "unicode")