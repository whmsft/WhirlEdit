##python syntax
class Delegator:

	def __init__(self, delegate=None):
		self.delegate = delegate
		self.__cache = set()
		# Cache is used to only remove added attributes
		# when changing the delegate.

	def __getattr__(self, name):
		attr = getattr(self.delegate, name) # May raise AttributeError
		setattr(self, name, attr)
		self.__cache.add(name)
		return attr

	def resetcache(self):
		"Removes added attributes while leaving original attributes."
		# Function is really about resetting delegator dict
		# to original state.  Cache is just a means
		for key in self.__cache:
			try:
				delattr(self, key)
			except AttributeError:
				pass
		self.__cache.clear()

	def setdelegate(self, delegate):
		"Reset attributes and change delegate."
		self.resetcache()
		self.delegate = delegate

from configparser import ConfigParser
import os
import sys

from tkinter.font import Font
#import idlelib

class InvalidConfigType(Exception): pass
class InvalidConfigSet(Exception): pass
class InvalidTheme(Exception): pass

class IdleConfParser(ConfigParser):
	"""
	A ConfigParser specialised for idle configuration file handling
	"""
	def __init__(self, cfgFile, cfgDefaults=None):
		"""
		cfgFile - string, fully specified configuration file name
		"""
		self.file = cfgFile  # This is currently '' when testing.
		ConfigParser.__init__(self, defaults=cfgDefaults, strict=False)

	def Get(self, section, option, type=None, default=None, raw=False):
		"""
		Get an option value for given section/option or return default.
		If type is specified, return as type.
		"""
		# TODO Use default as fallback, at least if not None
		# Should also print Warning(file, section, option).
		# Currently may raise ValueError
		if not self.has_option(section, option):
			return default
		if type == 'bool':
			return self.getboolean(section, option)
		elif type == 'int':
			return self.getint(section, option)
		else:
			return self.get(section, option, raw=raw)

	def GetOptionList(self, section):
		"Return a list of options for given section, else []."
		if self.has_section(section):
			return self.options(section)
		else:  #return a default value
			return []

	def Load(self):
		"Load the configuration file from disk."
		if self.file:
			self.read(self.file)

class IdleUserConfParser(IdleConfParser):
	"""
	IdleConfigParser specialised for user configuration handling.
	"""

	def SetOption(self, section, option, value):
		"""Return True if option is added or changed to value, else False.
		Add section if required.  False means option already had value.
		"""
		if self.has_option(section, option):
			if self.get(section, option) == value:
				return False
			else:
				self.set(section, option, value)
				return True
		else:
			if not self.has_section(section):
				self.add_section(section)
			self.set(section, option, value)
			return True

	def RemoveOption(self, section, option):
		"""Return True if option is removed from section, else False.
		False if either section does not exist or did not have option.
		"""
		if self.has_section(section):
			return self.remove_option(section, option)
		return False

	def AddSection(self, section):
		"If section doesn't exist, add it."
		if not self.has_section(section):
			self.add_section(section)

	def RemoveEmptySections(self):
		"Remove any sections that have no options."
		for section in self.sections():
			if not self.GetOptionList(section):
				self.remove_section(section)

	def IsEmpty(self):
		"Return True if no sections after removing empty sections."
		self.RemoveEmptySections()
		return not self.sections()

	def Save(self):
		"""Update user configuration file.
		If self not empty after removing empty sections, write the file
		to disk. Otherwise, remove the file from disk if it exists.
		"""
		fname = self.file
		if fname and fname[0] != '#':
			if not self.IsEmpty():
				try:
					cfgFile = open(fname, 'w')
				except OSError:
					os.unlink(fname)
					cfgFile = open(fname, 'w')
				with cfgFile:
					self.write(cfgFile)
			elif os.path.exists(self.file):
				os.remove(self.file)

