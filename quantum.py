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

		self.count = 0
		self.password = ""
		self.inputView = self.window.show_input_panel("Password:", "", self.on_done, self.on_change, 0)
		
	def on_done(self, input):
		self.inputView = None
		print("Password: {!s}".format(self.password))

		# output = self.window.create_output_panel("quantum")
		# self.window.run_command("show_panel", {"panel": "output.quantum", "toggle": True})
		self.window.run_command("show_panel", {"panel": "console"})
		print("Connecting to {!s}@{!s}".format(self.username, self.host))

	def on_change(self, input):
		self.count += 1
		if self.count > 100:
			self.count = 0
			print("Recursive loop bug; please fix")
			return
		if hasattr(self, 'inputView') == False or self.inputView == None:
			return
		
		reg = self.inputView.line(0)
		password = self.inputView.substr(reg)
		length = len(password)
		actualLength = len(self.password)

		# Count the number of *s
		stars = 0
		for x in password:
			if x != '*':
				break
			stars += 1
		allStars = stars == length

		# Append to password or prevent changing password
		if allStars and length == actualLength: # Avoid when on_change gets called by hide_password
			return
		if length < actualLength:
			self.inputView.run_command("hide_password", {"length": actualLength})
		else:
			self.password += password[stars:]
			self.inputView.run_command("hide_password", {"length": length})


class HidePasswordCommand(sublime_plugin.TextCommand):
	def run(self, edit, length):
		# Edit the displayed input, replacing it with *s
		reg = self.view.line(0)
		s = ""
		for x in range(length):
			s += '*'
		self.view.replace(edit, reg, s)


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
