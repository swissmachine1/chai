import json,pathlib
d=pathlib.Path(__file__).parent
files={'/':('text/html; charset=utf-8',(d/'app.html').read_text()),'/sw.js':('application/javascript',(d/'sw.js').read_text()),'/manifest.json':('application/manifest+json',(d/'manifest.json').read_text()),'/icon.svg':('image/svg+xml',(d/'icon.svg').read_text())}
w='''const FILES=%s;
export default{async scheduled(ev,env){const v=await env.KV.get('state');if(!v)return;const d=new Date().toISOString().slice(0,10);await env.KV.put('bak:'+d,v,{expirationTtl:31*86400});},
async fetch(req,env){const u=new URL(req.url);
 if(u.pathname==='/api/state'){if(req.headers.get('X-Key')!==env.PIN){await new Promise(r=>setTimeout(r,1500));return new Response('{"error":"code"}',{status:401});} // ponytail: freine un essai de force brute, pas un vrai limiteur
  if(req.method==='GET'){const v=await env.KV.get('state');return new Response(v||'{"cuves":{},"ts":0}',{headers:{'Content-Type':'application/json'}});}
  if(req.method==='PUT'){const body=await req.text();if(body.length>2e6)return new Response('too big',{status:413});await env.KV.put('state',body);return new Response('{"ok":true}',{headers:{'Content-Type':'application/json'}});}
  return new Response('',{status:405});}
 if(u.pathname.startsWith('/api/backups')){if(req.headers.get('X-Key')!==env.PIN)return new Response('{"error":"code"}',{status:401});
  const k=u.pathname.slice('/api/backups/'.length);
  if(k){const v=await env.KV.get('bak:'+k.replace(/^bak:/,''));return new Response(v||'null',{headers:{'Content-Type':'application/json'}});}
  const l=await env.KV.list({prefix:'bak:'});return new Response(JSON.stringify(l.keys.map(x=>x.name).sort().reverse()),{headers:{'Content-Type':'application/json'}});}
 const f=FILES[u.pathname];if(!f)return new Response('introuvable',{status:404});
 return new Response(f[1],{headers:{'Content-Type':f[0],'Cache-Control':'no-cache'}});}}'''%json.dumps(files,ensure_ascii=False)
(d/'worker.js').write_text(w)
print('worker.js',len(w),'octets')