class IdleConf:
	"""Hold config parsers for all idle config files in singleton instance.
	Default config files, self.defaultCfg --
		for config_type in self.config_types:
			(idle install dir)/config-{config-type}.def
	User config files, self.userCfg --
		for config_type in self.config_types:
		(user home dir)/.idlerc/config-{config-type}.cfg
	"""
	def __init__(self, _utest=False):
		self.config_types = ('main', 'highlight', 'keys', 'extensions')
		self.defaultCfg = {}
		self.userCfg = {}
		self.cfg = {}  # TODO use to select userCfg vs defaultCfg
		# self.blink_off_time = <first editor text>['insertofftime']
		# See https:/bugs.python.org/issue4630, msg356516.

		if not _utest:
			self.CreateConfigHandlers()
			self.LoadCfgFiles()

	def CreateConfigHandlers(self):
		"Populate default and user config parser dictionaries."
		idledir = os.path.dirname(__file__)
		self.userdir = userdir = '' if False else self.GetUserCfgDir()
		for cfg_type in self.config_types:
			self.defaultCfg[cfg_type] = IdleConfParser(
				os.path.join(idledir, f'config-{cfg_type}.def'))
			self.userCfg[cfg_type] = IdleUserConfParser(
				os.path.join(userdir or '#', f'config-{cfg_type}.cfg'))

	def GetUserCfgDir(self):
		"""Return a filesystem directory for storing user config files.
		Creates it if required.
		"""
		cfgDir = '.idlerc'
		userDir = os.path.expanduser('~')
		if userDir != '~': # expanduser() found user home dir
			if not os.path.exists(userDir):
				if not False:
					warn = ('\n Warning: os.path.expanduser("~") points to\n ' +
							userDir + ',\n but the path does not exist.')
					try:
						print(warn, file=sys.stderr)
					except OSError:
						pass
				userDir = '~'
		if userDir == "~": # still no path to home!
			# traditionally IDLE has defaulted to os.getcwd(), is this adequate?
			userDir = os.getcwd()
		userDir = os.path.join(userDir, cfgDir)
		if not os.path.exists(userDir):
			try:
				os.mkdir(userDir)
			except OSError:
				if not False:
					warn = ('\n Warning: unable to create user config directory\n' +
							userDir + '\n Check path and permissions.\n Exiting!\n')
					try:
						print(warn, file=sys.stderr)
					except OSError:
						pass
				raise SystemExit
		# TODO continue without userDIr instead of exit
		return userDir

	def GetOption(self, configType, section, option, default=None, type=None,
				  warn_on_default=True, raw=False):
		"""Return a value for configType section option, or default.
		If type is not None, return a value of that type.  Also pass raw
		to the config parser.  First try to return a valid value
		(including type) from a user configuration. If that fails, try
		the default configuration. If that fails, return default, with a
		default of None.
		Warn if either user or default configurations have an invalid value.
		Warn if default is returned and warn_on_default is True.
		"""
		try:
			if self.userCfg[configType].has_option(section, option):
				return self.userCfg[configType].Get(section, option,
													type=type, raw=raw)
		except ValueError:
			warning = ('\n Warning: config.py - IdleConf.GetOption -\n'
					   ' invalid %r value for configuration option %r\n'
					   ' from section %r: %r' %
					   (type, option, section,
					   self.userCfg[configType].Get(section, option, raw=raw)))
			_warn(warning, configType, section, option)
		try:
			if self.defaultCfg[configType].has_option(section,option):
				return self.defaultCfg[configType].Get(
						section, option, type=type, raw=raw)
		except ValueError:
			pass
		#returning default, print warning
		if warn_on_default:
			warning = ('\n Warning: config.py - IdleConf.GetOption -\n'
					   ' problem retrieving configuration option %r\n'
					   ' from section %r.\n'
					   ' returning default value: %r' %
					   (option, section, default))
			_warn(warning, configType, section, option)
		return default

	def SetOption(self, configType, section, option, value):
		"""Set section option to value in user config file."""
		self.userCfg[configType].SetOption(section, option, value)

	def GetSectionList(self, configSet, configType):
		"""Return sections for configSet configType configuration.
		configSet must be either 'user' or 'default'
		configType must be in self.config_types.
		"""
		if not (configType in self.config_types):
			raise InvalidConfigType('Invalid configType specified')
		if configSet == 'user':
			cfgParser = self.userCfg[configType]
		elif configSet == 'default':
			cfgParser=self.defaultCfg[configType]
		else:
			raise InvalidConfigSet('Invalid configSet specified')
		return cfgParser.sections()

	def GetHighlight(self, theme, element):
		"""Return dict of theme element highlight colors.
		The keys are 'foreground' and 'background'.  The values are
		tkinter color strings for configuring backgrounds and tags.
		"""
		cfg = ('default' if self.defaultCfg['highlight'].has_section(theme)
			   else 'user')
		theme_dict = self.GetThemeDict(cfg, theme)
		fore = theme_dict[element + '-foreground']
		if element == 'cursor':
			element = 'normal'
		back = "#333333"#theme_dict[element + '-background']
		return {"foreground": fore, "background": back}

	def GetThemeDict(self, type, themeName):
		"""Return {option:value} dict for elements in themeName.
		type - string, 'default' or 'user' theme type
		themeName - string, theme name
		Values are loaded over ultimate fallback defaults to guarantee
		that all theme elements are present in a newly created theme.
		"""
		if type == 'user':
			cfgParser = self.userCfg['highlight']
		elif type == 'default':
			cfgParser = self.defaultCfg['highlight']
		else:
			raise InvalidTheme('Invalid theme type specified')
		# Provide foreground and background colors for each theme
		# element (other than cursor) even though some values are not
		# yet used by idle, to allow for their use in the future.
		# Default values are generally black and white.
		# TODO copy theme from a class attribute.
		theme ={"keyword-foreground" : "#F92672",
				"keyword-background" : "#333333",
				"builtin-foreground" : "#66D9EF",
				"builtin-background" : "#333333",
				"comment-foreground" : "#75715E",
				"comment-background" : "#737373",
				"string-foreground"  : "#FD971F",
				"string-background"  : "#333333",
				"definition-foreground" : "#A6E22E",
				"definition-background" : "#333333",
				"hilite-foreground" : "#F8F8F2",
				"hilite-background" : "gray"   ,
				"break-foreground"  : "black"  ,
				"break-background"  : "#ffff55",
				"hit-foreground"    : "#F8F8F2",
				"hit-background"    : "#171812",
				"error-foreground"  : "#ff3338",
				"error-background"  : "#333333",
				"cursor-foreground" : "#F8F8F2",
				"stdout-foreground" : "#DDDDDD",
				"stdout-background" : "#333333",
				"stderr-foreground" : "#ff3338",
				"stderr-background" : "#333333",
				"console-foreground": "#75715E",
				"console-background" :"#333333",
				}
		'''for element in theme:
			if not (cfgParser.has_option(themeName, element) or
					# Skip warning for new elements.
					element.startswith(('context-', 'linenumber-'))):
				# Print warning that will return a default color
				warning = ('\n Warning: config.IdleConf.GetThemeDict'
						   ' -\n problem retrieving theme element %r'
						   '\n from theme %r.\n'
						   ' returning default color: %r' %
						   (element, themeName, theme[element]))
				_warn(warning, 'highlight', themeName, element)
			theme[element] = cfgParser.Get(
					themeName, element, default=theme[element])'''
		return theme

	def CurrentTheme(self):
		"Return the name of the currently active text color theme."
		return self.current_colors_and_keys('Theme')

	def CurrentKeys(self):
		"""Return the name of the currently active key set."""
		return self.current_colors_and_keys('Keys')

	def current_colors_and_keys(self, section):
		"""Return the currently active name for Theme or Keys section.
		idlelib.config-main.def ('default') includes these sections
		[Theme]
		default= 1
		name= IDLE Classic
		name2=
		[Keys]
		default= 1
		name=
		name2=
		Item 'name2', is used for built-in ('default') themes and keys
		added after 2015 Oct 1 and 2016 July 1.  This kludge is needed
		because setting 'name' to a builtin not defined in older IDLEs
		to display multiple error messages or quit.
		See https://bugs.python.org/issue25313.
		When default = True, 'name2' takes precedence over 'name',
		while older IDLEs will just use name.  When default = False,
		'name2' may still be set, but it is ignored.
		"""
		cfgname = 'highlight' if section == 'Theme' else 'keys'
		default = self.GetOption('main', section, 'default',
								 type='bool', default=True)
		name = ''
		if default:
			name = self.GetOption('main', section, 'name2', default='')
		if not name:
			name = self.GetOption('main', section, 'name', default='')
		if name:
			source = self.defaultCfg if default else self.userCfg
			if source[cfgname].has_section(name):
				return name
		return "IDLE Classic" if section == 'Theme' else self.default_keys()

	@staticmethod
	def default_keys():
		if sys.platform[:3] == 'win':
			return 'IDLE Classic Windows'
		elif sys.platform == 'darwin':
			return 'IDLE Classic OSX'
		else:
			return 'IDLE Modern Unix'

	def GetExtensions(self, active_only=True,
					  editor_only=False, shell_only=False):
		"""Return extensions in default and user config-extensions files.
		If active_only True, only return active (enabled) extensions
		and optionally only editor or shell extensions.
		If active_only False, return all extensions.
		"""
		extns = self.RemoveKeyBindNames(
				self.GetSectionList('default', 'extensions'))
		userExtns = self.RemoveKeyBindNames(
				self.GetSectionList('user', 'extensions'))
		for extn in userExtns:
			if extn not in extns: #user has added own extension
				extns.append(extn)
		for extn in ('AutoComplete','CodeContext',
					 'FormatParagraph','ParenMatch'):
			extns.remove(extn)
			# specific exclusions because we are storing config for mainlined old
			# extensions in config-extensions.def for backward compatibility
		if active_only:
			activeExtns = []
			for extn in extns:
				if self.GetOption('extensions', extn, 'enable', default=True,
								  type='bool'):
					#the extension is enabled
					if editor_only or shell_only:  # TODO both True contradict
						if editor_only:
							option = "enable_editor"
						else:
							option = "enable_shell"
						if self.GetOption('extensions', extn,option,
										  default=True, type='bool',
										  warn_on_default=False):
							activeExtns.append(extn)
					else:
						activeExtns.append(extn)
			return activeExtns
		else:
			return extns

	def RemoveKeyBindNames(self, extnNameList):
		"Return extnNameList with keybinding section names removed."
		return [n for n in extnNameList if not n.endswith(('_bindings', '_cfgBindings'))]

	def GetExtnNameForEvent(self, virtualEvent):
		"""Return the name of the extension binding virtualEvent, or None.
		virtualEvent - string, name of the virtual event to test for,
					   without the enclosing '<< >>'
		"""
		extName = None
		vEvent = '<<' + virtualEvent + '>>'
		for extn in self.GetExtensions(active_only=0):
			for event in self.GetExtensionKeys(extn):
				if event == vEvent:
					extName = extn  # TODO return here?
		return extName

	def GetExtensionKeys(self, extensionName):
		"""Return dict: {configurable extensionName event : active keybinding}.
		Events come from default config extension_cfgBindings section.
		Keybindings come from GetCurrentKeySet() active key dict,
		where previously used bindings are disabled.
		"""
		keysName = extensionName + '_cfgBindings'
		activeKeys = self.GetCurrentKeySet()
		extKeys = {}
		if self.defaultCfg['extensions'].has_section(keysName):
			eventNames = self.defaultCfg['extensions'].GetOptionList(keysName)
			for eventName in eventNames:
				event = '<<' + eventName + '>>'
				binding = activeKeys[event]
				extKeys[event] = binding
		return extKeys

	def __GetRawExtensionKeys(self,extensionName):
		"""Return dict {configurable extensionName event : keybinding list}.
		Events come from default config extension_cfgBindings section.
		Keybindings list come from the splitting of GetOption, which
		tries user config before default config.
		"""
		keysName = extensionName+'_cfgBindings'
		extKeys = {}
		if self.defaultCfg['extensions'].has_section(keysName):
			eventNames = self.defaultCfg['extensions'].GetOptionList(keysName)
			for eventName in eventNames:
				binding = self.GetOption(
						'extensions', keysName, eventName, default='').split()
				event = '<<' + eventName + '>>'
				extKeys[event] = binding
		return extKeys

	def GetExtensionBindings(self, extensionName):
		"""Return dict {extensionName event : active or defined keybinding}.
		Augment self.GetExtensionKeys(extensionName) with mapping of non-
		configurable events (from default config) to GetOption splits,
		as in self.__GetRawExtensionKeys.
		"""
		bindsName = extensionName + '_bindings'
		extBinds = self.GetExtensionKeys(extensionName)
		#add the non-configurable bindings
		if self.defaultCfg['extensions'].has_section(bindsName):
			eventNames = self.defaultCfg['extensions'].GetOptionList(bindsName)
			for eventName in eventNames:
				binding = self.GetOption(
						'extensions', bindsName, eventName, default='').split()
				event = '<<' + eventName + '>>'
				extBinds[event] = binding

		return extBinds

	def GetKeyBinding(self, keySetName, eventStr):
		"""Return the keybinding list for keySetName eventStr.
		keySetName - name of key binding set (config-keys section).
		eventStr - virtual event, including brackets, as in '<<event>>'.
		"""
		eventName = eventStr[2:-2] #trim off the angle brackets
		binding = self.GetOption('keys', keySetName, eventName, default='',
								 warn_on_default=False).split()
		return binding

	def GetCurrentKeySet(self):
		"Return CurrentKeys with 'darwin' modifications."
		result = self.GetKeySet(self.CurrentKeys())

		if sys.platform == "darwin":
			# macOS (OS X) Tk variants do not support the "Alt"
			# keyboard modifier.  Replace it with "Option".
			# TODO (Ned?): the "Option" modifier does not work properly
			#     for Cocoa Tk and XQuartz Tk so we should not use it
			#     in the default 'OSX' keyset.
			for k, v in result.items():
				v2 = [ x.replace('<Alt-', '<Option-') for x in v ]
				if v != v2:
					result[k] = v2

		return result

	def GetKeySet(self, keySetName):
		"""Return event-key dict for keySetName core plus active extensions.
		If a binding defined in an extension is already in use, the
		extension binding is disabled by being set to ''
		"""
		keySet = self.GetCoreKeys(keySetName)
		activeExtns = self.GetExtensions(active_only=1)
		for extn in activeExtns:
			extKeys = self.__GetRawExtensionKeys(extn)
			if extKeys: #the extension defines keybindings
				for event in extKeys:
					if extKeys[event] in keySet.values():
						#the binding is already in use
						extKeys[event] = '' #disable this binding
					keySet[event] = extKeys[event] #add binding
		return keySet

	def IsCoreBinding(self, virtualEvent):
		"""Return True if the virtual event is one of the core idle key events.
		virtualEvent - string, name of the virtual event to test for,
					   without the enclosing '<< >>'
		"""
		return ('<<'+virtualEvent+'>>') in self.GetCoreKeys()

