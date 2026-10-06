# Notes — Leforzz premium motion v01

- Direção escolhida: **Gallery Objects**. Motivo: preserva o caráter high-end e mantém um herói por frame.
- Renderer: HTML/CSS/JS determinístico + Playwright + FFmpeg, cloud-renderable em Linux.
- Assets de produto: baixados de URLs oficiais `leforzzfast.vtexassets.com` extraídas das páginas de produto. O pipeline registra SHA-256 em `.cloud-render/asset-capture.json`.
- Logo: nunca é redesenhado. O script abre a homepage oficial, identifica o elemento de marca no header/nav, isola o elemento e o rasteriza para PNG; o candidato escolhido e seu diagnóstico ficam registrados no manifest de captura.
- A captura em runtime é uma exceção deliberada ao princípio de assets congelados porque o conector atual não expõe os bytes dos assets web. O artifact preserva URLs, timestamp e hashes da captura usada no render.
- Copy usada: apenas naming/modelos e frases/descritores publicamente associados à marca. Sem preço ou condição comercial.
- Motion gates: M0/M2/M3 executados por `scripts/motion_quality.py`; M1/M4/M5/M6/M7 exigem revisão do filmstrip/contact sheet.
- Stillness final é intencional e deve ficar abaixo do limite de hold do M3.
