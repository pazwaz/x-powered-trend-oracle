import requests
r = requests.post(
    'https://x-powered-trend-oracle.vercel.app/oracle',
    headers={'x-payment': '0.49'},
    json={'topic': 'SOL memecoins last 6h test', 'signals': ['whale_moves', 'sentiment']}
)
print("Status:", r.status_code)
print(r.text)