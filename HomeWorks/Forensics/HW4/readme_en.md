# Forensics – Variant 1

> **Purpose:** walkthrough and evidence pack for the laboratory task *“Network‑forensics analysis of `var1.pcap`”* (10 questions).

---

## 📁 Repository layout

| Path                        | Description                                                                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **/var1.pcap**              | raw network capture used in the analysis                                                                                                         |
| **/attacks.xlsx**           | Excel sheet with the redirect/attack chain (**answer to Q‑10**). Each row = transition step (time, source → target, mechanism, reference frame). |
| **/Вариант 1.docx**         | assignment sheet in Russian (10 questions)                                                                                                       |
| **/Новиков В.С. ДЗ 3.docx** | report template provided by lecturer                                                                                                             |
| **/docs/**                  | any additional documents (slides, notes)                                                                                                         |
| **/pics/**                  | extracted benign page assets (JPG, GIF) used as examples for **Q‑7** ("мирные загрузки")                                                         |

### `/pics` structure

| File                                                                                 | Role in report                                   |
| ------------------------------------------------------------------------------------ | ------------------------------------------------ |
| `01.jpg` … `07.jpg`                                                                  | screenshots referenced in answers Q‑1 ÷ Q‑6, Q‑8 |
| `IMG‑20130928‑WA002‑150x150.jpg`                                                     | legitimate content example for Q‑7               |
| `P1260499‑200x298.jpg`                                                               | legitimate content example for Q‑7               |
| `newsletter_on.gif`, `twitter_on.gif`, `youtubelogo_on.gif`, `squareorangedecor.gif` | small UI icons <2 KB, also cited in Q‑7          |

> *Tip:* GitHub auto‑renders images—just drop the file name in markdown (`![](pics/01.jpg)`).

---

## Quick answers (one‑line summary)

| #  | Question (ru)      | Short answer                                                                                                                   |
| -- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| 1  | IP заражённого     | **172.16.165.165**                                                                                                             |
| 2  | MAC заражённого    | **f0:19\:af:02:9b\:f1**                                                                                                        |
| 3  | Host‑name          | *(N/A – Option 12 empty)*                                                                                                      |
| 4  | Осознанные сайты   | `www.bing.com`, `www.ciniholland.nl`                                                                                           |
| 5  | Все домены         | `bing.com`, `c.bing.com`, `ciniholland.nl`, `youtube.com`, `24corp-shop.com`, `adultbiz.in`, `stand.trustandprobaterealty.com` |
| 6  | Домен malware      | **stand.trustandprobaterealty.com**                                                                                            |
| 7  | IP malware         | **37.200.69.143**                                                                                                              |
| 8  | Мирные загрузки    | favicon.ico, style.css, jquery.js, br\_logo.gif, …                                                                             |
| 9  | Вредоносные домены | 24corp‑shop.com, adultbiz.in, stand.trustandprobaterealty.com                                                                  |
| 10 | Механизм redirect  | *см. `/attacks.xlsx`*                                                                                                          |

> 📄 Полные развёрнутые ответы, скриншоты пакетов и хеши файлов — в *Новиков В.С. ДЗ 3.docx*.

---

## How to reproduce

1. **Open** `var1.pcap` in Wireshark 4.2+ with profile `profiles/forensics` (optional).
2. Follow the steps in `docs/Variant 1.docx` or section *«Methodology»* inside the report.
3. Cross‑check timestamps with `attacks.xlsx` sheet *Timeline*.
4. Compare extracted objects via `File → Export Objects → HTTP` with files in `/pics`.

---

## Author

*Student:* **Новиков В.С.**
*Course:* Cybersecurity (Forensics Lab) – HSE, 2024/25.
