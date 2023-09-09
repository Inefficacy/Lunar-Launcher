import json
import os
import platform
import re
import subprocess
from lunarclient import API

os_type = platform.system()

config = json.load(open('config.json'))

def modify_path(dir):
	return os.path.expanduser(dir.replace('/', os.sep))

def java_location(home):
	return os.path.join(home, 'bin', 'javaw.exe' if os_type == 'Windows' else 'java')

def earliest_folder(wd):
	return sorted(filter(os.path.isdir, [os.path.join(wd, i) for i in os.listdir(wd)]), key=os.path.getmtime)[0]

def replace_variable(argument):
	for v in re.findall('%([^%]+)%', argument):
		if v in variables.keys():
			argument = argument.replace(f'%{v}%', variables[v])
	return argument

if config['launch']['mode'] in ['download', 'file']:
	import io
	import zipfile
	API.getUpdate()
	if config['launch']['mode'] == 'download':
		launch_response = API.getLaunch({
			'os': { 'Linux': 'linux', 'Windows': 'win32', 'Darwin': 'darwin' }.get(os_type),
			'os_release': platform.version(),
			'arch': platform.machine().lower() if platform.machine().lower() in ['arm', 'arm64', 'ia32', 'mips', 'mipsel', 'ppc', 'ppc64', 's390', 's390x', 'x64'] else 'x64',
			'version': config['version']
		})
	else:
		launch_response = json.load(open(config['launch']['file'], 'r'))

	artifacts = API.parseArtifacts(launch_response)

	savedir = modify_path(config['launch']['directory'])

	os.makedirs(savedir, exist_ok=True)

	for artifact in artifacts:
		if 'natives' in artifact.name and artifact.name.endswith('.zip'):
			with zipfile.ZipFile(io.BytesIO(artifact.download())) as zf:
				zf.extractall(os.path.join(savedir, 'natives'))
		else:
			with open(os.path.join(savedir, artifact.name), 'wb') as f:
				f.write(artifact.download())

jar_files = [f for f in os.listdir(modify_path(config['launch']['directory'])) if f.endswith('.jar')]

variables = {
	'ram': str(config['ram']*1024),
	'assetindex': '.'.join(config['version'].split('.')[:-1]),
	'version': config['version'],
	'gamedir': modify_path({
		'Linux': '~/.minecraft',
		'Windows': '~/AppData/Roaming/.minecraft',
		'Darwin': '~/Library/Application Support/minecraft'
	}.get(os_type)),
	'texturesdir': modify_path('~/.lunarclient/textures'),
	'classpath': (';' if os_type == 'Windows' else ':').join([f for f in jar_files if not f.startswith('OptiFine')]),
	'ichorclasspath': ','.join([f for f in jar_files if not f.startswith('OptiFine')]),
	'ichorexternal': [f for f in jar_files if f.startswith('OptiFine')][0]
}

variables.update(config['custom_variables'])

subprocess.Popen(
	[{
		'environment': 'javaw' if os_type == 'Windows' else 'java',
		'custom': java_location(config['jre']['custom']),
		'lunar': java_location(earliest_folder(earliest_folder(modify_path('~/.lunarclient/jre'))))
	}.get(config['jre']['mode'])]+[replace_variable(a) for a in config['arguments']],
	cwd=modify_path(config['launch']['directory']),
	stdout=subprocess.DEVNULL,
	stderr=subprocess.STDOUT
)