# TODO make keyBindins a file or class attribute used for test above
# and copied in function below.

	former_extension_events = {  #  Those with user-configurable keys.
		'<<force-open-completions>>', '<<expand-word>>',
		'<<force-open-calltip>>', '<<flash-paren>>', '<<format-paragraph>>',
		 '<<run-module>>', '<<check-module>>', '<<zoom-height>>',
		 '<<run-custom>>',
		 }

	def GetCoreKeys(self, keySetName=None):
		"""Return dict of core virtual-key keybindings for keySetName.
		The default keySetName None corresponds to the keyBindings base
		dict. If keySetName is not None, bindings from the config
		file(s) are loaded _over_ these defaults, so if there is a
		problem getting any core binding there will be an 'ultimate last
		resort fallback' to the CUA-ish bindings defined here.
		"""
		keyBindings={
			'<<copy>>': ['<Control-c>', '<Control-C>'],
			'<<cut>>': ['<Control-x>', '<Control-X>'],
			'<<paste>>': ['<Control-v>', '<Control-V>'],
			'<<beginning-of-line>>': ['<Control-a>', '<Home>'],
			'<<center-insert>>': ['<Control-l>'],
			'<<close-all-windows>>': ['<Control-q>'],
			'<<close-window>>': ['<Alt-F4>'],
			'<<do-nothing>>': ['<Control-x>'],
			'<<end-of-file>>': ['<Control-d>'],
			'<<python-docs>>': ['<F1>'],
			'<<python-context-help>>': ['<Shift-F1>'],
			'<<history-next>>': ['<Alt-n>'],
			'<<history-previous>>': ['<Alt-p>'],
			'<<interrupt-execution>>': ['<Control-c>'],
			'<<view-restart>>': ['<F6>'],
			'<<restart-shell>>': ['<Control-F6>'],
			'<<open-class-browser>>': ['<Alt-c>'],
			'<<open-module>>': ['<Alt-m>'],
			'<<open-new-window>>': ['<Control-n>'],
			'<<open-window-from-file>>': ['<Control-o>'],
			'<<plain-newline-and-indent>>': ['<Control-j>'],
			'<<print-window>>': ['<Control-p>'],
			'<<redo>>': ['<Control-y>'],
			'<<remove-selection>>': ['<Escape>'],
			'<<save-copy-of-window-as-file>>': ['<Alt-Shift-S>'],
			'<<save-window-as-file>>': ['<Alt-s>'],
			'<<save-window>>': ['<Control-s>'],
			'<<select-all>>': ['<Alt-a>'],
			'<<toggle-auto-coloring>>': ['<Control-slash>'],
			'<<undo>>': ['<Control-z>'],
			'<<find-again>>': ['<Control-g>', '<F3>'],
			'<<find-in-files>>': ['<Alt-F3>'],
			'<<find-selection>>': ['<Control-F3>'],
			'<<find>>': ['<Control-f>'],
			'<<replace>>': ['<Control-h>'],
			'<<goto-line>>': ['<Alt-g>'],
			'<<smart-backspace>>': ['<Key-BackSpace>'],
			'<<newline-and-indent>>': ['<Key-Return>', '<Key-KP_Enter>'],
			'<<smart-indent>>': ['<Key-Tab>'],
			'<<indent-region>>': ['<Control-Key-bracketright>'],
			'<<dedent-region>>': ['<Control-Key-bracketleft>'],
			'<<comment-region>>': ['<Alt-Key-3>'],
			'<<uncomment-region>>': ['<Alt-Key-4>'],
			'<<tabify-region>>': ['<Alt-Key-5>'],
			'<<untabify-region>>': ['<Alt-Key-6>'],
			'<<toggle-tabs>>': ['<Alt-Key-t>'],
			'<<change-indentwidth>>': ['<Alt-Key-u>'],
			'<<del-word-left>>': ['<Control-Key-BackSpace>'],
			'<<del-word-right>>': ['<Control-Key-Delete>'],
			'<<force-open-completions>>': ['<Control-Key-space>'],
			'<<expand-word>>': ['<Alt-Key-slash>'],
			'<<force-open-calltip>>': ['<Control-Key-backslash>'],
			'<<flash-paren>>': ['<Control-Key-0>'],
			'<<format-paragraph>>': ['<Alt-Key-q>'],
			'<<run-module>>': ['<Key-F5>'],
			'<<run-custom>>': ['<Shift-Key-F5>'],
			'<<check-module>>': ['<Alt-Key-x>'],
			'<<zoom-height>>': ['<Alt-Key-2>'],
			}

		if keySetName:
			if not (self.userCfg['keys'].has_section(keySetName) or
					self.defaultCfg['keys'].has_section(keySetName)):
				warning = (
					'\n Warning: config.py - IdleConf.GetCoreKeys -\n'
					' key set %r is not defined, using default bindings.' %
					(keySetName,)
				)
				_warn(warning, 'keys', keySetName)
			else:
				for event in keyBindings:
					binding = self.GetKeyBinding(keySetName, event)
					if binding:
						keyBindings[event] = binding
					# Otherwise return default in keyBindings.
					elif event not in self.former_extension_events:
						warning = (
							'\n Warning: config.py - IdleConf.GetCoreKeys -\n'
							' problem retrieving key binding for event %r\n'
							' from key set %r.\n'
							' returning default value: %r' %
							(event, keySetName, keyBindings[event])
						)
						_warn(warning, 'keys', keySetName, event)
		return keyBindings

	def GetExtraHelpSourceList(self, configSet):
		"""Return list of extra help sources from a given configSet.
		Valid configSets are 'user' or 'default'.  Return a list of tuples of
		the form (menu_item , path_to_help_file , option), or return the empty
		list.  'option' is the sequence number of the help resource.  'option'
		values determine the position of the menu items on the Help menu,
		therefore the returned list must be sorted by 'option'.
		"""
		helpSources = []
		if configSet == 'user':
			cfgParser = self.userCfg['main']
		elif configSet == 'default':
			cfgParser = self.defaultCfg['main']
		else:
			raise InvalidConfigSet('Invalid configSet specified')
		options=cfgParser.GetOptionList('HelpFiles')
		for option in options:
			value=cfgParser.Get('HelpFiles', option, default=';')
			if value.find(';') == -1: #malformed config entry with no ';'
				menuItem = '' #make these empty
				helpPath = '' #so value won't be added to list
			else: #config entry contains ';' as expected
				value=value.split(';')
				menuItem=value[0].strip()
				helpPath=value[1].strip()
			if menuItem and helpPath: #neither are empty strings
				helpSources.append( (menuItem,helpPath,option) )
		helpSources.sort(key=lambda x: x[2])
		return helpSources

	def GetAllExtraHelpSourcesList(self):
		"""Return a list of the details of all additional help sources.
		Tuples in the list are those of GetExtraHelpSourceList.
		"""
		allHelpSources = (self.GetExtraHelpSourceList('default') +
				self.GetExtraHelpSourceList('user') )
		return allHelpSources

	def GetFont(self, root, configType, section):
		"""Retrieve a font from configuration (font, font-size, font-bold)
		Intercept the special value 'TkFixedFont' and substitute
		the actual font, factoring in some tweaks if needed for
		appearance sakes.
		The 'root' parameter can normally be any valid Tkinter widget.
		Return a tuple (family, size, weight) suitable for passing
		to tkinter.Font
		"""
		family = self.GetOption(configType, section, 'font', default='courier')
		size = self.GetOption(configType, section, 'font-size', type='int',
							  default='10')
		bold = self.GetOption(configType, section, 'font-bold', default=0,
							  type='bool')
		if (family == 'TkFixedFont'):
			f = Font(name='TkFixedFont', exists=True, root=root)
			actualFont = Font.actual(f)
			family = actualFont['family']
			size = actualFont['size']
			if size <= 0:
				size = 10  # if font in pixels, ignore actual size
			bold = actualFont['weight'] == 'bold'
		return (family, size, 'bold' if bold else 'normal')

	def LoadCfgFiles(self):
		"Load all configuration files."
		for key in self.defaultCfg:
			self.defaultCfg[key].Load()
			self.userCfg[key].Load() #same keys

	def SaveUserCfgFiles(self):
		"Write all loaded user configuration files to disk."
		for key in self.userCfg:
			self.userCfg[key].Save()


