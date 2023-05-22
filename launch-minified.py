m='jre'
l='custom'
k='ram'
j='natives'
i='Darwin'
h='Linux'
g='file'
f='download'
e='java'
d=print
X='OptiFine'
W='directory'
V='mode'
U='name'
T='artifacts'
S='launchTypeData'
R=None
Q=open
H='version'
G='Windows'
E='launch'
D=False
import json,os as B,requests as I,platform as Y,re,subprocess as L
F=Y.system()
A=json.load(Q('config.json'))
def C(dir):return B.path.expanduser(dir.replace('/',B.sep))
def Z(home):return B.path.join(home,'bin','javaw.exe'if F==G else e)
def a(wd):return sorted(filter(B.path.isdir,[B.path.join(wd,A)for A in B.listdir(wd)]),key=B.path.getmtime)[0]
def n(argument):
	A=argument
	for B in re.findall('%([^%]+)%',A):
		if B in P.keys():A=A.replace(f"%{B}%",P[B])
	return A
class b:
	def __init__(A,req):A.req=req
	def download(B):
		try:A=I.post('https://api.lunarclientprod.com/launcher/launch',json=B.req)
		except I.exceptions.RequestException as C:return D
		if A.status_code!=200 or A.json()==R:return D
		B.rjson=A.json();return A
	def fromFile(A,file):A.req=file.read()
	def downloadArtifact(A,name):
		for E in A.rjson[S][T]:
			if E[U]==name:
				try:
					for B in A.rjson[S][T]:
						if B[U]==name:C=I.get(B['url'])
				except I.exceptions.RequestException as F:return D
				if C.content==R:return D
				return C.content
if A[E][V]in[f,g]:
	import io,zipfile as o
	if A[E][V]==f:
		J=b({'hwid':'na','os':{h:'linux',G:'win32',i:'darwin'}.get(F),'arch':'x64'if Y.machine().endswith('64')else'x32',H:A[H],'branch':'master','luanch_type':'OFFLINE','classifier':'optifine'});c=J.download()
		if c==D:d('Error with sending a launch request.');exit()
	else:J=b(R);J.fromFile(Q(A[E][g]))
	p=[A[U]for A in c.json()[S][T]];M=C(A[E][W]);B.makedirs(M,exist_ok=True)
	for K in p:
		N=J.downloadArtifact(K)
		if N==D:d('Error downloading artifact.');exit()
		if j in K and K.endswith('.zip'):
			with o.ZipFile(io.BytesIO(N))as q:q.extractall(B.path.join(M,j))
		with Q(B.path.join(M,K),'wb')as r:r.write(N)
O=[A for A in B.listdir(C(A[E][W]))if A.endswith('.jar')]
P={k:str(A[k]*1024),'assetindex':'.'.join(A[H].split('.')[:-1]),H:A[H],'gamedir':C({h:'~/.minecraft',G:'~/AppData/Roaming/.minecraft',i:'~/Library/Application Support/minecraft'}.get(F)),'texturesdir':C('~/.lunarclient/textures'),'classpath':(';'if F==G else':').join([A for A in O if not A.startswith(X)]),'ichorclasspath':','.join([A for A in O if not A.startswith(X)]),'ichorexternal':[A for A in O if A.startswith(X)][0]}
P.update(A['custom_variables'])
L.Popen([{'environment':'javaw'if F==G else e,l:Z(A[m][l]),'lunar':Z(a(a(C('~/.lunarclient/jre'))))}.get(A[m][V])]+[n(A)for A in A['arguments']],cwd=C(A[E][W]),stdout=L.DEVNULL,stderr=L.STDOUT)