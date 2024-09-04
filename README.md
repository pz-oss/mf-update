[![Python application](https://github.com/PzyyBfiuMatrrP3WLxptx6ZbHZAGtXkx/mf-update/actions/workflows/python-app.yml/badge.svg)](https://github.com/PzyyBfiuMatrrP3WLxptx6ZbHZAGtXkx/mf-update/actions/workflows/python-app.yml)

## Excel

1. GCPでAPI有効化
   1. Google Drive
   2. Google Spread Sheet
2. サービスアカウント 編集者を作成


## Local

```sh
% (set -a;source .env; set +a; poetry run python -m mfupdate)
```

## GitHub actions

```sh
% gh secret set -f .env
% (set -a;source .env; set +a; sh -c 'base64 $MF_SA_FILE' | gh secret set MF_SA_FILE)  
```
