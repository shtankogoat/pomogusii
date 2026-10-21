"""Собирает index.html (предпросмотр) из блоков в папке tilda/.

Запуск: python build.py
Редактируйте файлы в tilda/, затем пересоберите index.html.
"""
from pathlib import Path

ROOT = Path(__file__).parent
BLOCKS = sorted((ROOT / "tilda").glob("[0-9][0-9]-*.html"))

# Только для локального предпросмотра (виджет GetCourse запускается на DOMContentLoaded,
# поэтому его скрипт стоит в разметке сразу, а не подгружается по клику): на Tilda ссылки #popup:tarif1
# открывает штатный блок-попап (T868) с виджетом оплаты GetCourse.
PREVIEW_POPUP = """
<div id="pg-preview-popup" style="display:none;position:fixed;inset:0;z-index:2000;background:rgba(0,0,0,.75);align-items:center;justify-content:center;padding:16px">
  <div style="position:relative;width:100%;max-width:560px;max-height:90vh;overflow:auto;background:#fff;border-radius:16px;padding:24px">
    <button type="button" id="pg-preview-close" aria-label="Закрыть" style="position:absolute;top:8px;right:12px;border:0;background:none;font-size:28px;cursor:pointer">&times;</button>
    <div id="pg-preview-widget"><script id="47ba71c13b415f85f08128b4062f6260dfce9c83" src="https://pomogusii.getcourse.ru/pl/lite/widget/script?id=1598811"></script></div>
  </div>
</div>
<script>
(function () {
  if (window.t_onReady) return; // на Tilda работает её собственный попап
  var popup = document.getElementById('pg-preview-popup');
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href$="#popup:tarif1"]');
    if (!a) return;
    e.preventDefault();
    popup.style.display = 'flex';
  });
  popup.addEventListener('click', function (e) {
    if (e.target === popup || e.target.id === 'pg-preview-close') popup.style.display = 'none';
  });
})();
</script>
"""

HEAD = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ПомогусИИ — клуб по нейросетям Льва Кудрина</title>
<meta name="description" content="Стань Нейрокреатором — это проще, чем кажется! Закрытый клуб по нейросетям: 40+ практических уроков, ИИ-мультфильмы, фото, видео, озвучка и монетизация.">
<style>body{margin:0;background:#0b0705}</style>
</head>
<body>
"""


def main():
    parts = [HEAD]
    for block in BLOCKS:
        parts.append(f"\n<!-- ===== {block.name} ===== -->\n")
        parts.append(block.read_text(encoding="utf-8"))
    parts.append(PREVIEW_POPUP)
    parts.append("</body>\n</html>\n")
    (ROOT / "index.html").write_text("".join(parts), encoding="utf-8")
    print(f"index.html built from {len(BLOCKS)} blocks")


if __name__ == "__main__":
    main()
