#!/usr/bin/env python3
"""
Upload the optimized app images to Cloudflare R2.
Run on a machine with a clean network (the Windows box's security software breaks
the TLS handshake to r2.cloudflarestorage.com — the Mac works fine).

Usage:
    pip install boto3
    export R2_AKID=...            # R2 Access Key ID
    export R2_SECRET=...          # R2 Secret Access Key
    export R2_ENDPOINT=https://<account>.r2.cloudflarestorage.com
    export R2_BUCKET=doarbai-assets        # optional, default doarbai-assets
    python upload-to-r2.py            # run from this folder (images/ next to it)

After uploading, enable the bucket's Public Development URL in the Cloudflare
dashboard (R2 -> doarbai-assets -> Settings -> Public Development URL), then set
AppConfig.assetBaseURL in the iOS app to that https://pub-xxxx.r2.dev URL.
"""
import os, sys, boto3
from botocore.config import Config

AKID = os.environ["R2_AKID"]
SECRET = os.environ["R2_SECRET"]
ENDPOINT = os.environ["R2_ENDPOINT"]
BUCKET = os.environ.get("R2_BUCKET", "doarbai-assets")
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

s3 = boto3.client("s3", endpoint_url=ENDPOINT, aws_access_key_id=AKID,
                  aws_secret_access_key=SECRET, region_name="auto",
                  config=Config(signature_version="s3v4"))
try:
    s3.create_bucket(Bucket=BUCKET); print("bucket created:", BUCKET)
except Exception as e:
    print("bucket:", str(e)[:80], "(continuing)")

CT = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
n = err = 0
for r, _, fs in os.walk(os.path.join(ROOT, "images")):
    for fn in fs:
        p = os.path.join(r, fn)
        key = os.path.relpath(p, ROOT).replace("\\", "/")
        ext = fn.lower().rsplit(".", 1)[-1]
        try:
            s3.upload_file(p, BUCKET, key, ExtraArgs={
                "ContentType": CT.get(ext, "application/octet-stream"),
                "CacheControl": "public, max-age=31536000, immutable"})
            n += 1
            if n % 40 == 0: print(f"  {n} uploaded...", flush=True)
        except Exception as e:
            err += 1
            if err <= 5: print("ERR", key, str(e)[:70])
print(f"DONE: uploaded {n} files, errors {err}")