idleConf = IdleConf()

_warned = set()
def _warn(msg, *key):
	key = (msg,) + key
	if key not in _warned:
		try:
			print(msg, file=sys.stderr)
		except OSError:
			pass
		_warned.add(key)


class ConfigChanges(dict):
	"""Manage a user's proposed configuration option changes.
	Names used across multiple methods:
		page -- one of the 4 top-level dicts representing a
				.idlerc/config-x.cfg file.
		config_type -- name of a page.
		section -- a section within a page/file.
		option -- name of an option within a section.
		value -- value for the option.
	Methods
		add_option: Add option and value to changes.
		save_option: Save option and value to config parser.
		save_all: Save all the changes to the config parser and file.
		delete_section: If section exists,
						delete from changes, userCfg, and file.
		clear: Clear all changes by clearing each page.
	"""
	def __init__(self):
		"Create a page for each configuration file"
		self.pages = []  # List of unhashable dicts.
		for config_type in idleConf.config_types:
			self[config_type] = {}
			self.pages.append(self[config_type])

	def add_option(self, config_type, section, item, value):
		"Add item/value pair for config_type and section."
		page = self[config_type]
		value = str(value)  # Make sure we use a string.
		if section not in page:
			page[section] = {}
		page[section][item] = value

	@staticmethod
	def save_option(config_type, section, item, value):
		"""Return True if the configuration value was added or changed.
		Helper for save_all.
		"""
		if idleConf.defaultCfg[config_type].has_option(section, item):
			if idleConf.defaultCfg[config_type].Get(section, item) == value:
				# The setting equals a default setting, remove it from user cfg.
				return idleConf.userCfg[config_type].RemoveOption(section, item)
		# If we got here, set the option.
		return idleConf.userCfg[config_type].SetOption(section, item, value)

	def save_all(self):
		"""Save configuration changes to the user config file.
		Clear self in preparation for additional changes.
		Return changed for testing.
		"""
		idleConf.userCfg['main'].Save()

		changed = False
		for config_type in self:
			cfg_type_changed = False
			page = self[config_type]
			for section in page:
				if section == 'HelpFiles':  # Remove it for replacement.
					idleConf.userCfg['main'].remove_section('HelpFiles')
					cfg_type_changed = True
				for item, value in page[section].items():
					if self.save_option(config_type, section, item, value):
						cfg_type_changed = True
			if cfg_type_changed:
				idleConf.userCfg[config_type].Save()
				changed = True
		for config_type in ['keys', 'highlight']:
			# Save these even if unchanged!
			idleConf.userCfg[config_type].Save()
		self.clear()
		# ConfigDialog caller must add the following call
		# self.save_all_changed_extensions()  # Uses a different mechanism.
		return changed

	def delete_section(self, config_type, section):
		"""Delete a section from self, userCfg, and file.
		Used to delete custom themes and keysets.
		"""
		if section in self[config_type]:
			del self[config_type][section]
		configpage = idleConf.userCfg[config_type]
		configpage.remove_section(section)
		configpage.Save()

	def clear(self):
		"""Clear all 4 pages.
		Called in save_all after saving to idleConf.
		XXX Mark window *title* when there are changes; unmark here.
		"""
		for page in self.pages:
			page.clear()


# TODO Revise test output, write expanded unittest
def _dump():  # htest # (not really, but ignore in coverage)
	from zlib import crc32
	line, crc = 0, 0

	def sprint(obj):
		global line, crc
		txt = str(obj)
		line += 1
		crc = crc32(txt.encode(encoding='utf-8'), crc)
		print(txt)
		#print('***', line, crc, '***')  # Uncomment for diagnosis.

	def dumpCfg(cfg):
		print('\n', cfg, '\n')  # Cfg has variable '0xnnnnnnnn' address.
		for key in sorted(cfg.keys()):
			sections = cfg[key].sections()
			sprint(key)
			sprint(sections)
			for section in sections:
				options = cfg[key].options(section)
				sprint(section)
				sprint(options)
				for option in options:
					sprint(option + ' = ' + cfg[key].Get(section, option))

	dumpCfg(idleConf.defaultCfg)
	dumpCfg(idleConf.userCfg)
	print('\nlines = ', line, ', crc = ', crc, sep='')

import builtins
import keyword
import re
import time

DEBUG = False

def any(name, alternates):
	"Return a named group pattern matching list of alternates."
	return "(?P<%s>" % name + "|".join(alternates) + ")"


def make_pat():
	kw = r"\b" + any("KEYWORD", keyword.kwlist) + r"\b"
	builtinlist = [str(name) for name in dir(builtins)
				   if not name.startswith('_') and
				   name not in keyword.kwlist]
	builtin = r"([^.'\"\\#]\b|^)" + any("BUILTIN", builtinlist) + r"\b"
	comment = any("COMMENT", [r"#[^\n]*"])
	stringprefix = r"(?i:r|u|f|fr|rf|b|br|rb)?"
	sqstring = stringprefix + r"'[^'\\\n]*(\\.[^'\\\n]*)*'?"
	dqstring = stringprefix + r'"[^"\\\n]*(\\.[^"\\\n]*)*"?'
	sq3string = stringprefix + r"'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"
	dq3string = stringprefix + r'"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'
	string = any("STRING", [sq3string, dq3string, sqstring, dqstring])
	return (kw + "|" + builtin + "|" + comment + "|" + string +
			"|" + any("SYNC", [r"\n"]))


