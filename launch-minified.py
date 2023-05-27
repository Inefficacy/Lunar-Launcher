p='jre'
o='custom'
n='ram'
m='natives'
l='Darwin'
k='Linux'
j='file'
i='download'
h='java'
b='OptiFine'
a='mode'
Z='artifacts'
Y='launchTypeData'
X=None
W=True
P=print
M='version'
L='name'
K='weave'
J='Windows'
H='launch'
G='directory'
F=open
D=False
import json,os as B,requests as E,platform as c,re,subprocess as Q
I=c.system()
A=json.load(F('config.json'))
def C(dir):return B.path.expanduser(dir.replace('/',B.sep))
def d(home):return B.path.join(home,'bin','javaw.exe'if I==J else h)
def e(wd):return sorted(filter(B.path.isdir,[B.path.join(wd,A)for A in B.listdir(wd)]),key=B.path.getmtime)[0]
def q(argument):
	A=argument
	for B in re.findall('%([^%]+)%',A):
		if B in V.keys():A=A.replace(f"%{B}%",V[B])
	return A
R=B.path.join(C(A[K][G]),'agent.jar')
def r():
	H=B.path.join(C(A[K][G]),'version.txt');M=E.get('https://api.github.com/repos/Weave-MC/Weave-Loader/releases/latest')
	if M.status_code!=200:P('Error sending request to GitHub API.');return
	I=M.json()
	if A[K]['ignore_duplicate']:
		if B.path.isfile(R)and B.path.isfile(H):
			if I[L]==F(H,'r').read():return D
	B.makedirs(C(A[K][G]),exist_ok=W);N=E.get(I['assets'][0]['browser_download_url'])
	if N.status_code!=200:P('Error downloading Weave asset.');return D
	with F(R,'wb')as J:J.write(N.content)
	with F(H,'w+')as J:J.write(I[L])
	return W
class f:
	def __init__(A,req):A.req=req
	def download(B):
		try:A=E.post('https://api.lunarclientprod.com/launcher/launch',json=B.req)
		except E.exceptions.RequestException as C:return D
		if A.status_code!=200 or A.json()==X:return D
		B.rjson=A.json();return A
	def fromFile(A,file):A.req=file.read()
	def downloadArtifact(A,name):
		for F in A.rjson[Y][Z]:
			if F[L]==name:
				try:
					for B in A.rjson[Y][Z]:
						if B[L]==name:C=E.get(B['url'])
				except E.exceptions.RequestException as G:return D
				if C.content==X:return D
				return C.content
if A[H][a]in[i,j]:
	import io,zipfile as s
	if A[H][a]==i:
		N=f({'hwid':'na','os':{k:'linux',J:'win32',l:'darwin'}.get(I),'arch':'x64'if c.machine().endswith('64')else'x32',M:A[M],'branch':'master','luanch_type':'OFFLINE','classifier':'optifine'});g=N.download()
		if g==D:P('Error with sending a launch request.');exit()
	else:N=f(X);N.fromFile(F(A[H][j]))
	t=[A[L]for A in g.json()[Y][Z]];S=C(A[H][G]);B.makedirs(S,exist_ok=W)
	for O in t:
		T=N.downloadArtifact(O)
		if T==D:P('Error downloading artifact.');exit()
		if m in O and O.endswith('.zip'):
			with s.ZipFile(io.BytesIO(T))as u:u.extractall(B.path.join(S,m))
		with F(B.path.join(S,O),'wb')as v:v.write(T)
U=[A for A in B.listdir(C(A[H][G]))if A.endswith('.jar')]
r()
V={K:R,n:str(A[n]*1024),'assetindex':'.'.join(A[M].split('.')[:-1]),M:A[M],'gamedir':C({k:'~/.minecraft',J:'~/AppData/Roaming/.minecraft',l:'~/Library/Application Support/minecraft'}.get(I)),'texturesdir':C('~/.lunarclient/textures'),'classpath':(';'if I==J else':').join([A for A in U if not A.startswith(b)]),'ichorclasspath':','.join([A for A in U if not A.startswith(b)]),'ichorexternal':[A for A in U if A.startswith(b)][0]}
V.update(A['custom_variables'])
Q.Popen([{'environment':'javaw'if I==J else h,o:d(A[p][o]),'lunar':d(e(e(C('~/.lunarclient/jre'))))}.get(A[p][a])]+[q(A)for A in A['arguments']],cwd=C(A[H][G]),stdout=Q.DEVNULL,stderr=Q.STDOUT)