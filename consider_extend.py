from pylint import lint, reporters, interfaces
from pylint import checkers
from pylint.reporters import text

import astroid

class MyChecker(checkers.BaseChecker):
    __implements__ = interfaces.IAstroidChecker
    name = "foo"
    msgs = {
        'R9991': ("Consider Using %s.extend(%s)",
                  "consider-using-extend",
                  "Consider using list.extend instead of '+=' "
                  "will allow you to use",
                  ),
    }

    def visit_augassign(self, node):
        try:
            for inferred in node.target.infer():
                if inferred.qname() == 'builtins.list':
                    args = (node.target.name, node.value.as_string())
                    self.add_message(
                        'consider-using-extend',
                        node=node, args=args)
        except astroid.InferenceError:
            pass

linter = lint.PyLinter()
linter.register_checker(MyChecker(linter))
args = linter.load_command_line_configuration()
linter.set_reporter(text.TextReporter())
linter.disable('bad-option-value')
with lint.fix_import_path(args):
    linter.check(args)
linter.generate_reports()