prog = re.compile(make_pat(), re.S)
idprog = re.compile(r"\s+(\w+)", re.S)


def color_config(text):
	"""Set color options of Text widget.
	If ColorDelegator is used, this should be called first.
	"""
	# Called from htest, TextFrame, Editor, and Turtledemo.
	# Not automatic because ColorDelegator does not know 'text'.
	theme = "IDLE Classic"
	'''{"keyword-foreground" : "#F92672",
				"keyword-background" : "#333333",
				"builtin-foreground" : "#66D9EF",
				"builtin-background" : "#333333",
				"comment-foreground" : "#75715E",
				"comment-background" : "#737373",
				"string-foreground"  : "#FD971F",
				"string-background"  : "#333333",
				"definition-foreground" : "#A6E22E",
				"definition-background" : "#333333",
				"hilite-foreground" : "#F8F8F2",
				"hilite-background" : "gray"   ,
				"break-foreground"  : "black"  ,
				"break-background"  : "#ffff55",
				"hit-foreground"    : "#F8F8F2",
				"hit-background"    : "#171812",
				"error-foreground"  : "#ff3338",
				"error-background"  : "#333333",
				"cursor-foreground" : "#F8F8F2",
				"stdout-foreground" : "#DDDDDD",
				"stdout-background" : "#333333",
				"stderr-foreground" : "#ff3338",
				"stderr-background" : "#333333",
				"console-foreground": "#75715E",
				"console-background" :"#333333",
				}'''
	normal_colors = idleConf.GetHighlight(theme, 'normal')
	cursor_color = idleConf.GetHighlight(theme, 'cursor')['foreground']
	select_colors = idleConf.GetHighlight(theme, 'hilite')
	text.config(
		foreground=normal_colors['foreground'],
		background=normal_colors['background'],
		insertbackground=cursor_color,
		selectforeground=select_colors['foreground'],
		selectbackground=select_colors['background'],
		inactiveselectbackground=select_colors['background'],  # new in 8.5
		)


class ColorDelegator(Delegator):
	"""Delegator for syntax highlighting (text coloring).
	Instance variables:
		delegate: Delegator below this one in the stack, meaning the
				one this one delegates to.
		Used to track state:
		after_id: Identifier for scheduled after event, which is a
				timer for colorizing the text.
		allow_colorizing: Boolean toggle for applying colorizing.
		colorizing: Boolean flag when colorizing is in process.
		stop_colorizing: Boolean flag to end an active colorizing
				process.
	"""

	def __init__(self):
		Delegator.__init__(self)
		self.init_state()
		self.prog = prog
		self.idprog = idprog
		self.LoadTagDefs()

	def init_state(self):
		"Initialize variables that track colorizing state."
		self.after_id = None
		self.allow_colorizing = True
		self.stop_colorizing = False
		self.colorizing = False

	def setdelegate(self, delegate):
		"""Set the delegate for this instance.
		A delegate is an instance of a Delegator class and each
		delegate points to the next delegator in the stack.  This
		allows multiple delegators to be chained together for a
		widget.  The bottom delegate for a colorizer is a Text
		widget.
		If there is a delegate, also start the colorizing process.
		"""
		if self.delegate is not None:
			self.unbind("<<toggle-auto-coloring>>")
		Delegator.setdelegate(self, delegate)
		if delegate is not None:
			self.config_colors()
			self.bind("<<toggle-auto-coloring>>", self.toggle_colorize_event)
			self.notify_range("1.0", "end")
		else:
			# No delegate - stop any colorizing.
			self.stop_colorizing = True
			self.allow_colorizing = False

	def config_colors(self):
		"Configure text widget tags with colors from tagdefs."
		for tag, cnf in self.tagdefs.items():
			self.tag_configure(tag, **cnf)
		self.tag_raise('sel')

	def LoadTagDefs(self):
		"Create dictionary of tag names to text colors."
		theme = idleConf.CurrentTheme()
		self.tagdefs = {
			"COMMENT": idleConf.GetHighlight(theme, "comment"),
			"KEYWORD": idleConf.GetHighlight(theme, "keyword"),
			"BUILTIN": idleConf.GetHighlight(theme, "builtin"),
			"STRING": idleConf.GetHighlight(theme, "string"),
			"DEFINITION": idleConf.GetHighlight(theme, "definition"),
			"SYNC": {'background': None, 'foreground': None},
			"TODO": {'background': None, 'foreground': None},
			"ERROR": idleConf.GetHighlight(theme, "error"),
			# "hit" is used by ReplaceDialog to mark matches. It shouldn't be changed by Colorizer, but
			# that currently isn't technically possible. This should be moved elsewhere in the future
			# when fixing the "hit" tag's visibility, or when the replace dialog is replaced with a
			# non-modal alternative.
			"hit": idleConf.GetHighlight(theme, "hit"),
			}

		if DEBUG: print('tagdefs', self.tagdefs)

	def insert(self, index, chars, tags=None):
		"Insert chars into widget at index and mark for colorizing."
		index = self.index(index)
		self.delegate.insert(index, chars, tags)
		self.notify_range(index, index + "+%dc" % len(chars))

	def delete(self, index1, index2=None):
		"Delete chars between indexes and mark for colorizing."
		index1 = self.index(index1)
		self.delegate.delete(index1, index2)
		self.notify_range(index1)

	def notify_range(self, index1, index2=None):
		"Mark text changes for processing and restart colorizing, if active."
		self.tag_add("TODO", index1, index2)
		if self.after_id:
			if DEBUG: print("colorizing already scheduled")
			return
		if self.colorizing:
			self.stop_colorizing = True
			if DEBUG: print("stop colorizing")
		if self.allow_colorizing:
			if DEBUG: print("schedule colorizing")
			self.after_id = self.after(1, self.recolorize)
		return

	def close(self):
		if self.after_id:
			after_id = self.after_id
			self.after_id = None
			if DEBUG: print("cancel scheduled recolorizer")
			self.after_cancel(after_id)
		self.allow_colorizing = False
		self.stop_colorizing = True

	def toggle_colorize_event(self, event=None):
		"""Toggle colorizing on and off.
		When toggling off, if colorizing is scheduled or is in
		process, it will be cancelled and/or stopped.
		When toggling on, colorizing will be scheduled.
		"""
		if self.after_id:
			after_id = self.after_id
			self.after_id = None
			if DEBUG: print("cancel scheduled recolorizer")
			self.after_cancel(after_id)
		if self.allow_colorizing and self.colorizing:
			if DEBUG: print("stop colorizing")
			self.stop_colorizing = True
		self.allow_colorizing = not self.allow_colorizing
		if self.allow_colorizing and not self.colorizing:
			self.after_id = self.after(1, self.recolorize)
		if DEBUG:
			print("auto colorizing turned",
				  "on" if self.allow_colorizing else "off")
		return "break"

	def recolorize(self):
		"""Timer event (every 1ms) to colorize text.
		Colorizing is only attempted when the text widget exists,
		when colorizing is toggled on, and when the colorizing
		process is not already running.
		After colorizing is complete, some cleanup is done to
		make sure that all the text has been colorized.
		"""
		self.after_id = None
		if not self.delegate:
			if DEBUG: print("no delegate")
			return
		if not self.allow_colorizing:
			if DEBUG: print("auto colorizing is off")
			return
		if self.colorizing:
			if DEBUG: print("already colorizing")
			return
		try:
			self.stop_colorizing = False
			self.colorizing = True
			if DEBUG: print("colorizing...")
			t0 = time.perf_counter()
			self.recolorize_main()
			t1 = time.perf_counter()
			if DEBUG: print("%.3f seconds" % (t1-t0))
		finally:
			self.colorizing = False
		if self.allow_colorizing and self.tag_nextrange("TODO", "1.0"):
			if DEBUG: print("reschedule colorizing")
			self.after_id = self.after(1, self.recolorize)

	def recolorize_main(self):
		"Evaluate text and apply colorizing tags."
		next = "1.0"
		while True:
			item = self.tag_nextrange("TODO", next)
			if not item:
				break
			head, tail = item
			self.tag_remove("SYNC", head, tail)
			item = self.tag_prevrange("SYNC", head)
			head = item[1] if item else "1.0"

			chars = ""
			next = head
			lines_to_get = 1
			ok = False
			while not ok:
				mark = next
				next = self.index(mark + "+%d lines linestart" %
										 lines_to_get)
				lines_to_get = min(lines_to_get * 2, 100)
				ok = "SYNC" in self.tag_names(next + "-1c")
				line = self.get(mark, next)
				##print head, "get", mark, next, "->", repr(line)
				if not line:
					return
				for tag in self.tagdefs:
					self.tag_remove(tag, mark, next)
				chars = chars + line
				m = self.prog.search(chars)
				while m:
					for key, value in m.groupdict().items():
						if value:
							a, b = m.span(key)
							self.tag_add(key,
										 head + "+%dc" % a,
										 head + "+%dc" % b)
							if value in ("def", "class"):
								m1 = self.idprog.match(chars, b)
								if m1:
									a, b = m1.span(1)
									self.tag_add("DEFINITION",
												 head + "+%dc" % a,
												 head + "+%dc" % b)
					m = self.prog.search(chars, m.end())
				if "SYNC" in self.tag_names(next + "-1c"):
					head = next
					chars = ""
				else:
					ok = False
				if not ok:
					# We're in an inconsistent state, and the call to
					# update may tell us to stop.  It may also change
					# the correct value for "next" (since this is a
					# line.col string, not a true mark).  So leave a
					# crumb telling the next invocation to resume here
					# in case update tells us to leave.
					self.tag_add("TODO", next)
				self.update()
				if self.stop_colorizing:
					if DEBUG: print("colorizing stopped")
					return

	def removecolors(self):
		"Remove all colorizing tags."
		for tag in self.tagdefs:
			self.tag_remove(tag, "1.0", "end")


