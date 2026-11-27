# Правила за използване и инсталиране на периферни устройства

Стандартна мисия по урок 10, стр. 30–31 от [учебника по ИТ за 8. клас, Домино](https://ebook.domino.bg/books/8/it/#page=30).

30 стъпки: 16 информационни, 13 проверки с шест варианта и няколко верни отговора, един отворен въпрос с примерен отговор и насоки за самопроверка. Няма AI проверка, инсталиране на реално устройство, промяна на настройки или предаване на файл. UUID е постоянен в identity.json. Текстът е за начинаещи ученици.

## Съответствие с целия изходен урок

| Материал от учебника | Стъпки в мисията |
|---|---|
| Управление и видове ПУ; всички посочени входни примери | input, output, storage, communication |
| Изходни примери, включително плотер и прожектор | output |
| Запомнящи устройства, CD/DVD/Blu-ray | storage |
| Модем, хъб, рутер, суич | communication |
| Стандартен интерфейс, контролер; видео-, мрежова и звукова карта | interface |
| Задача 1: портове; целият списък от урока | ports — готов пример вместо оглед на реалния компютър |
| USB, FireWire, HDMI, DisplayPort | usb-firewire, display-ports |
| Драйвери и зависимост от устройство и ОС | drivers |
| Задача 2: свързване на принтер, Plug-and-Play | plug-and-play — обяснен пример, без изпълнение |
| IR и Wi-Fi | wireless; Bluetooth е добавен познат пример |
| Драйвер от диск или производител, указания | manufacturer |
| Регистър и задача 3: Search → Device Manager → Disk drives → Properties → Driver → Driver Details | device-manager, driver-details — готови данни и схеми |
| Основни понятия и заключителни въпроси | проверки след темите, driver-answer, summary |

Всички понятия са обяснени с предназначение и ситуация. Имената на старите портове са в кратка справочна таблица, а не като самостоятелни технически определения за заучаване.

23 реални снимки, описани в images.json, и 4 оригинални схеми. Източникът и лицензът се показват при необходимост. Учебните схеми за Device Manager са обозначени като опростени примери и не се представят като снимка на ученическия компютър. Условното име „Учебен принтер А“ и примерните данни за USB драйвера не са отчет от действително устройство.

## Фактическа проверка

- [Microsoft Learn: Plug and Play](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/introduction-to-plug-and-play) — автоматично разпознаване и настройка, използване на драйвери.
- [Microsoft: автоматично получаване на драйвери](https://support.microsoft.com/en-gb/windows/hardware/drivers/automatically-get-recommended-and-updated-hardware-drivers) — вградени драйвери, Windows Update и официална поддръжка.
- [Microsoft: Device Manager](https://support.microsoft.com/en-us/windows/update-drivers-through-device-manager-in-windows-ec62f46c-ff14-c91d-eead-d7126dc1f7b6) — групи устройства и свойства на драйверите.
- [Dell: външни портове и накрайници](https://www.dell.com/support/kbdoc/en-us/000132029/a-guide-to-the-external-ports-and-connectors-on-a-dell-computer) — предназначение и разпознаване на портовете, включително по-стари.
- [VESA: DisplayPort FAQ](https://www.displayport.org/faq/) — цифрова картина и звук.
- [USB-IF: Type-C](https://www.usb.org/sites/default/files/usb_type-c_language_product_and_packaging_guidelines_20230320.pdf) — формата USB-C не гарантира всички функции и скорости.

Уточнения спрямо неточни или прекалено общи формулировки в учебника: оптичният диск е носител и не всеки диск е записваем; „външна памет“ не означава непременно извън корпуса; HDMI не гарантира по-качествена картина от DVI; Plug-and-Play използва драйвер; контролерите могат да са вградени; Device Manager не е редакторът на системния регистър.

## Възстановяване

`python authoring/build_diagrams.py` създава схемите. `python authoring/lesson.py` създава JSON със същия UUID. build.py съдържа HTML и стъпковите функции за тази мисия.
