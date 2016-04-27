import sublime, sublime_plugin

class TestCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.new_file()

class ConnectCommand(sublime_plugin.WindowCommand):
	def run(self):
		defaultSettings = sublime.load_settings("Default.sublime-settings");
		userSettings = sublime.load_settings("QuantumFTP.sublime-settings");

		self.username = defaultSettings.get("quantum_username")
		if self.username == "":
			self.username = userSettings.get("quantum_username")
		self.host = defaultSettings.get("quantum_host")
		if self.host == "":
			self.host = userSettings.get("quantum_host")

		self.window.show_input_panel("Password?", "", self.on_done, self.on_change, self.on_cancel)

	def on_done(self, input):
		output = self.window.create_output_panel("quantum")
		self.window.run_command("show_panel", {"panel": "console"})
		# self.window.run_command("show_panel", {"panel": "output.quantum", "toggle": True})
		print("Password: {!s}".format(input))
		print("Connecting to {!s}@{!s}".format(self.username, self.host))

	def on_change(self, input):
		print("On change!")

	def on_cancel(self):
		print("You canceled, noob!")

class DefaultSettingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		settingsView = self.window.open_file("Default.sublime-settings")
		settingsView.set_read_only(True)

class UserSettingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		settingsView = self.window.open_file("../User/QuantumFTP.sublime-settings")

# class Test(sublime_plugin.EventListener):
# 	def onPostSave(view):
# 		print view.fileName(), "Saved!"
