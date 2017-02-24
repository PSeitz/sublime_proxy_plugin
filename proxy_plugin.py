
class ProxyNavigateToDeclaration(sublime_plugin.TextCommand):
    """
    Provider for the ``proxy_navigate_to_declaration`` command.

    Command navigates to the definition for a symbol in the open file(s) or
    folder(s).
    """

    def __init__(self, args):
        sublime_plugin.TextCommand.__init__(self, args)

    def run(self, edit):
        view = self.view
        language = view.settings().get('syntax')
        if 'Scala' in language:
            view.window().run_command('ensime_go_to_definition')
        else:
            view.window().run_command('navigate_to_definition')
