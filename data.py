import os
import yaml
import cairosvg
import tempfile

temp_dir = tempfile.gettempdir()

if not os.path.isdir(temp_dir+'/WhirlEdit/'):
    #if "OSError: [Errno 30] Read-only file system:" happens, we will create another temp folder
    try:
        os.mkdir(temp_dir+'\\Whirledit\\')
    except OSError:
        temp_dir = Path(Path(__file__).parent.resolve(), 'temp')
        os.mkdir(temp_dir+'\\Whirledit\\')

configuration = """
Key Bindings:
  Close: <Control-w>
  Fullscreen: <F11>
  New: <Control-n>
  Open: <Control-o>
  Open cmd: <Control-Shift-t>
  Run: <F5>
  Save: <Control-s>
Logs:
  Logging: false
Looks:
  Font:
    BlockCursor: true
    Font: Consolas
    Size: '12'
  Icons:
    Theme: fluent.dark
  InitialSyntax: Python
  Scheme:
    Default: azure-modified
    Folder: ./DATA/Schemes/
  Theme:
    Default: forest-dark.whTheme
    Folder: ./DATA/Themes/
  WindowTitle: WhirlEdit
"""
try:
    configuration = (yaml.safe_load(open('./DATA/configure.yaml').read()))
except Exception:
    configuration = (yaml.safe_load(configuration))
font = "{} {}".format(configuration['Looks']['Font']['Font'],configuration['Looks']['Font']['Size'])
isBlockcursor = configuration['Looks']['Font']['BlockCursor']
config = configuration

