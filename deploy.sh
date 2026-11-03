#!/bin/zsh
# Deploie le Worker "carnet-chai" + KV + secret PIN. Lit .env.
set -e; cd "$(dirname "$0")"; set -a; source .env; set +a
[ -n "$CLOUDFLARE_WORKERS_TOKEN" ] && [ -n "$CHAI_PIN" ] || { echo "Remplis CLOUDFLARE_WORKERS_TOKEN et CHAI_PIN dans .env"; exit 1; }
A="https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID"; H="Authorization: Bearer $CLOUDFLARE_WORKERS_TOKEN"
python3 build.py
KV=$(curl -s -H "$H" "$A/storage/kv/namespaces?per_page=100" | python3 -c "import sys,json;print(next((n['id'] for n in json.load(sys.stdin)['result'] if n['title']=='carnet-chai'),''))")
[ -n "$KV" ] || KV=$(curl -s -X POST -H "$H" -H 'Content-Type: application/json' "$A/storage/kv/namespaces" -d '{"title":"carnet-chai"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['result']['id'])")
echo "KV $KV"
META=$(python3 -c "import json;print(json.dumps({'main_module':'worker.js','compatibility_date':'2026-10-01','bindings':[{'type':'kv_namespace','name':'KV','namespace_id':'$KV'},{'type':'secret_text','name':'PIN','text':'$CHAI_PIN'}]}))")
curl -s -X PUT -H "$H" "$A/workers/scripts/carnet-chai" -F "metadata=$META;type=application/json" -F "worker.js=@worker.js;type=application/javascript+module" | python3 -c "import sys,json;r=json.load(sys.stdin);print('deploy',r['success'],r.get('errors'))"
curl -s -X PUT -H "$H" -H 'Content-Type: application/json' "$A/workers/scripts/carnet-chai/schedules" -d '[{"cron":"0 3 * * *"}]' | python3 -c "import sys,json;print('cron',json.load(sys.stdin)['success'])"
curl -s -X POST -H "$H" -H 'Content-Type: application/json' "$A/workers/scripts/carnet-chai/subdomain" -d '{"enabled":true,"previews_enabled":false}' >/dev/null
SUB=$(curl -s -H "$H" "$A/workers/subdomain" | python3 -c "import sys,json;print(json.load(sys.stdin)['result']['subdomain'])")
echo "URL: https://carnet-chai.$SUB.workers.dev"
