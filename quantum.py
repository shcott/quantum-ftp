import sublime, sublime_plugin

class ConnectCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.load_settings("Default.sublime-settings");
		sublime.load_settings("User.sublime-settings");
		username = self.view.settings().get("quantum_username", "null")
		host = self.view.settings().get("quantum_host", "null")
		print("{!s}@{!s}".format(username, host))

class DefaultSettingsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		settingsView = self.view.window().open_file("Default.sublime-settings")
		settingsView.set_read_only(True)

class UserSettingsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		settingsView = self.view.window().open_file("User.sublime-settings")

class TestCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print("Hello")

# class Test(sublime_plugin.EventListener):
# 	def onPostSave(view):
# 		print view.fileName(), "Saved!"
