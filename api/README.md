# API Prediksi Biaya Asuransi Kesehatan (Flask)

Pengaplikasian model **Linear Regression** dari laporan praktikum Medical Insurance Cost
ke dalam REST API Flask yang bisa diuji dengan `curl`.
Model di API ini **persis sama** dengan yang didokumentasikan di laporan:
R² uji 0,8069 · MAE USD 4.177,05 · RMSE USD 5.956,34.

## Isi folder

- `app.py` — server Flask (endpoint `/`, `/health`, `/predict`)
- `train_model.py` — melatih ulang model dari `../data/insurance.csv` → `model.pkl` + `model_info.json`
- `model.pkl` — artefak model terlatih (siap pakai, tidak perlu latih ulang)
- `model_info.json` — metrik & skema fitur model
- `requirements-api.txt` — dependensi (Flask + pandas/numpy/scikit-learn)
- `test_api.sh` — skrip uji curl otomatis (6 skenario)
- `hasil_uji_curl.txt` — bukti hasil uji curl oleh Ochi (23 Okt 2026)

## Cara menjalankan (lokal)

```bash
cd api
pip install -r requirements-api.txt   # sekali saja
python app.py                          # server di http://127.0.0.1:5000
# ganti port bila perlu:  PORT=5001 python app.py
```

## Cara menjalankan di server hardy

Paket ini juga tersimpan di hardy: `/var/www/html/laporan-ml-regresi/api/`
(file web-nya bisa dilihat di http://100.115.94.1/laporan-ml-regresi/).
Untuk menjalankannya sebagai server API di hardy (belum dijalankan sebagai service — manual saja):

```bash
ssh hardy@100.115.94.1                       # masuk ke hardy (via Tailscale)
cd /var/www/html/laporan-ml-regresi/api
# Di hardy sudah ada .venv di folder laporan-ml-regresi (dipakai menjalankan notebook/train.py).
# Pakai itu saja, tinggal tambah Flask:
../.venv/bin/pip install flask
../.venv/bin/python app.py                   # server jalan di port 5000
# Alternatif bila ingin venv khusus API: python3 -m venv .venv && .venv/bin/pip install -r requirements-api.txt
```

Lalu dari komputer lain di tailnet yang sama, uji dengan curl:

```bash
curl http://100.115.94.1:5000/health
curl -X POST http://100.115.94.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 40, "sex": "male", "bmi": 30.5, "children": 2, "smoker": "no", "region": "southeast"}'
```

Berhenti: `Ctrl+C` di terminal tempat `app.py` berjalan.
Catatan: `train_model.py` membaca dataset dari `../data/insurance.csv` — di hardy file itu ada di
`/var/www/html/laporan-ml-regresi/data/insurance.csv`, jadi pelatihan ulang langsung bisa jalan.

Melatih ulang model (opsional, `model.pkl` sudah tersedia):

```bash
python train_model.py
```

## Endpoint

- `GET /` — info layanan + contoh body
- `GET /health` — status + metrik model
- `POST /predict` — prediksi biaya (`charges`, USD)

Body `POST /predict` (semua field wajib):

- `age` — angka 0–120
- `sex` — `female` | `male`
- `bmi` — angka 10–70
- `children` — angka 0–15
- `smoker` — `yes` | `no`
- `region` — `northeast` | `northwest` | `southeast` | `southwest`

Input tidak valid (field kurang, tipe salah, di luar rentang/pilihan) → HTTP 400 + pesan error JSON.

## Contoh curl

```bash
curl http://127.0.0.1:5000/health

curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 40, "sex": "male", "bmi": 30.5, "children": 2, "smoker": "no", "region": "southeast"}'
```

Respons contoh di atas: `prediction_usd: 8681.73` — sama persis dengan contoh prediksi di laporan.
Uji lengkap: `bash test_api.sh` (server harus sudah jalan).
