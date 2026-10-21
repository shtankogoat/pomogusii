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
<div id="pg-preview-popup" style="display:none;position:fixed;inset:0;z-index:2000;background:rgba(8,5,3,.85);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);align-items:center;justify-content:center;padding:16px">
  <div class="pg-popup-box" style="position:relative;width:100%;max-width:560px;max-height:90vh;overflow:auto;background:linear-gradient(180deg,#2a190d,#140c07);border:1px solid rgba(233,182,92,.45);border-radius:22px;padding:56px 22px 22px;box-shadow:0 40px 120px -30px rgba(233,160,70,.45)">
    <button type="button" id="pg-preview-close" aria-label="Закрыть" style="position:absolute;top:12px;right:14px;width:38px;height:38px;border-radius:50%;border:1px solid rgba(233,182,92,.5);background:none;color:#f6d590;font-size:24px;line-height:1;cursor:pointer">&times;</button>
    <div id="pg-preview-widget" style="border-radius:14px;overflow:hidden"><script id="47ba71c13b415f85f08128b4062f6260dfce9c83" src="https://pomogusii.getcourse.ru/pl/lite/widget/script?id=1598811"></script></div>
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