def _color_delegator(parent):  # htest #
	from tkinter import Toplevel, Text

	top = Toplevel(parent)
	top.title("Test ColorDelegator")
	x, y = map(int, parent.geometry().split('+')[1:])
	top.geometry("700x250+%d+%d" % (x + 20, y + 175))
	source = (
		"if True: int ('1') # keyword, builtin, string, comment\n"
		"elif False: print(0)\n"
		"else: float(None)\n"
		"if iF + If + IF: 'keyword matching must respect case'\n"
		"if'': x or''  # valid keyword-string no-space combinations\n"
		"async def f(): await g()\n"
		"# All valid prefixes for unicode and byte strings should be colored.\n"
		"'x', '''x''', \"x\", \"\"\"x\"\"\"\n"
		"r'x', u'x', R'x', U'x', f'x', F'x'\n"
		"fr'x', Fr'x', fR'x', FR'x', rf'x', rF'x', Rf'x', RF'x'\n"
		"b'x',B'x', br'x',Br'x',bR'x',BR'x', rb'x', rB'x',Rb'x',RB'x'\n"
		"# Invalid combinations of legal characters should be half colored.\n"
		"ur'x', ru'x', uf'x', fu'x', UR'x', ufr'x', rfu'x', xf'x', fx'x'\n"
		)
	text = Text(top, background="white")
	text.pack(expand=1, fill="both")
	text.insert("insert", source)
	text.focus_set()

	color_config(text)
	p = Percolator(text)
	d = ColorDelegator()
	p.insertfilter(d)


class Percolator:

	def __init__(self, text):
		# XXX would be nice to inherit from Delegator
		self.text = text
		self.redir = WidgetRedirector(text)
		self.top = self.bottom = Delegator(text)
		self.bottom.insert = self.redir.register("insert", self.insert)
		self.bottom.delete = self.redir.register("delete", self.delete)
		self.filters = []

	def close(self):
		while self.top is not self.bottom:
			self.removefilter(self.top)
		self.top = None
		self.bottom.setdelegate(None)
		self.bottom = None
		self.redir.close()
		self.redir = None
		self.text = None

	def insert(self, index, chars, tags=None):
		# Could go away if inheriting from Delegator
		self.top.insert(index, chars, tags)

	def delete(self, index1, index2=None):
		# Could go away if inheriting from Delegator
		self.top.delete(index1, index2)

	def insertfilter(self, filter):
		# Perhaps rename to pushfilter()?
		assert isinstance(filter, Delegator)
		assert filter.delegate is None
		filter.setdelegate(self.top)
		self.top = filter

	def removefilter(self, filter):
		# XXX Perhaps should only support popfilter()?
		assert isinstance(filter, Delegator)
		assert filter.delegate is not None
		f = self.top
		if f is filter:
			self.top = filter.delegate
			filter.setdelegate(None)
		else:
			while f.delegate is not filter:
				assert f is not self.bottom
				f.resetcache()
				f = f.delegate
			f.setdelegate(filter.delegate)
			filter.setdelegate(None)


def _percolator(parent):  # htest #
	import tkinter as tk

	class Tracer(Delegator):
		def __init__(self, name):
			self.name = name
			Delegator.__init__(self, None)

		def insert(self, *args):
			print(self.name, ": insert", args)
			self.delegate.insert(*args)

		def delete(self, *args):
			print(self.name, ": delete", args)
			self.delegate.delete(*args)

	box = tk.Toplevel(parent)
	box.title("Test Percolator")
	x, y = map(int, parent.geometry().split('+')[1:])
	box.geometry("+%d+%d" % (x, y + 175))
	text = tk.Text(box)
	p = Percolator(text)
	pin = p.insertfilter
	pout = p.removefilter
	t1 = Tracer("t1")
	t2 = Tracer("t2")

	def toggle1():
		(pin if var1.get() else pout)(t1)
	def toggle2():
		(pin if var2.get() else pout)(t2)

	text.pack()
	var1 = tk.IntVar(parent)
	cb1 = tk.Checkbutton(box, text="Tracer1", command=toggle1, variable=var1)
	cb1.pack()
	var2 = tk.IntVar(parent)
	cb2 = tk.Checkbutton(box, text="Tracer2", command=toggle2, variable=var2)
	cb2.pack()

from tkinter import TclError

class WidgetRedirector:
	def __init__(self, widget):
		self._operations = {}
		self.widget = widget            # widget instance
		self.tk = tk = widget.tk        # widget's root
		w = widget._w                   # widget's (full) Tk pathname
		self.orig = w + "_orig"
		# Rename the Tcl command within Tcl:
		tk.call("rename", w, self.orig)
		# Create a new Tcl command whose name is the widget's pathname, and
		# whose action is to dispatch on the operation passed to the widget:
		tk.createcommand(w, self.dispatch)

	def __repr__(self):
		return "%s(%s<%s>)" % (self.__class__.__name__,
							   self.widget.__class__.__name__,
							   self.widget._w)

	def close(self):
		"Unregister operations and revert redirection created by .__init__."
		for operation in list(self._operations):
			self.unregister(operation)
		widget = self.widget
		tk = widget.tk
		w = widget._w
		# Restore the original widget Tcl command.
		tk.deletecommand(w)
		tk.call("rename", self.orig, w)
		del self.widget, self.tk  # Should not be needed
		# if instance is deleted after close, as in Percolator.

	def register(self, operation, function):
		'''Return OriginalCommand(operation) after registering function.
		Registration adds an operation: function pair to ._operations.
		It also adds a widget function attribute that masks the tkinter
		class instance method.  Method masking operates independently
		from command dispatch.
		If a second function is registered for the same operation, the
		first function is replaced in both places.
		'''
		self._operations[operation] = function
		setattr(self.widget, operation, function)
		return OriginalCommand(self, operation)

	def unregister(self, operation):
		'''Return the function for the operation, or None.
		Deleting the instance attribute unmasks the class attribute.
		'''
		if operation in self._operations:
			function = self._operations[operation]
			del self._operations[operation]
			try:
				delattr(self.widget, operation)
			except AttributeError:
				pass
			return function
		else:
			return None

	def dispatch(self, operation, *args):
		'''Callback from Tcl which runs when the widget is referenced.
		If an operation has been registered in self._operations, apply the
		associated function to the args passed into Tcl. Otherwise, pass the
		operation through to Tk via the original Tcl function.
		Note that if a registered function is called, the operation is not
		passed through to Tk.  Apply the function returned by self.register()
		to *args to accomplish that.  For an example, see colorizer.py.
		'''
		m = self._operations.get(operation)
		try:
			if m:
				return m(*args)
			else:
				return self.tk.call((self.orig, operation) + args)
		except TclError:
			return ""


