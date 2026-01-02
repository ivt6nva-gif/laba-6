import sys
import json
from pathlib import Path

# Ensure backend package is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'backend'))

from app import create_app

app = create_app()
app.config['TESTING'] = True

print('\nRegistered URL rules:')
for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
    print(f"{rule.endpoint:30} {rule.rule}")

print('\nRegistered blueprints and their url_prefixes:')
for name, bp in app.blueprints.items():
    # blueprint object may be None for 'static'
    prefix = getattr(bp, 'url_prefix', None)
    print(f"{name:20} prefix={prefix}")

with app.test_client() as client:
    print('\nRequesting /api/sensors/all/location/1')
    resp = client.get('/api/sensors/all/location/1')
    print('status:', resp.status_code)
    print('response body:', resp.get_data(as_text=True))
    print('\nRequesting /api/sensors/measurements?sensor_id=1')
    resp2 = client.get('/api/sensors/measurements?sensor_id=1')
    print('status2:', resp2.status_code)
    try:
        print(json.dumps(resp2.get_json(), ensure_ascii=False)[:1000])
    except Exception as e:
        print('failed to parse json:', e)
    # Now test with formatted time_from/time_to (backend expects 'YYYY-MM-DD HH:MM:SS')
    tf = '2025-12-10 06:00:00'
    tt = '2025-12-12 06:00:00'
    print(f"\nRequesting with time_from={tf} time_to={tt}")
    resp3 = client.get(f'/api/sensors/measurements?sensor_id=1&time_from={tf}&time_to={tt}')
    print('status3:', resp3.status_code)
    print('body3:', resp3.get_data(as_text=True)[:1000])
