# **Zadání soutěžních úloh**

## **Kategorie programování mikrořadičů**

**23.-25. dubna 2026**  
Soutěž v programování – 40\. ročník  
Krajské kolo 2025/2026  
Na řešení úlohy máte 4 hodiny čistého času.  
Pro řešení můžete použít vývojovou platformu s mikrokontrolerem dle své preference (např. Arduino, Raspberry PI, ESP8266/32, FRDM, STM32, micro:bit, PicAxe, BASIC Stamp, AVR, PIC ...).  
Pro řešení úlohy budete dále potřebovat:

* MCU dle vlastního výběru (Arduino, ...)  
* alfanumerický nebo grafický displej na I2C/SPI  
* 6x barevné LED (2x modrá, 2x zelená, 2x červená)  
* 1x přepínač 4 pozice  
* 1x potenciometr/trimr  
* 1x rotační enkodér s tlačítkem  
* 1x 2-kanálový relé modul  
* 4xAA battery holder nebo DC adapter 6/12V  
* 1x optická závora  
* 1x disk pro optické enkodéry  
* 1x DC motor s převodovkou  
* 1x PWM MOSFET  
* 2x tlačítko  
* nepájivé pole, propojovací kablíky, odpory, další potřebné součástky pro připojení

## **Řízení DC motoru**

**Obecné zadání**  
Zapojte takový obvod, který vám umožní řídit otáčky a směr otáčení DC motoru a za pomoci zpětné vazby měřit otáčky pomocí optického senzoru. Dále vytvořte vhodnou vizualizaci jednotlivých stavů motoru, které budete zobrazovat na LCD/OLED displeji a případně na LED. Zpracujte dokumentaci. Přiložte grafické schéma zapojení.  
Úloha se dělí na 4 režimy, které se budou volit pomocí přepínače se 4 pozicemi.  
**Realizace zapojení pro řízení DC motoru**  
K napájení DC motoru použijte bateriový holder nebo jiný zdroj požadovaného napájení.

### **Pokyny k implementaci**

V kódu pojmenovávejte jednotlivé identifikátory jednotně pouze česky nebo pouze anglicky. Program vhodně strukturujte do podprogramů a na důležitých místech doplňte komentáři.

### **Režim 0: Ovládání směru a spínání otáčení motoru**

S využitím dvoukanálového relé vytvořte zapojení, které umožní změnu směru otáčení motoru a jeho zapnutí a vypnutí. Zapojte displej a vytvořte níže popsanou vizualizaci. Kromě displejové vizualizace realizujte i LED vizualizaci, kdy rozsvícená zelená LED znamená, že motor se netočí a červená, že se točí.  
Pomocí 2 modrých LED ukazujte, zda se motor točí doleva nebo doprava. Jedna modrá LED znamená doleva a dvě modré LED doprava.  
Tlačítko 1 bude sloužit pro START/STOP. Tlačítko 2 pro změnu směru otáčení. (Před změnou směru otáčení se motor musí viditelně zastavit a po změně směru otáčení znovu spustit). Po změně režimu nebo po resetu dojde vždy k zastavení motoru.  
**Požadavky na vizualizaci**

* **První řádek:** Směr otáčení nebo zastavený motor.  
* **Pozice dva:** Display uživateli zobrazuje „Progress bar“, který zprostředka baru zobrazuje, na jakou stranu se motor otáčí. Pokud se motor otočí doleva, tak „Progress bar“ se bude plnit směrem doleva, a pokud doprava, tak se „Progress bar“ bude pohybovat směrem doprava. Pokud motor bude vypnutý, tak „Progress bar“ bude mít čárku uprostřed.

*Obr.1: Ukázka vizualizace (přepis z obrázku)*  
Stav STOP:  
\+----------------+  
| SMER: STOP     |  
|       \[|\]      |  
\+----------------+

Stav DOLEVA:  
\+----------------+  
| SMER: DOLEVA   |  
|  \[||||| \]      |  
\+----------------+

Stav DOPRAVA:  
\+----------------+  
| SMER: DOPRAVA  |  
|       \[ |||||\] |  
\+----------------+

### **Režim 1: Ovládání rychlosti otáčení a plynulá změna směru otáčení**

Do zapojení DC motoru přidejte MOSFET tak, aby bylo možné nastavit otáčky motoru. Rychlost otáčení bude řízena pomocí potenciometru/trimru v rozsahu 0 až MAX. Při změně směru otáčení dojde nejdříve k PLYNULÉMU zastavení a roztočení motoru na požadovanou hodnotu. LCD displej bude na prvním řádku zobrazovat směr otáčení, hodnotu potenciometru v % číselně a na bargrafu graficky. Stav potenciometru (rychlost otáčení) zobrazujte zároveň pomocí LED diod rovnoměrně od 0.. žádná nesvítí, 1 zelená, 2 zelené, 2 modré, 1 červená, 2 červené .. MAX otáčky. Tlačítka 1 a 2 budou mít stejnou funkci jako v Režimu 0\. Při změně režimu nebo po resetu dojde vždy k zastavení motoru. Hodnoty zobrazované na displeji průběžně aktualizujte.

### **Režim 2: Měření otáček pomocí optického snímače a nastavení otáček rotačním enkodérem**

Pomocí optického snímače a disku pro optické enkodéry měřte počet otáček za 1s. Změřený počet otáček zobrazujte číselně na prvním řádku displeje. Nastavení otáček realizujte rotačním enkodérem. Každá změna stavu rotačního enkodéru bude znamenat změnu o 1/100 z MAX počtu otáček. Tlačítka 1 a 2 budou mít stejnou funkci. Při změně režimu nebo po resetu dojde vždy k zastavení motoru. LED mají stejnou funkci jako v Režimu 1\.  
Hodnoty zobrazované na displeji průběžně aktualizujte.

### **Režim 3: Sekvenční automat**

Sekvenčním automatem jef myšlena simulace automatizovaného pracovního procesu, při kterém motor prochází předem definovaným cyklem bez dalšího zásahu uživatele. Vytvořte automat, který bude zpracovávat jednoduchou sekvenci příkazů zadanou pomocí textových řetězců přímo v programu a následně zadaných pomocí sériové linky z PC. Při provádění příkazů zadaných v programu posílejte jejich textovou podobu po sériové lince do PC.  
Syntaxe příkazu: TxxxL/RSyyyDzz, T .. doba otáčení, L nebo R .. směr otáčení, S .. počet otáček za 1s, D .. prodleva mezi dalším krokem v sekundách. Příklad: T010LS050D05  
Při změně režimu nebo po resetu dojde k novému spuštění celé sekvence. Hodnoty zobrazované na displeji průběžně aktualizujte. Tlačítko 1 umožní přerušit aktuální příkaz a tlačítko 2 je v tomto režimu neaktivní. LED mají stejnou funkci jako v Režim 1\.  
Při změně směru nebo rychlosti dojde k PLYNULÉMU zastavení nebo postupné změně hodnoty.

### **Požadovaný výstup práce**

* Funkční sestavený obvod.  
* Dostatečně komentovaný a strukturovaný zdrojový kód.  
* Dokumentace v textovém souboru readme.txt bude obsahovat popis zapojení vstupně-výstupních pinů a výčet nerealizovaných funkcí. *(pozn. konec slova pinů byl na fotce uříznutý)*  
* Schéma zapojení v souboru schematics.png