class icons:
  logo = b'x\xda-V\xc7\x1a\xa20\x10~ \x0f\x02\x02\xcaa\x0f\t\xbd7A\xe0&-A\xaa\x14\x01\x9f~q\xbf\r\x04\xc8\xf4\xf9g\x92\x8f*\x84\xb6\xb7\x12\xba\x8czp\x0c\xcb\x0f\xb0\x18\xa0\xe3Kv\x8f\x07\xacy`\xfe\xde\x8a#\x87\xedO\x00\xca9\xbc\x07"\x00\x86\xec\xf0\xe7\r\xc3\x9f\x18\x90\xbeA\x9d\xf3@\xbf\xda\x8a]\x1fk\xa3\x0f\xc4-\xf0\x82m\xc8\x8aW\xcf*!\x99\xe7\xf7\x80t.\xdc9\xe5\xd7I}\xca\xb8\xb6\x04\x97\xc0\xaa\xaf\xebU?]\xaco\x98G\xe1\xf9\xff\xa0\xc2&\x89\xb8sy\xb5\xbf\x13\xb3\xa4\xed\xcd\xe0\xd76i\x93\xc5y\xd1\x17L\x17\xf26\xa5"c\xdf?\x87\xec\xa9\x1b\xd8G3<#m\xcf:\x8f\xc8\x15\xe6T\xbe\xedW\x7f-.3\x05Ql\x1f:\xcc#l\x8e;y\xb6\xc3;\xa6\xacW\xd6i{\xc2\xbb\xb5\x18J\xde\xc3z\xc5\x9cs\'~~/\t\x95\xb7\xdc\'%\xad{\xc0\x1c|\xeb\x9b]~\xf6jO\xf4\xa4\x83\xc6\xca\xb8\x8fm\x01Q\x87\x7f\xe3I\xcd\xeda\xb3\xfc\xde\xcez\xd1\r?}\x12\xba\x81\x1d5Lz\xf8\xfe\xad\xe9\x93\xf3"\x1a\xcdOt\xbf\xfe\xc5J\xe2\xf8\xc1\xf7o\x1dA\xbbC\xb0\xda\x00\x94*\xc4\x8b\xe7\x15.\x97\xea\xa0\xfb\xa8\xd7e\xafN\xc0\xc1_\x0f\xde\xcaK\x07\xcf\xee\xbc\x9ay\xfc\xe4\xddF\xc1\xe8\xa0\xfb\xf1l\xae\xf59_\xe1k\xab\xe2\xc5\xf2j2\xa8\xfaA[\xe1\x87\x86\x9eR\xec\xf5\xa0\xbb\xa4\xd7\xf8\xfd\xa0\x03\x99?\xf9h2\xbdY\xcf\xdd\x9c\xa4\xf6\x80\xf4x4\x9b?\x7f+\xf9|\x83\xc3\xf7\n\xcd\x16A\xf9\x05=\xbbr\xa1\xd3\x03\x98-.\x0fN.\xdc\xe8\n\x8d\x06"\xb8\xd4\x85=\x81x\xe1\xec\xbb\x8b\r\x12\xf5\x90}\xb68\xb8\xc6\x9e\xa4c\xbe\x1f\r\x88\x1dTeG,\xa1\x98a\xc9o\xdc!\x9f\xaa\xecc\xad\xc3\xb2\xef\xebd\xf0\xd3\xa8\xefh\xb1xz1^\x88\xb6\x85\xe0@\x19\xac&\x7f\xc4\xc6\xd7\xa3\xf1\x9b\x1e\xb6\xd1aK\xdf$\xbf\xde\x8ex\xf1\x91\x97K&\xc3/\xd7*\x9e\xcc_\xec>1\x1b\xf7\xech\x18\x97\xb0\x04q3\xef?\x90\xa7\xa3S\xcc\xaf\xf9\xd3Y5\xb3u\xe1|\x01G\x96.l\xbf\x00+\x15\x9c\xbew@\xdf\x9ex\xa5\x02\xe8\x19\xf8\x87I\x056\xd7\x8b\xd9h\xb3\xd4\xb2:\xf0X\xc3\xe7\xb8\x1fXb\xc4<\xb0\xa5\x95\x07\xfe/x\xe4\xf6\xcb\xdb\x0bn\xf1\xe6\xa9%8\xf2\xe7E\xca_\x8f\xdc\xdc-}o\xb9\x90\xe2\x98\x8d\xbd\x1b\x1d\xf0\xd9j\x03^>\xaf\xdb\xb0\xfa\xf5d\xe0\\+\xdd9\x1bq"d.D+\x90&\xcaC\xa7\xc4\x85\xe9\xbc\x99L\xb4\x016\xf1\x0f\xbc\x10t\xba_\xdd|p\x8e`#f\xc0\xbb\xb2\x08\x86o\xbc\xa9\x99?\xbdu>\x9b-\x10j\xaf*\x9e\x8f\xcdy`\x7f\xc4\xb3e\x97\xc7\xaf>\xe8\xa8\xcf\x8ae\x8c\xa5cs&\xe8\x03\xa0\xd1B\xcby\xfd\xea\xebZWvm`\x81\x8f\x9a\x022\x1f\x8f\x9e\xb1\x80\xf5\x9c\\\xc8qh\xf3[?X\xed\x15\xab\xff\xea\xed\x07\x84[\xb9\x17\xdf\x1d\xe6\x1d\xcd\xfd\n\xe0J#LPn\xb3\x13{=\x9b\xbcz\r6-\xef\xb7$\xac\xf9xw\x80,\x9cac#\xc7\x0b\xbf\x1b\xfd;\x15\xa4\\\xd2\xec`\x05\xf1\xcaOvd87\x8e\x16\x97+R\x15:\x9d\x1f(\x88njz^n\xc8\xcd\xb9\xacT\xf7\xce\x8ai|J\xcf\x1d\xbf\xd8I\xc4P\xfbM\xa6\xec\x8ek\xaa\xear*8z\xb3\xb4;\x87=\n\x94 \x0b\xd7\xf7x\xeeW\x81\xe9?\x07\xcc\xbf\xb3\xc5\xc4~\xe0\xc1P~\x15\xd7|\x08C\xe8y\xb2)l<\x8d\r?\xca\xc6KN\xcd\xd1\x11\xa8\xfb\x92\xdcC\xf9.\xa5\xf2\x96QuP\xf3\xecu\xf9\x7fQd&Q\t%e[\xde\xb6i}c\x9d\xad\xcco\xe7\xdbw\xfa\xf2]\\~\x00\xc1\x07u\x10\xa4\xe6\x85\xcau\xe9\xb9\x9b\xdd\x93\x9a\xa2\x84\x00\x9f\xf0\x9d>\x98\xaa\xd6D\xdb\xbf\xd3W\xf7!\x87\x9f\xd8\xce\xc7\xa7X\x13\xc1xo\xf8\xb2\xae\x19\xc1:\t\x82\x10\xd4\x8bm6}\xfff\x9f_\x9d\xf3D\xb7a\x0c\x98*^\x88\xba\xaa\xf2\xf70d\x1b.\x9c\x06]3\xfd\xa6\x91\xbb\x9e\xac\xf8\xe7\x1b\xc32Q\xc3\xf4\xe1De\xf3\xa8\xd9Mo\xe8SI\xc2\xafR\xd7w\xe4\xb5\x85\xeb\x02u3q\x88\x9c\x1d\x116\xc4\xaeX\x1a\x84\xd6\xe2\xde\xa4\xe4\xa8*\xa5\xde\x1f\x8c\tLJjB?,\xd0\xeb\xbc\x03\xa46\xc1+\\\xeb\x9c~\xf7\x91\xaa\x81\xf2)\xfa\xac\xce\x17\xe1b\x14V2u\x157\xc63+ScV\xa5\xaa?~J8\xe8\xba+y\x95u\xca)C\\\xba\xea\xbd\xac^\xfc\xb9\xeb\x80\xcd\x11f(\n\xd7\xf9Z>\xd3\xa2\x9e\x88\xbc\x13vi\x86*\xe7\x0c\xea\xc9\xac\xeb\xd8O\x06f\x12\xda,\xc6\x8ac\x94\xaaX<\xabe\x0f\xc0\xbd9\x85\xb6F\xb0\x18D\x17\x02\\\xd8\x8a\xbf\x92\xb3\xa6,\r}3\x13\xe3}\xca\xe6\x131\xce\x11\xdc\xebXE\x8e\xcf\x04\xfb\xbe\x08\xc5\'\xa2\x02\xa7\x96\x0cj]KA\xd3dlV\xb2\x17ZJ\xdea\xc5\x8f\x1a$*\xa6\xf8 \xfa\xc5=7\xd7Z\x04W\\+7Ou\xef}7\xf2\xaa(\x9d\x0b\tqr\xa8|/\\[\xbd_kh\x8a\xb6\xa1\xcc\xc4I\xa8\x05\x8a\xb5\xe2\xf1\xbd\x85f[\xd9B\xf4%\xd1\x90\'j\xcf\xd5\xe6\xb3\xbee\xe4\x94]\xa5\x01F\xd7\xb2\x89\xbf\xaaa2X4\xe9A\x91j\x85\xb1\xbf\xecw\x9a\x13\xe7\x06\xb5\xa9\xd0i\xfb\xd3\x9d\x1b\xed\xb9D\xd4m\x01\x1fF\x144\xa6\xbb\xee\xd7F\xb8\xb9T\xb93\x01\x11YNT\xb8\xb2o\xf4\xeen\xc2D\x8d\xd7*0\xe9\x7f\xf6 \xb33w\rNl\xfc\n\xa9\xb3\xcd\x12\xd4X<\xe7=\x11\x01\xe5\xf3\xba\xb7R?\xd2\xd7\x0bp{\x9c\x80\x12Y\xeb\xbemY\x0b\x91\x02\x86K$\xf5^\'\xd5\x16\x7f+\xd1=\xe6\xfd\xe19\xd9.\x18\xd2\xee)\x01G:\xd5[I\xfd\xf2\x8e\xbe\xa0\'\x9b\xecR,\xad\xcf/\xc2\xe2\xf0\x97\x8f\xff>\xc3\x80\xef\xb4\x9a\xefw\x8f\xa1R\xfb\x84=\x8fdo!\xf7\x84\x89Xj4\xd6: \xdf/\xa26\xf4AQ\xad)x\xec\xef\xc9\xe4N\xe7X&\x9d"\xf1\xec\xec\xbb\x83\x98\xb6\x17\xf9,\x9a\x1b\xa0\xa9\x87X\xecz\xc9.\xc8BO\xba\xb9\x14\xb4\xd2)\xae\x0fz/\xb5\xef\xee\xbeG\xfc\xa9.ZN\x1a\xdb`p\xeaG?~\xc8\x0b\x0cr\xf8A\xfb\xddEc\xaa\xb3ch`{xJ\x1e\n\xcaW\xc3\xf6\xe3\xbc\xc9\xb3\xb7\xb4L\xf1\x88vJ\xb9\xeb\xe1\xc0\x16\xb36*H*\xd2NL\xf6d\xaf4\xa1n\xda\xe23\xd3\x98\x0b\xd3\x10\xd4\x86\x10\x85\xeb\xe8\x93/\xf6r\xab\xcc\x9b\x93i98\xbd?e\xf2Y$s\xf5\xf34\x1a\xa9\xec\xf7\xa3\x02\xfc \xb4=\x9d\xe1cU\xfd\xf3\x17\xe8\xaa\xff\xa1'
  logo_mini = "./DATA/icons/logo-mini.png"
  sidebar_files = "./DATA/icons/{}/sidebar.files.png".format(config['Looks']['Icons']['Theme'])
  sidebar_runner = "./DATA/icons/{}/sidebar.runner.png".format(config['Looks']['Icons']['Theme'])
  sidebar_looks = "./DATA/icons/{}/sidebar.looks.png".format(config['Looks']['Icons']['Theme'])
  sidebar_settings = "./DATA/icons/{}/sidebar.settings.png".format(config['Looks']['Icons']['Theme'])
  project_newfile = './DATA/icons/{}/project.newfile.png'.format(config['Looks']['Icons']['Theme']), 
  project_newfolder = './DATA/icons/{}/project.newfolder.png'.format(config['Looks']['Icons']['Theme'])
  project_closefile = './DATA/icons/{}/project.closefile.png'.format(config['Looks']['Icons']['Theme'])
  main_newtab = './DATA/icons/{}/main.newtab.png'.format(config['Looks']['Icons']['Theme'])
  terminal_clear = './DATA/icons/{}/terminal.clear.png'.format(config['Looks']['Icons']['Theme'])
  terminal_reset = './DATA/icons/{}/terminal.restart.png'.format(config['Looks']['Icons']['Theme'])  