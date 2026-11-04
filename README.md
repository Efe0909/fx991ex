# fx-991EX mobile web app

A mobile-focused fx-991EX calculator emulator with a pixel display, a woven face inspired by the physical calculator, a decorative solar cell, and home-screen support. It runs as a static website and can be self-hosted or deployed to GitHub Pages. It does not require an App Store account.

## Credit and origin

This project adapts the calculator emulator from **[RedZebra123H/calculator](https://github.com/RedZebra123H/calculator)**. Thank you to RedZebra123H for making the browser version available. The upstream README says the emulators were taken from Casio's website. The calculator engine, firmware data, original face elements and trademarks originate from upstream or their respective owners; this project is not affiliated with Casio.

## Licence and third-party material

The new contributions to this project are offered under the GNU General Public License, version 3.0 only; see [LICENSE](LICENSE). **That grant covers only material the contributors have the rights to license.** The upstream repository does not specify a licence, and the rights for its Casio-derived engine, firmware, artwork, fonts and trademarks have not been established. The GPL notice here does not grant rights to that third-party material or imply the combined emulator has been cleared for redistribution. Obtain any required rights independently before redistribution or public hosting.

## Run locally

Run `python3 -m http.server 8000` in the project directory and open `http://localhost:8000/`. The calculator runs in the browser. HTTPS is needed for installation and offline features outside localhost.

## Host on GitHub Pages

1. Push this repository to GitHub.
2. Open **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, then select `main` and `/ (root)` and save.
3. Open the resulting `https://YOUR-USERNAME.github.io/fx991ex/` URL on your iPhone in Safari.
4. Tap **Share → Add to Home Screen → Add**.

GitHub Pages sites are publicly accessible, even if the source repository is private. Check the third-party rights above before publishing. You may configure a custom domain in GitHub Pages.

A service worker caches the app after an initial successful visit so it can work offline. Safari may remove cached data under storage pressure; reopen the app online if necessary. Actual iPhone offline operation has not been verified in this project.

## Editing the face

Edit `face.svg` to change the visual face, then run `python3 tools/update-face.py` to embed it into `index.html`. The screen, key hit areas and emulator are implemented in `index.html`; keep their coordinates aligned if the face dimensions change. The three PNG icons are pre-rendered and must be refreshed separately when desired.
