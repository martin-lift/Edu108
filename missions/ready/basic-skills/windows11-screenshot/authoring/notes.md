# Екранна снимка (Screenshot) в Windows 11 — заснемане и записване

Категория: **Базови умения**. Мисията няма клас, предмет или обвързване с
конкретен урок: полетата `class_name`, `subject` и `lesson` са пропуснати.

Текущата изрично зададена структура има предимство пред по-ранното изискване
последната стъпка да е файл: 10 стъпки, от които 8 информационни и 2 за файл.
Няма въпроси, тестове или AI проверка. Първо е целият екран, след това област.

1. Увод и пример с Calculator.
2. Windows + Print Screen → автоматичен PNG → описателно име → предаване.
   Алтернатива с мишка: Start → Snipping Tool → Full screen → New → Save as.
3. Windows + Shift + S → Rectangle → Paint → Paste → Save → отделно предаване.
   Алтернативи: Start → Snipping Tool → Rectangle → New; Paste в лентата на
   Paint; File → Save as → PNG picture.
4. Последна информационна стъпка: самостоятелният Prt Scr и настройката му.

Снимката на целия екран е в Pictures / Screenshots; при автоматично записване
се преименува през контекстното меню. При записване от Snipping Tool папката
се създава само ако липсва. Папката за второто изображение в Documents се
създава при Save as в Paint. Няма предварително създаване на папки.

Примерни имена: `screenshot-full-screen Martin.png` и
`screenshot-calculator Martin.png`; Martin се заменя с името на ученика.
Първият файл остава записан и приложен при предаването на втория. След двете
предавания ученикът завършва мисията от информационната стъпка за Prt Scr.

Всяка обяснена клавишна комбинация има непосредствена алтернатива през
менюта/бутони. Запазен е пълният абзац за различните надписи на Prt Scr и Fn.
Обяснено е пренасочването на Pictures към OneDrive; не се разчита на
автоматичното записване на Snipping Tool, зависещо от версия и настройки.

Дават се български и английски имена на основните елементи. Обяснени са
клипбордът, PNG и намирането на папката. Опитите се записват с различни имена.
Очакват се две собствени снимки — цял екран и област, PNG или JPG/JPEG до
20 MB всяка. Това е условие в текста: форматът на мисията не
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
  метаданните и структурата без проверки; прикачва два PNG файла и проверява
  байтовете, хеша и възстановяването на двата отделни отговора.
- `python authoring/verify.py --render` отваря всички стъпки в реалния
  Student108 PreviewWindow, проверява изображението, оразмеряването и липсата
  на бутон за проверка. В двете стъпки за файл упражнява реалния `attach_file`
  обработчик, показването на съответното име и възстановяването. При достигане
  на края проверява, че двата файла са запазени независимо. Тестовите PNG са
  заснети от целия прозорец за преглед и само неговата област за съдържание.

Проверките използват наличните работни копия в `work/student108-current`,
`work/Teacher108-feedback` и `work/new-systems/qt-runtime`. Резултатите и
екранните снимки са в `work/screenshot-qa`, извън Git.
