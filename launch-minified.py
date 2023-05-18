l='jre'
k='custom'
j='ram'
i='natives'
h='Darwin'
g='Linux'
f='file'
e='download'
d='java'
c=print
W='OptiFine'
V='directory'
U='mode'
T='name'
S='artifacts'
R='launchTypeData'
Q=None
P=open
K='Windows'
F='version'
E='launch'
D=False
import json,os as B,requests as G,platform as X,re,subprocess as m
H=X.system()
A=json.load(P('config.json'))
def C(dir):return B.path.expanduser(dir.replace('/',B.sep))
def Y(home):return B.path.join(home,'bin','javaw.exe'if H==K else d)
def Z(wd):return sorted(filter(B.path.isdir,[B.path.join(wd,A)for A in B.listdir(wd)]),key=B.path.getmtime)[0]
def n(argument):
	A=argument
	for B in re.findall('%([^%]+)%',A):
		if B in O.keys():A=A.replace(f"%{B}%",O[B])
	return A
class a:
	def __init__(A,req):A.req=req
	def download(B):
		try:A=G.post('https://api.lunarclientprod.com/launcher/launch',json=B.req)
		except G.exceptions.RequestException as C:return D
		if A.status_code!=200 or A.json()==Q:return D
		B.rjson=A.json();return A
	def fromFile(A,file):A.req=file.read()
	def downloadArtifact(A,name):
		for E in A.rjson[R][S]:
			if E[T]==name:
				try:
					for B in A.rjson[R][S]:
						if B[T]==name:C=G.get(B['url'])
				except G.exceptions.RequestException as F:return D
				if C.content==Q:return D
				return C.content
if A[E][U]in[e,f]:
	import io,zipfile as o
	if A[E][U]==e:
		I=a({'hwid':'na','os':{g:'linux',K:'win32',h:'darwin'}.get(H),'arch':'x64'if X.machine().endswith('64')else'x32',F:A[F],'branch':'master','luanch_type':'OFFLINE','classifier':'optifine'});b=I.download()
		if b==D:c('Error with sending a launch request.');exit()
	else:I=a(Q);I.fromFile(P(A[E][f]))
	p=[A[T]for A in b.json()[R][S]];L=C(A[E][V]);B.makedirs(L,exist_ok=True)
	for J in p:
		M=I.downloadArtifact(J)
		if M==D:c('Error downloading artifact.');exit()
		if i in J and J.endswith('.zip'):
			with o.ZipFile(io.BytesIO(M))as q:q.extractall(B.path.join(L,i))
		with P(B.path.join(L,J),'wb')as r:r.write(M)
N=[A for A in B.listdir(C(A[E][V]))if A.endswith('.jar')]
O={j:str(A[j]*1024),'assetindex':'.'.join(A[F].split('.')[:-1]),F:A[F],'gamedir':C({g:'~/.minecraft',K:'~/AppData/Roaming/.minecraft',h:'~/Library/Application Support/minecraft'}.get(H)),'texturesdir':C('~/.lunarclient/textures'),'classpath':';'.join([A for A in N if not A.startswith(W)]),'ichorclasspath':','.join([A for A in N if not A.startswith(W)]),'ichorexternal':[A for A in N if A.startswith(W)][0]}
O.update(A['custom_variables'])
m.Popen([{'environment':'javaw'if H==K else d,k:Y(A[l][k]),'lunar':Y(Z(Z(C('~/.lunarclient/jre'))))}.get(A[l][U])]+[n(A)for A in A['arguments']],cwd=C(A[E][V]))