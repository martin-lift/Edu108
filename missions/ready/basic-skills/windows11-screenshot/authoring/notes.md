# Екранна снимка (Screenshot) в Windows 11 — заснемане и записване

Категория: **Базови умения**. Мисията няма клас, предмет или обвързване с
конкретен урок: полетата `class_name`, `subject` и `lesson` са пропуснати.

Изрично зададената структура има предимство пред принципите за стандартен
урок: 8 информационни стъпки, без въпроси, тестове или AI проверка;
деветата и последна стъпка е предаване на файл. Няма обобщение след нея.

Основен път: Calculator като пример → Windows + Shift + S → правоъгълна
област → Paint / Ctrl + V → Ctrl + S → създаване на папка в Documents в
прозореца за записване → PNG → отваряне → качване. Папка не се създава
предварително. Ако вече съществува, се използва същата папка.

След записването е обяснена комбинацията Windows + Print Screen за целия
екран → Pictures / Screenshots. След двете комбинации има отделна стъпка
за самостоятелния Prt Scr и зависимостта му от настройката в Windows 11:
избор на област чрез Snipping Tool или копиране на целия екран в клипборда.
Обяснени са Fn, възможното пренасочване на Pictures към OneDrive и изборът
на цял екран през Snipping Tool. Не се разчита на автоматичното записване
на Snipping Tool, което зависи от версия и настройки.

Дават се български и английски имена на основните елементи. Обяснени са
клипбордът, PNG и намирането на папката. Опитите се записват с различни имена.
Приемливият краен резултат е собствена снимка на част или на целия екран,
PNG или JPG/JPEG до 20 MB. Това е условие в текста: форматът на мисията не
поддържа филтър за разширения; Student108 осигурява общото ограничение 20 MB.

## Първични източници

Проверени на 23.11.2026 г.:

- [Настройката на Prt Scr, Microsoft Support](https://support.microsoft.com/en-gb/accessibility/windows/make-your-mouse-keyboard-and-other-input-devices-easier-to-use)
- [Snipping Tool, Microsoft Support](https://support.microsoft.com/en-us/windows/apps/use-snipping-tool-to-capture-screenshots)
- [Заснемане в Windows 11, Microsoft](https://www.microsoft.com/en-us/windows/learning-center/how-to-screenshot-windows-11)
- [Копиране на екран и поставяне в Paint, Microsoft Support](https://support.microsoft.com/en-us/office/copy-the-window-or-screen-contents)
- [Автоматично записване според настройките, Microsoft](https://www.microsoft.com/en-us/windows/learning-center/how-to-use-snipping-tool-on-windows-screenshots-shortcuts-and-screen-recordings)
- [Разширения на файловете, Microsoft Support](https://support.microsoft.com/en-au/windows/experience/storage-filemanagement/common-file-name-extensions-in-windows)

Единственото външно изображение е официалният екран на Snipping Tool от първия
източник: `https://support.microsoft.com/en-us/windows/media/snipping-tool-opened-png.png`.
Авторството Microsoft е посочено. Останалите нагледни средства са HTML/CSS:
клавишни комбинации, схема на избрана област, последователност и папки.
Схемите са обозначени като примерни и не имитират действителен Windows екран.

## Генериране и проверка

- `python authoring/build.py` генерира `windows11-screenshot.mission.json`.
- `python authoring/verify.py` проверява схемите на Teacher108 и Student108,
  метаданните и структурата без проверки; прикачва PNG и проверява байтовете,
  хеша и възстановяването на отговора.
- `python authoring/verify.py --render` отваря всички стъпки в реалния
  Student108 PreviewWindow, проверява изображението, оразмеряването и липсата
  на бутон за проверка. Накрая упражнява реалния `attach_file` обработчик с
  предварително зададен път, показването на името и възстановяването на файла.
  Тестовият PNG е екранна снимка на прозореца за преглед.

Проверките използват наличните работни копия в `work/student108-current`,
`work/Teacher108-feedback` и `work/new-systems/qt-runtime`. Резултатите и
екранните снимки са в `work/screenshot-qa`, извън Git.