class OriginalCommand:
	'''Callable for original tk command that has been redirected.
	Returned by .register; can be used in the function registered.
	redir = WidgetRedirector(text)
	def my_insert(*args):
		print("insert", args)
		original_insert(*args)
	original_insert = redir.register("insert", my_insert)
	'''

	def __init__(self, redir, operation):
		'''Create .tk_call and .orig_and_operation for .__call__ method.
		.redir and .operation store the input args for __repr__.
		.tk and .orig copy attributes of .redir (probably not needed).
		'''
		self.redir = redir
		self.operation = operation
		self.tk = redir.tk  # redundant with self.redir
		self.orig = redir.orig  # redundant with self.redir
		# These two could be deleted after checking recipient code.
		self.tk_call = redir.tk.call
		self.orig_and_operation = (redir.orig, operation)

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__,
							   self.redir, self.operation)

	def __call__(self, *args):
		return self.tk_call(self.orig_and_operation + args)


def _widget_redirector(parent):  # htest #
	from tkinter import Toplevel, Text

	top = Toplevel(parent)
	top.title("Test WidgetRedirector")
	x, y = map(int, parent.geometry().split('+')[1:])
	top.geometry("+%d+%d" % (x, y + 175))
	text = Text(top)
	text.pack()
	text.focus_set()
	redir = WidgetRedirector(text)
	def my_insert(*args):
		print("insert", args)
		original_insert(*args)
	original_insert = redir.register("insert", my_insert)

##syntax.python.end

import os
import subprocess
import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkfont
from WhirlData import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
#from pysyncolor import Percolator, ColorDelegator
#from percolator import Percolator
#from colorizer import ColorDelegator

filepath = ""

try:
	configs = open("runner.whirldata","r+")
except FileNotFoundError:
	configs = open("runner.whirldata", "x")

datafile = open("runner.whirldata").read()

if datafile.isspace():
	isConf = False
else:
	isConf = True

def runnerConf(thisType):
	print(thisType)
	cmds = read(datafile)
	command = cmds[thisType][1]
	command = command.replace("$file",'"'+filepath+'"')
	base = filepath.split("/")[-1]
	base = base[:base.find(".")]
	command = command.replace("$base",base.replace(" ","_"))
	command = command.replace("$dir",'"'+"/".join(filepath.split("/")[:-1])+'"')
	subprocess.call("start cmd /k {}".format(command), shell = True)

def getConfs():
	confs = []
	cmds = read(datafile)
	for i in cmds.keys():
		confs.append(i)
	return confs

colors = []
extension = {}

def curnote2(*args):
	variable = notebook.select()
	if notebook.select().replace(".!text","") == "":
		variable = 0
	else:
		variable = int(notebook.select().replace(".!text",""))
		if variable == 0:
			pass
		else:
			variable = int(variable) -1
	return variable

