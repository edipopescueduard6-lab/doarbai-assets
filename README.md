# doarbăi — App Assets (optimized)

Mobile-ready showroom + coming-soon images for the doarbăi app, optimized
(max 1600px, ~62 MB total, 257 files). These are the `/images/...` paths referenced
by `boxes.json` and `coming-soon.json` — product photos are NOT here (they load from
doarbai.ro). All 109 app-referenced images are present.

**Private repo — used only to transport the optimized assets to the Mac for R2 upload.**

## Finish hosting (on the Mac — clean network)

1. Enable the bucket's public URL: Cloudflare dashboard → **R2 → `doarbai-assets` →
   Settings → Public Development URL → Enable**. Copy the `https://pub-xxxx.r2.dev` URL.

2. Upload the images to R2:
   ```bash
   pip install boto3
   export R2_AKID=<R2 Access Key ID>
   export R2_SECRET=<R2 Secret Access Key>
   export R2_ENDPOINT=https://2e9114da6b94b28e83cf4c2cf9ce021d.r2.cloudflarestorage.com
   python upload-to-r2.py
   ```

3. In the iOS app, set the asset base URL to the R2 public URL:
   `Sources/Core/Networking/AppConfig.swift` →
   `static let assetBaseURL = "https://pub-xxxx.r2.dev"`
   (product photos stay on doarbai.ro — AssetResolver only rewrites root-relative `/images/...`).

That's it — box/showroom/coming-soon images will then load in the app.

Showroom **videos** (~1.5 GB) are phase 2: same bucket, or use On-Demand Resources.
