# Prediksi Biaya Asuransi Kesehatan dengan Regresi Linear

Proyek ini membangun model regresi linear untuk memprediksi biaya asuransi kesehatan (`charges`) berdasarkan fitur seperti usia, jenis kelamin, BMI, jumlah anak, status merokok, dan wilayah.

Dataset yang digunakan adalah dataset populer dari Kaggle: `Medical Cost Personal Dataset` dengan file:

- [data/insurance.csv](data/insurance.csv)
- [notebook/medical_insurance_regression.ipynb](notebook/medical_insurance_regression.ipynb)

## Tujuan

- Menganalisis hubungan antar variabel terhadap biaya asuransi.
- Melakukan preprocessing data dan encoding fitur kategorikal.
- Melatih model regresi linear.
- Mengevaluasi performa model menggunakan MAE, RMSE, dan R2.
- Menyajikan visualisasi data dan hasil prediksi.

## Struktur Project

```text
medical_insurance_regression/
├── data/
│   └── insurance.csv
├── notebook/
│   └── medical_insurance_regression.ipynb
├── requirements.txt
├── index.html
└── README.md
```

## Dataset

File dataset: [data/insurance.csv](data/insurance.csv)

Kolom yang tersedia:

- `age`
- `sex`
- `bmi`
- `children`
- `smoker`
- `region`
- `charges`

Variabel target:

- `charges` : biaya asuransi kesehatan (USD)

## Teknologi

Proyek ini menggunakan Python 3.11 dan library berikut:

- pandas
- numpy
- matplotlib
- scikit-learn

Daftar dependency lengkap ada di [requirements.txt](requirements.txt).

## Persiapan Lingkungan

Disarankan menggunakan virtual environment agar library tidak bercampur dengan environment sistem.

```bash
cd /var/www/html/laporan-ml-regresi
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Menjalankan Proyek

### 1) Jalankan training model

```bash
cd /var/www/html/laporan-ml-regresi
source .venv/bin/activate
```

Script ini akan:

- membaca dataset dari [data/insurance.csv](data/insurance.csv)
- membersihkan data duplikat
- melakukan one-hot encoding pada fitur kategorikal
- membagi data train/test
- melatih model Linear Regression
- mengevaluasi model
- menghasilkan output di folder `output/`

### 2) Buka notebook analisis

Buka file:

- [notebook/medical_insurance_regression.ipynb](notebook/medical_insurance_regression.ipynb)

Notebook ini berisi langkah eksplorasi data, visualisasi, preprocessing, pelatihan model, dan evaluasi.


## Evaluasi Model

Metode evaluasi yang dipakai dalam proyek ini adalah:

- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R2 Score

Hasil yang umum dihasilkan pada split 80/20 adalah model dengan performa yang cukup baik untuk data ini, dengan `smoker` menjadi fitur paling dominan terhadap biaya asuransi.

## Catatan

- Jika Notebook gagal membaca file CSV, pastikan path yang dipakai benar, misalnya:

```python
pd.read_csv('../data/insurance.csv')
```

atau dari root project:

```python
pd.read_csv('data/insurance.csv')
```

- Untuk lingkungan Linux/macOS, aktifkan virtual environment dengan:

```bash
source .venv/bin/activate
```

