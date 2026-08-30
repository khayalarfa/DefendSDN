# DefendSDN

A machine-learning-based DDoS detection system with a Django web front end. Network flow statistics go in, a trained classifier says whether the flow looks like an attack or benign traffic.

## Overview

DefendSDN was built around the CICDDoS2019 dataset — flow-level features (protocol, packet timing, packet size, byte/packet rates, etc.) extracted from labeled DDoS attack traffic and benign traffic. Six classical ML/DL algorithms were trained and compared on this data; the best performer was wrapped in a small Django app so flow records can be submitted and classified through a browser instead of a script.

The dataset used here contains roughly 431k labeled flows across benign traffic and eleven DDoS attack categories (DrDoS_NTP, DrDoS_UDP, DrDoS_MSSQL, DrDoS_DNS, DrDoS_SNMP, DrDoS_LDAP, DrDoS_NetBIOS, TFTP, Syn, UDP, UDP-lag, LDAP, MSSQL, NetBIOS, Portmap, WebDDoS), collapsed into a binary `Attack` / `Benign` label for classification.

## Model comparison

Six models were trained on different sample sizes of the dataset (see the "Model training scripts" section for why the sample fraction varies) and evaluated on a held-out test split:

| Model | Accuracy | Notes |
|---|---|---|
| **XGBoost** | **91.2%** | Best overall — strongest balance of precision and recall on the attack class |
| Decision Tree | 86.4% | Cross-validated (5-fold, ~86.5% average) before the final fit |
| Random Forest | 85.4% | High precision on Attack (0.98) but recall trade-off on Benign |
| SVM (RBF kernel) | 78.9% | Very high recall on Attack, poor recall on Benign (0.08) — biased toward predicting attack |
| Naive Bayes | 55.3% | Weakest performer; included mainly as a baseline |
|

XGBoost was selected as the production model and is the one loaded by the Django app.

## Repository structure

```
Hello/                          Django project root
├── Hello/
│   ├── __init__.py
│   ├── settings.py             Project settings (SQLite DB, installed apps, static files)
│   ├── urls.py                 Root URL config — mounts admin and the `home` app
│   ├── asgi.py
│   └── wsgi.py
├── home/                       Django app — auth flow + detection UI
│   ├── __init__.py
│   ├── apps.py
│   ├── admin.py                Registers User_Data with the admin site
│   ├── models.py                User_Data model — stores submitted flow records
│   ├── urls.py                  Routes: landing, signup, login, contact (detection form), logout
│   ├── views.py                  Auth views + the prediction view
│   ├── tests.py
│   └── templates/
│       ├── index.html            Landing page (branded fork of the TemplateMo "Topic Listing" theme)
│       ├── signup.html
│       ├── login.html
│       ├── contact.html          The actual detection portal — the form users submit flow data through
│       ├── topics-listing.html   
│       └── topics-detail.html    
├── db.sqlite3                   SQLite DB — Django auth/admin tables plus `home_user_data`
├── detection_model.sav /
├── savedmodel.joblib             Trained XGBoost classifier, loaded by home/views.py
├── dataset.csv                    CICDDoS2019-derived training data
├── dt.py                          Decision Tree training script
├── knn.py                         KNN training script
├── nb.py                          Naive Bayes training script
├── rf.py                          Random Forest training script
├── svm.py                         SVM training script
├── xgb.py                         XGBoost training script (produces the model used in production)
├── running.py                     Standalone script for testing the saved model on a single sample
└── Resuts_ML.pdf                  Terminal output/screenshots of each model's evaluation run
```

## How it works

**Routes** (`home/urls.py`):

| Path | View | Purpose |
|---|---|---|
| `/` | `index` | Landing page |
| `/signup/` | `SignupPage` | Create an account (`django.contrib.auth`) |
| `/login/` | `LoginPage` | Log in |
| `/contact/` | `HomePage` | The detection form — requires login |
| `/logout/` | `LogoutPage` | Log out |
| `/admin/` | Django admin | Rebranded "DefendSDN Admin Portal" — review `User_Data` records and manage users |

**Prediction flow** (`HomePage` view, login-required):

1. The form on `contact.html` collects 9 of the model's 18 training features from the user: Protocol, Flow Duration, Fwd Packets Length Total, Flow Bytes/s, Flow Packets/s, Fwd IAT Total, Packet Length Mean, Avg Packet Size, Avg Fwd Segment Size, and Source IP (entered as an integer rather than a dotted address).
2. The remaining 9 features the model was trained on are filled in programmatically rather than collected from the user — several packet-length min/max/mean fields are just set equal to the one length value the user provided, `ACK Flag Count` is hardcoded to `0`, and `Subflow Fwd Bytes` reuses the Fwd Packets Length Total value. This keeps the form short at the cost of feeding the model an approximation rather than the true flow statistics for those fields.
3. The submitted record (the original 9 user-provided fields) is saved to `User_Data` via the ORM, so every prediction request leaves a row in `home_user_data` for later review.
4. The full 18-feature vector is passed to the loaded XGBoost model's `.predict()`, and the result (`0` = Attack, `1` = Benign, matching the label encoding used during training) is rendered back into `contact.html` next to the submitted Source IP.

**Auth**: signup/login/logout use Django's built-in `django.contrib.auth` — `SignupPage` creates a user directly with `User.objects.create_user`, `LoginPage` authenticates and logs in, and the detection form is gated behind `@login_required`.

**Landing page**: `index.html` is a customized fork of TemplateMo's free "Topic Listing" template, rebranded with the DefendSDN name. `topics-listing.html` and `topics-detail.html` came from the same template pack but aren't wired into any route — they're unused leftovers from the template download rather than active pages.

## Setup

```bash
pip install django scikit-learn xgboost joblib pandas
```

Run migrations and start the dev server from the project root (the directory containing `manage.py`):

```bash
python manage.py migrate
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/` for the detection page, or `http://127.0.0.1:8000/admin/` for the admin portal.

### Retraining the model

```bash
python xgb.py
```

This reads `dataset.csv`, trains a fresh XGBoost classifier, prints accuracy and a classification report, and dumps the trained model to disk. Update the `dump(...)` path at the bottom of `xgb.py` before running it — it currently points to a local Windows path from development and will need to match wherever you want the model saved.

### Testing the saved model directly

`running.py` loads the saved model and runs a single hardcoded flow record through it as a smoke test:

```bash
python running.py
```




