# Notes — Leforzz premium motion v01

- Direção escolhida: **Gallery Objects**. Motivo: preserva o caráter high-end e mantém um herói por frame.
- Renderer: HTML/CSS/JS determinístico + Playwright + FFmpeg, cloud-renderable em Linux.
- Assets de produto: baixados de URLs oficiais `leforzzfast.vtexassets.com` extraídas das páginas de produto. O pipeline registra SHA-256 em `.cloud-render/asset-capture.json`.
- Logo: o primeiro render descobriu no header oficial o SVG `b06c8cca...svg`. A partir daí o pipeline passou a baixar **esse asset oficial exato**, sem redesenhar ou reconstruir a marca.
- O review bundle inclui uma cópia dos assets capturados, URLs, timestamp e hashes para permitir congelamento/versionamento depois da validação.
- Revisão do primeiro render: removidos kicker/footer decorativos e o retângulo visual do packshot; packshots agora se integram à superfície por blend e escala maior. Adicionada variação lenta de luz para que a stillness seja intencional, não freeze acidental.
- Copy usada: apenas naming/modelos e frases/descritores publicamente associados à marca. Sem preço ou condição comercial.
- Motion gates: M0/M2/M3 executados por `scripts/motion_quality.py`; M1/M4/M5/M6/M7 exigem revisão do filmstrip/contact sheet.
