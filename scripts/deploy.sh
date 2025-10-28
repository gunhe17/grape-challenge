nc -z -w5 svc.sel3.cloudtype.app 30391 2>/dev/null || \
    ctype apply -f .cloudtype/db.prod.yaml

curl -sf --max-time 5 https://port-0-grape-challenge-mgx0qh415e7964a1.sel3.cloudtype.app/ >/dev/null || \
    ctype apply -f .cloudtype/app.prod.yaml