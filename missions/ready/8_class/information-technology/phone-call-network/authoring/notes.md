# Как пътува телефонният разговор?

Допълнителна мисия по информационни технологии за 8. клас, по одобрения план за разширяване на темата „Клетъчна мрежа“. Самостоятелно учебно съдържание с готови примери; не изисква телефон. Не замества мисията за мобилните устройства.

22 стъпки: 12 информационни, 9 проверки с шест варианта и няколко верни отговора, 1 отворен въпрос с подготвен примерен отговор. AI обратната връзка е изключена. Последната стъпка обобщава пет основни идеи.

15 различни реални снимки от Wikimedia Commons и 4 собствени учебни SVG схеми. Точните автори, лицензи и адреси са в images.json; изискваните признания за авторство се показват под снимките. Изображенията се зареждат от външни URL. Схемите са опростени и не представят мащаб или точна топология на конкретен оператор. Не се правят изводи за оборудването на конкретен обект само от обща снимка.

## Източници за фактическа проверка

- [ITU: How mobiles and wireless devices work; towers and antennas](https://www.itu.int/net4/mob/ituemf/en/emfguide_m.html) — радиовръзка, станции и свързване през мрежа.
- [GSMA: Mobile Infrastructure Investment Landscape](https://www.gsma.com/solutions-and-impact/connectivity-for-good/public-policy/wp-content/uploads/2025/03/Mobile-Infrastructure-Investment-Landscape-1.pdf) — наземна инфраструктура, транспортна мрежа и сателитно свързване на отдалечени обекти.
- [Ofcom: Standard smartphones to receive signal from space](https://www.ofcom.org.uk/spectrum/space-and-satellites/standard-smartphones-to-receive-signal-from-space?language=en) — преки сателитни услуги и зависимости от услуга и съвместимост.
- [ESA: Direct 5G connection to a low Earth orbit satellite](https://www.esa.int/Applications/Connectivity_and_Secure_Communications/World-first_direct_5G_connection_to_low_Earth_orbit_satellite_opens_new_era_for_mobile_coverage) — развитие на пряката връзка.
- [GPS.gov: GPS](https://www.gps.gov/gps) — навигационните сигнали служат за местоположение, а не за пренос на телефонен разговор.

Не се твърди, че всяка пряка сателитна услуга осигурява разговори, нито че е достъпна навсякъде. Сателитният транспорт на станция е отделен от директната връзка на телефона.

## Възпроизвеждане

`python authoring/build.py` възстановява JSON, като запазва UUID. `images.json` съдържа метаданните на снимките. Схемите са в assets; `python authoring/build_diagrams.py` ги възстановява. Проверката в реалния Student108 е извършена отделно, без промяна на библиотеката на Teacher108.

Публикуване за преглед: директният JSON в тази папка. Новата мисия не се добавя автоматично в Teacher108 и не е обявена за одобрена от учителя.
