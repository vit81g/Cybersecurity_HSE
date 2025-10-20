#!/usr/bin/env python3
"""
baseline.py — Lightweight baseline for phishing URL classification hackathon.
"""
import pandas as pd, numpy as np, re
from urllib.parse import urlparse
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def normalize_series(s):
    s = s.fillna("").astype(str).str.strip().str.lower()
    s = s.str.replace(r"/{2,}", "/", regex=True)
    return s

def make_features_vec(series):
    s = normalize_series(series)
    def get_netloc(u):
        parsed = urlparse(u if re.match(r"^\w+://", u) else "http://" + u)
        return parsed.netloc or ""
    def get_path(u):
        parsed = urlparse(u if re.match(r"^\w+://", u) else "http://" + u)
        return parsed.path or ""
    netloc = s.apply(get_netloc)
    path = s.apply(get_path)
    feats = pd.DataFrame({
        "len": s.str.len(),
        "digits": s.str.count(r"\d"),
        "letters": s.str.count(r"[a-z]"),
        "dots": s.str.count(r"\."),
        "hyphens": s.str.count(r"-"),
        "underscores": s.str.count(r"_"),
        "slashes": s.str.count(r"/"),
        "at": s.str.count(r"@"),
        "question": s.str.count(r"\?"),
        "equal": s.str.count(r"="),
        "percent": s.str.count(r"%"),
        "colon": s.str.count(r":"),
        "has_https": s.str.startswith("https://").astype(int),
        "path_len": path.str.len(),
        "domain_len": netloc.str.len(),
        "tld_len": netloc.str.extract(r"\.([a-z0-9\-]+)$", expand=False).fillna("").str.len(),
        "has_ip": netloc.str.match(r"(?:\d{1,3}\.){3}\d{1,3}$").astype(int),
    })
    specials = feats[["dots","hyphens","underscores","slashes","at","question","equal","percent","colon"]].sum(axis=1)
    feats["ratio_digits"] = feats["digits"] / feats["len"].replace(0,1)
    feats["ratio_specials"] = specials / feats["len"].replace(0,1)
    feats["contains_kw"] = s.str.contains(r"login|secure|account|update|verify|bank|free|offer|win|prize", regex=True).astype(int)
    return feats

def main():
    train = pd.read_csv("train.csv")
    test = pd.read_csv("test.csv")
    sample = pd.read_csv("sample_submit.csv")
    X_train = make_features_vec(train["url"])
    y_train = train["result"].astype(int)
    X_test = make_features_vec(test["url"])
    scaler = StandardScaler(with_mean=False)
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    clf = LogisticRegression(max_iter=300, solver="liblinear")
    clf.fit(X_train_s, y_train)
    pred = clf.predict(X_test_s).astype(int)
    sub = sample.copy()
    n = min(len(sub), len(pred))
    sub = sub.iloc[:n].copy()
    sub["Predicted"] = pred[:n]
    sub.to_csv("submission_baseline.csv", index=False)
    print("Saved submission_baseline.csv")

if __name__ == "__main__":
    main()
