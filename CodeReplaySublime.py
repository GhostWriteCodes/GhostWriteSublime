import sublime
import sublime_plugin
from diff_match_patch import diff_match_patch
import os

# TODO: check commenting, pasting comment
# https://pypl.github.io/IDE.html
# https://stackoverflow.com/questions/55653265/

class Recorder(sublime_plugin.EventListener):
	def __init__(self):
		self.dmp = diff_match_patch()
		self.prev = None
		self.key_file = None
		# op, size
		self.last_diff = {
			'op': '',
			'size': -1,
			'start': -1,
			'count': -1,
		}

	def get_key_name(self, view):
		full_name = view.file_name()
		if not full_name:
			return ''
		base = os.path.dirname(full_name)
		name = os.path.basename(full_name)
		key_name = os.path.join(base, '.{}.keys'.format(name))
		return key_name

	def record(self, key_name):
		if key_name.endswith('.keys.keys'):
			return False

		base = os.path.dirname(key_name)
		checked = set()
		curr = os.path.join(base, "RECORD")
		while curr not in checked:
			if os.path.exists(curr):
				return True
			checked.add(curr)
			base = os.path.dirname(base)
			curr = os.path.join(base, "RECORD")

		return False

	def on_activated(self, view):
		self.prev = view.substr(sublime.Region(0, view.size()))
		key_name = self.get_key_name(view)
		if key_name == '':
			return

		if not self.record(key_name):
			# print('don\'t record')
			return

		if self.key_file is None or self.key_file.name != key_name:
			print('activated', key_name)
			self.key_file = open(key_name, 'a')
			if self.key_file.tell() == 0:
				self.add(0, self.prev)

	def on_deactivated(self, view):
		key_name = self.get_key_name(view)
		if key_name == '':
			return

		print('deactivated', key_name)
		if self.key_file is not None:
			self.key_file.close()
			self.key_file = None

	def on_modified(self, view):
		if self.key_file is None:
			return

		curr = view.substr(sublime.Region(0, view.size()))
		if self.prev is not None:
			diff = self.dmp.diff_main(self.prev, curr)
			self.dmp.diff_cleanupSemantic(diff)
			pos = 0
			for d in diff:
				if d[0] == 1:
					self.add(pos, d[1])
				elif d[0] == -1:
					self.rm(pos, d[1])

				if d[0] > -1:
					pos += len(d[1])

		self.prev = curr

	def repeat(self, op, pos, size):
		return self.last_diff['op'] == op and \
			self.last_diff['size'] == size and \
			self.last_diff['start'] + self.last_diff['count'] == pos

	def add(self, pos, val):
		if self.repeat('+', pos, len(val)):
			prefix = ':'
			self.last_diff['count'] += len(val)
		else:
			prefix = '+{}:{}:'.format(pos, len(val))
			self.last_diff = self.last_diff = {
				'op': '+',
				'size': len(val),
				'start': pos,
				'count': len(val),
			}
		out = '{}{}'.format(prefix, val)
		print(out)  
		self.key_file.write(out)

	def rm(self, pos, val):
		if self.repeat('-', pos, len(val)):
			prefix = ':'
			self.last_diff['count'] -= len(val)
		else:
			prefix = '-{}:{}:'.format(pos, len(val))
			self.last_diff = self.last_diff = {
				'op': '-',
				'size': len(val),
				'start': pos,
				'count': -len(val),
			}
		out = '{}{}'.format(prefix, val)
		print(out)
		# TODO: handle new files
		self.key_file.write(out)
