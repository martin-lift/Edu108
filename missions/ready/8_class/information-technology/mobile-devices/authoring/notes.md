# Принципи на действие на съвременните мобилни устройства

Мисия за стандартен урок за 8. клас по урок 8, стр. 26–28 от
[електронния учебник на Домино](https://ebook.domino.bg/books/8/it/#page=26).

38 стъпки: 20 информационни, 15 проверки с шест варианта и няколко верни
отговора, 3 отворени отговора. Само сравнението на ранния и съвременния
смартфон използва AI обратна връзка от Teacher108. Останалите отворени
отговори показват предварително подготвен примерен отговор.

Ред: мобилни устройства → видове → история → първи смартфони → клетъчна
мрежа → поколения → скорост и наблюдение → Android → iOS → HarmonyOS →
наблюдение на системите → Wi-Fi → Bluetooth → GPS → избор на технология →
обобщение с пет точки. След увода няма проверка. Всяка стъпка, включително
проверките, съдържа външно изображение.

Практическите наблюдения имат готови примерни данни за ученици без собствен
телефон или подходящ достъп. Не изискват създаване на акаунт или предаване
на файл. Наблюдението на ОС обяснява структурата на обща таблица и разликата
между резултат за конкретна група и световна статистика. Wi-Fi, Bluetooth и
GPS са обяснени преди проверката, а не оставени като непредадени знания.

## Фактически уточнения спрямо учебника

- Dynabook е концепция и макет, а не продаван през 1968 г. завършен таблет.
- 1G е представено с период, без погрешна единствена световна стартова дата.
- GPRS/EDGE са развитие на преноса на данни; VoIP не е изобретен само за 4G.
- Реалната скорост зависи от условията; няма гарантирани скорости според G.
- Разграничени са Mbit/s и MB/s; примерът 80 Mbit/s = 10 MB/s изключва
  служебния обмен и приема постоянна скорост.
- 6G е разработване/стандартизиране в рамката IMT-2030, без обещана дата
  за масово използване през 2028 г.
- За iPad е посочена iPadOS; iOS е разгледана като системата на iPhone.
- За HarmonyOS не се твърди, че всяка версия е изцяло с отворен код или
  че всеки телефон Huawei непременно използва тази система.
- GPS е приемане на спътникови сигнали, а не двупосочна интернет връзка.

## Източници за сверяване

- [Dynabook, Computer History Museum](https://computerhistory.org/events/40th-anniversary-dynabook/)
- [IBM/BellSouth Simon, CHM](https://www.computerhistory.org/revolution/artifact/1733)
- [Архив на създателите на Simon](https://github.com/simoneer/history)
- [GRiDPad, CHM](https://www.computerhistory.org/revolution/artifact/1727)
- [PalmPilot, CHM](https://www.computerhistory.org/revolution/mobile-computing/18/321/1643)
- [Newton, CHM timeline](https://www.computerhistory.org/timeline/computers/)
- [Представяне на iPad, Apple, 2010](https://www.apple.com/newsroom/2010/01/27Apple-Launches-iPad/)
- [Първият Android телефон, Google, 2008](https://opensource.googleblog.com/2008/10/android-open-source-cell-phone.html)
- [Архитектура на Android, AOSP](https://source.android.com/docs/core/architecture)
- [iPadOS, Apple](https://www.apple.com/os/ipados/)
- [GSM, GPRS, EDGE, GSMA](https://www.gsma.com/about-us/gsm-technology/)
- [5G и IMT-2030, ITU](https://www.itu.int/en/mediacentre/backgrounders/Pages/5G-fifth-generation-of-mobile-technologies.aspx)
- [IMT-2030, ITU](https://www.itu.int/en/ITU-R/study-groups/rsg5/rwp5d/imt-2030/Pages/default.aspx)
- [HarmonyOS, Huawei](https://consumer.huawei.com/en/harmonyos/)
- [Годишен отчет Huawei 2024, история на HarmonyOS](https://www.huawei.com/minisite/annual-report-download/annual_report_2024_en.pdf)
- [Bluetooth SIG](https://www.bluetooth.com/learn-about-bluetooth/tech-overview/)
- [GPS.gov](https://www.gps.gov/gps)
- [GPS.gov FAQ](https://www.gps.gov/faq)

Снимките са намерени чрез търсене в Wikimedia Commons. `images.json`
съдържа точните URL, автор, лиценз и страница на всяка снимка. Използвани са
оптимизирани 960 px миниатюри от официалния сървър thumb.wikimedia.org,
когато пълноразмерният оригинал връща HTTP 429. Изображенията не се копират
в хранилището. Изискваното авторство и лиценз са изписани кратко в мисията.
Снимката на Simon е обществено достояние; GPS илюстрацията е от NOAA.

## Възпроизвеждане и проверки

`python authoring/build.py` генерира `mobile-devices.mission.json` без
допълнителни зависимости. `python authoring/verify.py` проверява схемите на
Student108/Teacher108, реда, илюстрациите, единствената AI стъпка, въпросите,
верни/частични/грешни отговори и възстановяването на отворен отговор.

`python authoring/verify.py --render` преглежда всички стъпки през реалния
Student108 PreviewWindow, проверява зареждането на всяко изображение и
липсата на хоризонтално преливане. Скриптът очаква работните копия и Qt
средата в `work/student108-current`, `work/Teacher108-feedback` и
`work/new-systems/qt-runtime` до папката на хранилището. Снимките от прегледа
и резултатите се записват в `work/mobile-qa`, извън Git.
