import sublime, sublime_plugin
from subprocess import Popen, PIPE, check_output
import ftplib

# import sys, os
# sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
# import paramiko
# import pyssh

class ConnectSFTP:
	def connect(self, host, port, username, password):
		return

class ConnectPSFTP(ConnectSFTP):
	def connect(self, host, port, username, password):
		command = "psftp {!s}".format(host)
		if port != 22:
			command += " -P {0}".format(port)
		if username != "":
			command += " -l {!s}".format(username)
		if password != "":
			command += " -pw {!s}".format(password)

		# p = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		# p.stdin.write(b"ls Documents\n")
		# p.stdin.write(b"bye\n")
		# p.stdin.close()

		# print(output)

		with Popen(command.split(), stdin=PIPE, stdout=PIPE, universal_newlines=True, bufsize=1) as p:
			print(p.stdout.readline())
			p.stdin.write("ls Documents\n")
			p.stdin.flush()
			print(p.stdout.readline())

class ConnectFtplib(ConnectSFTP):
	def connect(self, host, port, username, password):
		ftp = ftplib.FTP()
		print("Connecting to {!s}@{!s}..".format(username, host))
		ftp.connect(host, port)
		print("Logging in..")
		ftp.login(username, password)


class ConnectCommand(sublime_plugin.WindowCommand):
	def run(self):
		print("Loading settings..")
		defaultSettings = sublime.load_settings("Default.sublime-settings");
		userSettings = sublime.load_settings("QuantumFTP.sublime-settings");

		self.host = defaultSettings.get("host")
		if self.host == "":
			self.host = userSettings.get("host")
		self.port = defaultSettings.get("port")
		port = userSettings.get("port")
		if port != None:
			self.port = port;
		self.username = defaultSettings.get("username")
		if self.username == "":
			self.username = userSettings.get("username")

		self.count = 0
		self.password = ""
		self.inputView = self.window.show_input_panel("Password:", "", self.on_done, self.on_change, self.on_cancel)

	def on_change(self, input):
		self.count += 1
		if self.count > 1000:
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

	def on_cancel(self):
		self.inputView = None
		self.password = ""
		self.count = 0
		print("Connection canceled.")
		self.window.run_command("show_panel", {"panel": "console"})

	def on_done(self, input):
		self.inputView = None
		self.count = 0

		# output = self.window.create_output_panel("quantum")
		# self.window.run_command("show_panel", {"panel": "output.quantum", "toggle": True})
		self.window.run_command("show_panel", {"panel": "console"})
		sublime.set_timeout_async(self.connect)

	def connect(self):
		c = ConnectPSFTP()
		c.connect(self.host, self.port, self.username, self.password)


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


# class FileEventListener(sublime_plugin.EventListener):
# 	def onPostSave(view):
# 		print view.fileName(), "Saved!"


class TestCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.new_file()
