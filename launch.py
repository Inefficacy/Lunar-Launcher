import json
import os
import requests
import platform
import re
import subprocess

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

agent_path = os.path.join(modify_path(config['weave']['directory']), 'agent.jar')

def download_weave():
	version_path = os.path.join(modify_path(config['weave']['directory']), 'version.txt')
	r = requests.get('https://api.github.com/repos/Weave-MC/Weave-Loader/releases/latest')
	if r.status_code != 200:
		print('Error sending request to GitHub API.')
		return
	j = r.json()
	if config['weave']['ignore_duplicate']:
		if os.path.isfile(agent_path) and os.path.isfile(version_path):
			if j['name'] == open(version_path, 'r').read():
				return False
	os.makedirs(modify_path(config['weave']['directory']), exist_ok=True)
	d = requests.get(j['assets'][0]['browser_download_url'])
	if d.status_code != 200:
		print('Error downloading Weave asset.')
		return False
	with open(agent_path, 'wb') as f:
		f.write(d.content)

	with open(version_path, 'w+') as f:
		f.write(j['name'])

	return True

###
# Modified from lcapi.py
# https://github.com/Inefficacy/Lunar-Archiver/blob/main/lcapi.py
###

class LcAPI:
	def __init__(self, req):
		self.req = req
	def download(self):
		try:
			r = requests.post('https://api.lunarclientprod.com/launcher/launch', json=self.req)
		except requests.exceptions.RequestException as e:
			return False
		if r.status_code != 200 or r.json() == None:
			return False
		self.rjson = r.json()
		return r
	def fromFile(self, file):
		self.req = file.read()
	def downloadArtifact(self, name):
		for artifact in self.rjson['launchTypeData']['artifacts']:
			if artifact['name'] == name:
				try:
					for a in self.rjson['launchTypeData']['artifacts']:
						if a['name'] == name:
							r = requests.get(a['url'])
				except requests.exceptions.RequestException as e:
					return False
				if r.content == None:
					return False
				return r.content

if config['launch']['mode'] in ['download', 'file']:
	import io
	import zipfile
	if config['launch']['mode'] == 'download':
		api = LcAPI({
			'hwid': 'na',
			'os': { 'Linux': 'linux', 'Windows': 'win32', 'Darwin': 'darwin' }.get(os_type),
			'arch': 'x64' if platform.machine().endswith('64') else 'x32',
			'version': config['version'],
			'branch': 'master',
			'luanch_type': 'OFFLINE',
			'classifier': 'optifine'
		})
		launch_request = api.download()
		if launch_request == False:
			print('Error with sending a launch request.')
			exit()
	else:
		api = LcAPI(None)
		api.fromFile(open(config['launch']['file']))

	artifacts = [a['name'] for a in launch_request.json()['launchTypeData']['artifacts']]

	savedir = modify_path(config['launch']['directory'])

	os.makedirs(savedir, exist_ok=True)

	for a in artifacts:
		d = api.downloadArtifact(a)
		if d == False:
			print('Error downloading artifact.')
			exit()
		if 'natives' in a and a.endswith('.zip'):
			with zipfile.ZipFile(io.BytesIO(d)) as zf:
				zf.extractall(os.path.join(savedir, 'natives'))
		with open(os.path.join(savedir, a), 'wb') as f:
			f.write(d)

jar_files = [f for f in os.listdir(modify_path(config['launch']['directory'])) if f.endswith('.jar')]

download_weave()

variables = {
	'weave': agent_path,
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