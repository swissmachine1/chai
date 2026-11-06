import json,pathlib
d=pathlib.Path(__file__).parent
files={'/':('text/html; charset=utf-8',(d/'app.html').read_text()),'/sw.js':('application/javascript',(d/'sw.js').read_text()),'/manifest.json':('application/manifest+json',(d/'manifest.json').read_text()),'/icon.svg':('image/svg+xml',(d/'icon.svg').read_text())}
w='''const FILES=%s;
// Un seul controle du code pour toutes les routes /api/. Blocage en 429, pas 401 : sur 401 l'app efface le code enregistre.
// ponytail: 30 codes faux par 24 h, mais KV peut etre en retard ~60 s, donc une rafale parallele passe encore ; code plus long ou Durable Object si ca compte
async function deny(req,env){const n=+(await env.KV.get('fails'))||0;
 if(n>=30)return new Response('{"error":"locked"}',{status:429});
 if(req.headers.get('X-Key')===env.PIN)return null;
 await env.KV.put('fails',String(n+1),{expirationTtl:86400});await new Promise(r=>setTimeout(r,1500));
 return new Response('{"error":"code"}',{status:401});}
export default{async scheduled(ev,env){const v=await env.KV.get('state');if(!v)return;const d=new Date().toISOString().slice(0,10);await env.KV.put('bak:'+d,v,{expirationTtl:31*86400});},
async fetch(req,env){const u=new URL(req.url);
 if(u.pathname.startsWith('/api/')){const no=await deny(req,env);if(no)return no;}
 if(u.pathname==='/api/state'){
  if(req.method==='GET'){const d=new Date().toISOString().slice(0,10);const n=+(await env.KV.get('use:'+d))||0;await env.KV.put('use:'+d,String(n+1),{expirationTtl:90*86400}); // ponytail: compteur d'ouvertures par jour, pas d'analytics
   const v=await env.KV.get('state');return new Response(v||'{"cuves":{},"ts":0}',{headers:{'Content-Type':'application/json'}});}
  if(req.method==='PUT'){const body=await req.text();if(body.length>2e6)return new Response('too big',{status:413});await env.KV.put('state',body);return new Response('{"ok":true}',{headers:{'Content-Type':'application/json'}});}
  return new Response('',{status:405});}
 if(u.pathname==='/api/usage'){if(req.headers.get('X-Key')!==env.PIN)return new Response('{"error":"code"}',{status:401});const l=await env.KV.list({prefix:'use:'});const out={};for(const k of l.keys)out[k.name.slice(4)]=+(await env.KV.get(k.name));return new Response(JSON.stringify(out),{headers:{'Content-Type':'application/json'}});}
 if(u.pathname.startsWith('/api/backups')){
  const k=u.pathname.slice('/api/backups/'.length);
  if(k){const v=await env.KV.get('bak:'+k.replace(/^bak:/,''));return new Response(v||'null',{headers:{'Content-Type':'application/json'}});}
  const l=await env.KV.list({prefix:'bak:'});return new Response(JSON.stringify(l.keys.map(x=>x.name).sort().reverse()),{headers:{'Content-Type':'application/json'}});}
 const f=FILES[u.pathname];if(!f)return new Response('introuvable',{status:404});
 return new Response(f[1],{headers:{'Content-Type':f[0],'Cache-Control':'no-cache'}});}}'''%json.dumps(files,ensure_ascii=False)
(d/'worker.js').write_text(w)
print('worker.js',len(w),'octets')