class AutocompleteEntry(ttk.Entry):
	"""
	Subclass of tkinter.Entry that features autocompletion.
	To enable autocompletion use set_completion_list(list) to define 
	a list of possible strings to hit.
	To cycle through hits use down and up arrow keys.
	"""

	def set_completion_list(self, completion_list):
		self._completion_list = completion_list
		self._hits = []
		self._hit_index = 0
		self.position = 0
		self.bind('<KeyRelease>', self.handle_keyrelease)               

	def autocomplete(self, delta=0):
		"""autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
		if delta: # need to delete selection otherwise we would fix the current position
			self.delete(self.position, tkinter.END)
		else: # set position to end so selection starts where textentry ended
			self.position = len(self.get())
		# collect hits
		_hits = []
		for element in self._completion_list:
			if element.startswith(self.get().lower()):
				_hits.append(element)
		# if we have a new hit list, keep this in mind
		if _hits != self._hits:
			self._hit_index = 0
			self._hits=_hits
		# only allow cycling if we are in a known hit list
		if _hits == self._hits and self._hits:
			self._hit_index = (self._hit_index + delta) % len(self._hits)
		# now finally perform the auto completion
		if self._hits:
			self.delete(0,tkinter.END)
			self.insert(0,self._hits[self._hit_index])
			self.select_range(self.position,tkinter.END)
						
	def handle_keyrelease(self, event):
		"""event handler for the keyrelease event on this widget"""
		if event.keysym == "BackSpace":
			self.delete(self.index(tkinter.INSERT), tkinter.END) 
			self.position = self.index(tkinter.END)
		if event.keysym == "Left":
			if self.position < self.index(tkinter.END): # delete the selection
				self.delete(self.position, tkinter.END)
			else:
				self.position = self.position-1 # delete one character
				self.delete(self.position, tkinter.END)
		if event.keysym == "Right":
			self.position = self.index(tkinter.END) # go to end (no selection)
		if event.keysym == "Down":
			self.autocomplete(1) # cycle to next hit
		if event.keysym == "Up":
			self.autocomplete(-1) # cycle to previous hit
		# perform normal autocomplete if event is a single key or an umlaut
		if len(event.keysym) == 1:# or event.keysym in tkinter_umlauts:
			self.autocomplete()

class CustomText(Text):
	def __init__(self, *args, **kwargs):
		"""A text widget that report on internal widget commands"""
		Text.__init__(self, *args, **kwargs)

		# create a proxy for the underlying widget
		self._orig = self._w + "_orig"
		self.tk.call("rename", self._w, self._orig)
		self.tk.createcommand(self._w, self._proxy)

	def _proxy(self, command, *args):
		cmd = (self._orig, command) + args
		result = self.tk.call(cmd)
		if command in ("insert", "delete", "replace"):
			self.event_generate("<<TextModified>>")
		return result

def newrunner():
	global conf
	def done():
		print(entry.get())
		thisconf = ""
		print(1)
		configs.writelines(datafile+'\n{}::["{}"::"{}"]'.format(name.get(),extension[curnote()],entry.get()))
		print(thisconf)
		conf.quit()
	def switchFunction():
		if gui.get():
			switch.config(text='Console')
		else:
			switch.config(text='No Console')
	conf = tk.Toplevel(root)
	conf.iconbitmap(r"favicon.ico")
	conf.resizable(False, False)
	conf.title("Configure runner for {} files".format(extension[curnote()]))
	conf.geometry("400x200")
	gui = BooleanVar()
	label = Label(conf,text = "Runner Name", font = "consolas")
	name = ttk.Entry(conf,width = 22, font = "consolas")
	name.place(x = 150, y = 10)
	label.place(x=10,y=16)
	#switch = ttk.Checkbutton(conf, text='Console', variable=gui, state = tk.DISABLED)
	#switch.invoke()
	#switch.config(command=switchFunction)
	label = Label(conf,text = "Command", font = "consolas")
	label.place(x=10,y=55)
	entry = AutocompleteEntry(conf,width = 22, font = "consolas")
	entry.set_completion_list((u'$file', u'$base', u'$dir', u'/k'))
	entry.place(x=150, y=50)
	entry.insert(0, 'compiler -o $base $file')
	submit = ttk.Button(conf,text = "Confirm", command = lambda:done())
	submit.place(x=150,y=150)
	conf.mainloop()

def runconf(*args):
	for i in datafile.split("\n"):
		if "[{}::".format(extension[curnote()]) in i:
			cmd = read(datafile)
			command = cmds[thisType][1]
			command.replace("$file",'"'+filepath+'"')
			base = filepath.split("/")[-1]
			base = base[:base.find(".")]
			command = command.replace("$base",base.replace(" ","_"))
			command = command.replace("$dir",'"'+"/".join(filepath.split("/")[:-1])+'"')
			subprocess.call("start cmd /k {}".format(command), shell = True)

root = tk.Tk()
root.iconbitmap(r"favicon.ico")
root.title('WhirlEdit 2bx')
windowWidth = 800
windowHeight = 530
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
xCordinate = int((screenWidth/2) - (windowWidth/2))
yCordinate = int((screenHeight/2) - (windowHeight/2))
root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))

style = ttk.Style(root)
try:
	root.tk.call('source', '.\\Themes\\azure-dark.tcl')
	style.theme_use('azure-dark') #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative','azure-dark')
except:
	pass

note = {}
openedfiles = {}
canvas = {}
scrolly = {}
scrollx = {}
var = 0

def opencmd(*args):
	try:
		cwd = "/".join(filepath.split("/")[:-1])
		drive = cwd[:2]
		subprocess.call('start cmd /k cd /d "{}"'.format(cwd), shell=True)
	except:
		subprocess.call('start cmd /k "{}"'.format(openedfiles[curnote2()]), shell=True)

def runfile(*args):
	try:
		cwd = "/".join(filepath.split("/")[:-1])
		drive = cwd[:3]
		subprocess.call('start cmd /k "{}"'.format(openedfiles[curnote2()]), shell=True)
	except:
		subprocess.call('start cmd /k "{}"'.format(openedfiles[curnote2()]), shell=True)

def getpos(*args):
	global pos
	global line
	pos = note[int(curnote())].index("end")
	pos = pos[:-2]
	pos = int(pos)
	pos = pos -1
	print(pos)
	line.set(pos)

'''def Highlight(event):
	note[curnote()].tag_remove("found", "1.0", "end")
	for i in colors:
		string = "{}".format(i)
		if string:
			idx = "1.0"
			while True:
				idx = note[curnote()].search(string, idx, nocase=1, stopindex=END)
				if not idx:
					break
				lastidx = f"{idx}+{len(string)}c"
				note[curnote()].tag_add("found", idx, lastidx)
				idx = lastidx
			note[curnote()].tag_config("found", foreground="#66d9ef") # #66D9EF #F92672 #AE81FF
		idx = "1.0"	
'''

def curnote():
	variable = notebook.select()
	if notebook.select().replace(".!text","") == "":
		variable = 0
	else:
		variable = notebook.select().replace(".!text","")
	return variable

def deltab(*args):
	try:
		notebook.forget(notebook.select())
	except:
		root.quit()

def saveAsFile(*args):
	global notebook
	global extension
	global filepath
	filepath = asksaveasfilename(defaultextension="",filetypes=[ ("All Files", "*.*"),("Text Files", "*.txt")])
	if not filepath:
		return
	with open(filepath, "w") as output_file:
		extension[curnote()] = "."+filepath.split(".")[-1]
		variable = int(curnote2())
		text = note[variable].get(1.0, tk.END)
		output_file.write(text)
	notebook.tab(note[variable], text = filepath.split("/")[-1])

def saveFile(*args):
	global notebook
	global extension
	print(curnote())
	print(openedfiles)
	if notebook.select().replace(".!text","") == "":
		variable = 0
	else:
		variable = notebook.select().replace(".!text","")
		if variable == 0:
			pass
		else:
			variable = int(variable) -1

	variable = int(curnote2())

	if openedfiles[variable] == "":
		saveAsFile()
	else:
		with open(openedfiles[variable], "w") as output_file:
			extension[curnote()] = "."+openedfiles[variable].split(".")[-1]


			text = note[variable].get(1.0, tk.END)
			output_file.write(text)
			notebook.tab(note[variable], text = openedfiles[curnote2()].split("/")[-1])

def openFile(*self): 
	#print("a",notebook.select())
	global extension
	global filepath
	if notebook.select() == "":
		newTab()

	variable = curnote2()
	filepath = askopenfilename(defaultextension=".py", filetypes=[("All Files","*.*"), ("Text Documents","*.txt"),("Python Files","*.py")]) 
	if filepath == "": 
		filepath = None
	else: 
		extension[curnote()] = "."+filepath.split(".")[-1]
		print(extension)
		note[variable].delete(1.0,END) 
		file = open(filepath,"r") 
		note[variable].insert(1.0,file.read()) 
		openedfiles[variable] = filepath
		file.close() 
		notebook.tab(note[variable], text = filepath.split("/")[-1])

def select_all(event):
    note[curnote2()].tag_add(SEL, "1.0", END)
    note[curnote2()].mark_set(INSERT, "1.0")
    note[curnote2()].see(INSERT)

def newTab(*args):
	global var
	global notebook
	note[var] = Text(font = "consolas", relief = FLAT, background = "#333333", wrap = None, width = 1000,undo=True)
	note[var].grid(sticky = N+E+S+W)
	note[var].focus_set()
	font = tkfont.Font(font=note[var]['font'])
	note[var].config(tabs=font.measure('    '))
	openedfiles[var] = ""
	notebook.add(note[var], text='Untitled')
	extension[curnote()] = ".*"
	scrolly[var] = ttk.Scrollbar(note[var],orient=VERTICAL,cursor = "hand2")
	scrolly[var].pack(side = RIGHT, fill=Y)
	scrolly[var].config(command = note[var].yview)
	note[var].config(yscrollcommand=scrolly[var].set)
	note[var].bind("Control-a",select_all)
	Percolator(note[var]).insertfilter(ColorDelegator())
	var = var + 1


Menubar = Menu(root, activebackground ="#0084FF", activeforeground = "#FFFFFF",bg = "#FFFFFF", fg = "#0084FF" ,font = "consolas")

Filemenu = Menu(root, tearoff = 0)
Filemenu.add_command(label="New",command=newTab)
Filemenu.add_separator()
Filemenu.add_command(label="Open", command=openFile)
Filemenu.add_command(label="Save", command=saveFile)
Filemenu.add_command(label="Save As", command=saveAsFile)
Filemenu.add_separator()
Filemenu.add_command(label="Close", command=deltab)
Filemenu.add_separator()
Filemenu.add_command(label="Exit", command=root.destroy)
Menubar.add_cascade(label="File", menu=Filemenu)

toolsMenu = Menu(root,tearoff=0)
confmenu = Menu(root,tearoff=0)
runmenu = Menu(root,tearoff = 0)
runmenu.add_command(label = "Open file from cmd", command = lambda:runfile())
runmenu.add_separator()
runner_command = StringVar()
if isConf:
	for i in getConfs():
		runmenu.add("command",label = i, command = lambda i=i: runnerConf(i))
	runmenu.add_separator()
runmenu.add_command(label= "New Runner",command = lambda:newrunner())
toolsMenu.add_cascade(label = "Runner", menu = runmenu)
toolsMenu.add_command(label = "Open cmd here", command = lambda:opencmd())
Menubar.add_cascade(label="Tools",menu = toolsMenu)

#Helpmenu = Menu(root, tearoff = 0)
#Helpmenu.add_command(label = "Website", command=lambda:webbrowser.open("http://www.github.com/Whirlpool-Programmer/WhirlEdit/"))
#Helpmenu.add_separator()
#Helpmenu.add_command(label = "Changelog", command=None)
#Helpmenu.add_command(label = "About",command = None)
#Menubar.add_cascade(label = "Help", menu=Helpmenu)

root.grid_rowconfigure(0, weight=1) 
root.grid_columnconfigure(0, weight=1) 

line = StringVar()

notebook = ttk.Notebook(root)
notebook.grid(sticky = N + E + S + W)
newTab()

extension[curnote()] = ".*"
notebook.bind("<Double-Button>", newTab)
root.bind("<Control-s>", saveFile)
root.bind("<Control-n>", newTab)
root.bind("<Control-w>", deltab)
root.bind("<Control-o>", openFile)
root.bind("<Control-F5>",runfile)
root.bind("<F5>",runconf)
root.bind("<Control-Shift-T>", opencmd)
#root.bind("<<TextModified>>", Highlight)
root.config(menu = Menubar)
root.mainloop()
configs.close()
