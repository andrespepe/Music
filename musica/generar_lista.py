import urllib.request
import json

# ╔══════════════════════════════════════════════╗
# ║  CONFIGURA ESTAS DOS LÍNEAS                  ║
# ╚══════════════════════════════════════════════╝
API_KEY   = 'AIzaSyDIgTZ7sm-Yu_HOajcVn0B6DOLuE84xym4'       # ← tu clave de API de Google
FOLDER_ID = '17toZHl2Db38mIZJ48PXBzid-Z00BABey'             # ← ID de tu carpeta de Drive

# ── Obtener lista de archivos ──
songs = []
page_token = ''

print('Obteniendo lista de canciones...')

while True:
    url = (
        'https://www.googleapis.com/drive/v3/files'
        f'?q=%27{FOLDER_ID}%27+in+parents+and+mimeType+contains+%27audio%27'
        f'&fields=nextPageToken,files(id,name)'
        f'&pageSize=1000'
        f'&key={API_KEY}'
    )
    if page_token:
        url += f'&pageToken={page_token}'

    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())

    for f in data.get('files', []):
        songs.append({
            'name': f['name'].replace('.mp3', '').replace('.MP3', ''),
            'id':   f['id']
        })

    page_token = data.get('nextPageToken', '')
    if not page_token:
        break

# ── Ordenar alfabéticamente ──
songs.sort(key=lambda x: x['name'].lower())

# ── Guardar ──
with open('songs.json', 'w', encoding='utf-8') as f:
    json.dump(songs, f, ensure_ascii=False, indent=2)

print(f'✓ {len(songs)} canciones guardadas en songs.json')