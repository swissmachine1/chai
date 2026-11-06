#!/bin/zsh
# Ouvertures de l'app par jour (lecture du compteur serveur)
cd "$(dirname "$0")"; source .env
curl -s -H "X-Key: $CHAI_PIN" https://carnet-chai.augustin-romaneschi.workers.dev/api/usage | python3 -c "import sys,json;d=json.load(sys.stdin);[print(k,v,'ouverture(s)') for k,v in sorted(d.items())] or print('aucune ouverture encore')"
