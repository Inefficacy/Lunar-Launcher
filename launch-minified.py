o='jre'
n='custom'
m='ram'
l='natives'
k='Darwin'
j='Linux'
i='file'
h='download'
g='java'
f=print
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
import json as Y,os as B,requests as I,platform as Z,re,subprocess as L
F=Z.system()
A=Y.load(Q('config.json'))
def C(dir):return B.path.expanduser(dir.replace('/',B.sep))
def a(home):return B.path.join(home,'bin','javaw.exe'if F==G else g)
def b(wd):return sorted(filter(B.path.isdir,[B.path.join(wd,A)for A in B.listdir(wd)]),key=B.path.getmtime)[0]
def p(argument):
	A=argument
	for B in re.findall('%([^%]+)%',A):
		if B in P.keys():A=A.replace(f"%{B}%",P[B])
	return A
class c:
	def __init__(A,req):A.req=req
	def download(B):
		try:A=I.post('https://api.lunarclientprod.com/launcher/launch',json=B.req)
		except I.exceptions.RequestException as C:return D
		if A.status_code!=200 or A.json()==R:return D
		B.rjson=A.json();return A
	def fromFile(A,f):A.rjson=Y.load(f);return A.rjson
	def downloadArtifact(A,name):
		for E in A.rjson[S][T]:
			if E[U]==name:
				try:
					for B in A.rjson[S][T]:
						if B[U]==name:C=I.get(B['url'])
				except I.exceptions.RequestException as F:return D
				if C.content==R:return D
				return C.content
if A[E][V]in[h,i]:
	import io,zipfile as q
	if A[E][V]==h:
		J=c({'hwid':'na','os':{j:'linux',G:'win32',k:'darwin'}.get(F),'arch':'x64'if Z.machine().endswith('64')else'x32',H:A[H],'branch':'master','luanch_type':'OFFLINE','classifier':'optifine'});d=J.download()
		if d==D:f('Error with sending a launch request.');exit()
		e=d.json()
	else:J=c(R);e=J.fromFile(Q(A[E][i]))
	r=[A[U]for A in e[S][T]];M=C(A[E][W]);B.makedirs(M,exist_ok=True)
	for K in r:
		N=J.downloadArtifact(K)
		if N==D:f('Error downloading artifact.');exit()
		if l in K and K.endswith('.zip'):
			with q.ZipFile(io.BytesIO(N))as s:s.extractall(B.path.join(M,l))
		with Q(B.path.join(M,K),'wb')as t:t.write(N)
O=[A for A in B.listdir(C(A[E][W]))if A.endswith('.jar')]
P={m:str(A[m]*1024),'assetindex':'.'.join(A[H].split('.')[:-1]),H:A[H],'gamedir':C({j:'~/.minecraft',G:'~/AppData/Roaming/.minecraft',k:'~/Library/Application Support/minecraft'}.get(F)),'texturesdir':C('~/.lunarclient/textures'),'classpath':(';'if F==G else':').join([A for A in O if not A.startswith(X)]),'ichorclasspath':','.join([A for A in O if not A.startswith(X)]),'ichorexternal':[A for A in O if A.startswith(X)][0]}
P.update(A['custom_variables'])
L.Popen([{'environment':'javaw'if F==G else g,n:a(A[o][n]),'lunar':a(b(b(C('~/.lunarclient/jre'))))}.get(A[o][V])]+[p(A)for A in A['arguments']],cwd=C(A[E][W]),stdout=L.DEVNULL,stderr=L.STDOUT)