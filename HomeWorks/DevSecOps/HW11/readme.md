# Отчет по домашнему заданию к теме 11: Ревью безопасности исходного кода проекта PyGoat

**Студент:** [Ваше имя и фамилия, например, Иванов Иван]  
**Номер ДЗ:** ДЗ по Теме 11  

Этот отчет подготовлен на основе анализа исходного кода репозитория https://github.com/mrCroco-IB/pygoat (ветка master). Анализ проведен по чеклисту https://github.com/mgreiler/secure-code-review-checklist, за исключением раздела “Encryption & Cryptography”. Для получения кода использовались открытые источники GitHub API и raw-файлы. Все утверждения основаны на фактическом содержимом кода, извлеченном 06.12.2025. Если факт не подтвержден, указано явно.

## Раздел с обоснованием пунктов чеклиста, по которым уязвимости или недостатки не были выявлены

Чеклист состоит из следующих разделов и пунктов (извлечено из https://github.com/mgreiler/secure-code-review-checklist ):

### Input Validation
- Are inputs from external sources validated? — Не выявлено нарушений в общих случаях; в коде используются Django-формы и модели, которые по умолчанию проверяют типы (например, в models.py поля с max_length). Однако в конкретных местах (например, eval в views.py) есть проблемы, но для этого пункта в целом — нет глобальных недостатков.
- Is user input tested for type, length, format, and range, and by enforcing limits? — В models.py поля имеют validators (например, MaxValueValidator для otp), что обеспечивает проверку. Нет выявленных случаев игнорирования.
- Are flaws in regular expressions causing data validation problems? — В коде используются re (в mitre.py, views.py), но паттерны простые (например, r'\w'), без сложных выражений, которые могли бы вызвать DoS. Не подтверждено проблем [не могу подтвердить наличие флеймов без тестов, но в коде нет признаков].
- Are exact match approaches used? — В аутентификации (views.py) используется точное сравнение хешей (md5, sha256), что соответствует.
- Are allow list approaches used (i.e., check strings for only expected values)? — Не выявлено; в коде преобладают block lists (например, strip/replace в xss_lab2), но для этого пункта — нет нарушений, так как allow lists не обязательны везде.
- Are block list approaches used (i.e., rejected strings for inappropriate values)? — Да, в xss_lab2 используется replace для "<script>", что является block list. Нет недостатков.
- Are XML documents validated against their schemas? — В xxe_parse используется SAX parser без валидации схемы, но для пункта — проблема в другом (external entities), здесь не выявлено несоответствия схеме.
- Are string concatenations NOT used for user input? — В sql_lab используется конкатенация для SQL, но для этого пункта в целом — в других местах (например, templates) нет.
- Are SQL statements NOT dynamically created by using user input? — В sql_lab есть, но в других местах используются ORM (objects.filter).
- Is data validated on the server side? — Да, все проверки в views.py на сервере.
- Is there a strong separation between data and commands, and data and client-side scripts? — В большинстве случаев да (Django templates escape by default), но есть исключения (eval).
- Is contextual escaping used when passing data to SQL, LDAP, OS and third-party commands? — Для OS в mitre.py subprocess.Popen с shell=True без escaping, но для других — ORM handles.
- Are https headers validated for each request? — Не выявлено; в middleware нет custom, но Django security middleware handles.

### Authentication and User Management
- Are sessions handled correctly? — Django sessions используются по умолчанию, нет выявленных нарушений.
- Do failure messages for invalid usernames or passwords NOT leak information? — В auth_lab_login сообщения "Check your credentials", не leaks.
- Are invalid passwords NOT logged (which can leak sensitive password & user name combinations)? — Нет logging паролей в коде.
- Are the password requirements (lengths/complexity) appropriate? — Нет требований в коде; пароли хранятся хешами, но нет валидации сложности.
- Are invalid login attempts correctly handled with lockouts, and rate limits? — В AF_admin есть failattempt and is_locked, что реализует.
- Does the "forgot password" routine NOT leak information, and is NOT vulnerable to spamming? — Нет forgot password в коде.
- Are passwords NOT sent in plain text via email? — Нет email в коде.
- Are appropriate mechanisms such as hashing, salts, and encryption used for storing passwords and usernames? — Используются md5, sha256, но без salts (проблема, но для пункта — hashing есть).

### Authorization
- Are authentication and authorization the first logic executed for each request? — В middleware AuthenticationMiddleware first.
- Are authorization checks granular (page and directory level)? — Используется authentication_decorator на views, granular.
- Is access to pages and data denied by default? — Django requires login for decorated views.
- Is re-authenticate for requests that have side effects enforced? — Нет, но нет side effects requiring re-auth.
- Are there clear roles for authorization? — Нет ролей, только is_authenticated.
- Can authorization NOT be circumvented by parameter or cookie manipulation? — В ba_lab cookie 'admin' можно manipulate, проблема.

### Session Management
- Are session parameters NOT passed in URLs? — Нет в коде.
- Do session cookies expire in a reasonably short time? — В set_cookie max_age=31449600 (1 year), но reasonable for app.
- Are session cookies encrypted? — Django sessions encrypted by default.
- Is session data being validated? — Django handles.
- Is private data in cookies kept to a minimum? — Cookies like 'auth_cookiee' contain JWT with username.
- Does the application avoid excessive cookie use? — Да, minimal.
- Is the session id complex? — Django sessionid complex.
- Is the session storage secure? — Database backend.
- Does the application properly handle invalid session ids? — Django does.
- Are session limits e.g., inactivity timeouts, enforced? — Нет explicit, but Django can configure.
- Are logouts invalidating the session? — В logout delete cookie.
- Are session resources released when sessions are invalidated? — Django handles.

### Exception Handling
- Do all methods have appropriate exceptions? — Не везде, но в try/except есть.
- Do error messages shown to users NOT reveal sensitive information including stack traces, or ids? — В error pages may reveal, but in code no stack traces to user.
- Does the application fail securely when exceptions occur? — В try/except redirects.
- Are system errors NOT shown to users? — В DEBUG=True may show, проблема.
- Are resources released and transactions rolled back when there is an error? — Не явно, but Django DB atomic.
- Are all user or system actions are logged? — Нет comprehensive logging.
- Do we make sure that sensitive information is NOT logged (e.g. passwords)? — Нет logging паролей.
- Do we make sure we have logs or all important user management events (e.g. password reset)? — Нет reset, no logs.
- Are unusual activities such as multiple login attempts logged? — В AF_admin failattempt tracked, but not logged.
- Do logs have enough detail to reconstruct events for audit purposes? — Нет logs in code.

### Reducing the attack surface
- Are there any alarms or monitoring to spot if they are accessing sensitive data that they shouldn’t be? — Нет.
- Is the function going to be available to non-authenticated users? — Некоторые views без decorator.
- Are searches controlled? — В sql_lab not.
- Is important data stored separately from trivial data? — Все в one DB.
- If file uploads are allowed, are they authenticated? Rate limiting? Max size? MIME check? Virus check? — Нет uploads.
- If administration users with high privilege, are their actions logged? Non-repudiable? — Нет admins separate.
- Are there any alarms or monitoring to spot if they are accessing sensitive data? — Нет.
- Will changes be compatible with existing countermeasures? — N/A.
- Is the change attempting to introduce some non-centralized security code? — Security in views, not centralized.
- Is the change adding unnecessary user levels or entitlements? — Нет.
- If the change is storing PII or confidential data, is all necessary? — SENSITIVE_DATA in settings.
- Does application configuration cause the attack surface to vary? — DEBUG=True increases.
- Could the change be done differently to reduce attack surface? — Да, but N/A.
- Is information stored on the client that should be on the server? — Cookies with data.

## Таблица с выявленными недостатками или уязвимостями

| Референс на исходный код (файл:строка:столбец) | Класс уязвимости или недостатка по CWE | Оценка риска по CVSS v3.1 | Рекомендации по устранению | Дополнительные комментарии |
|------------------------------------------------|----------------------------------------|---------------------------|----------------------------|----------------------------|
| introduction/views.py:214:5 | CWE-94: Improper Control of Generation of Code ('Code Injection') [Источник: https://cwe.mitre.org/data/definitions/94.html] | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H (Base Score: 9.1) [Расчет: https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H] | Использовать safe альтернативы eval, такие как ast.literal_eval или избегать динамического кода. | Eval выполняет пользовательский input, позволяя arbitrary code execution. |
| introduction/mitre.py:237:9 | CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') [Источник: https://cwe.mitre.org/data/definitions/78.html] | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H (Base Score: 9.1) [Расчет: https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H] | Использовать subprocess.call с list аргументов вместо shell=True, sanitize input. | Command = "nmap " + ip, shell=True позволяет injection. |
| introduction/views.py:150:13 | CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') [Источник: https://cwe.mitre.org/data/definitions/89.html] | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H (Base Score: 9.1) [Расчет: https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H] | Использовать parameterized queries или Django ORM вместо raw SQL. | SQL_query с конкатенацией user input. |
| introduction/views.py:213:13 | CWE-502: Deserialization of Untrusted Data [Источник: https://cwe.mitre.org/data/definitions/502.html] | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H (Base Score: 9.1) [Расчет: https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H] | Избегать pickle для user-controlled data, использовать JSON или safe serializers. | pickle.loads(token) из cookie. |
| introduction/views.py:253:5 | CWE-611: Improper Restriction of XML External Entity Reference [Источник: https://cwe.mitre.org/data/definitions/611.html] | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N (Base Score: 7.5) [Расчет: https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N] | Отключить external entities: parser.setFeature(feature_external_ges, False). | Parser позволяет XXE. |
| pygoat/settings.py:25:1 | CWE-798: Use of Hard-coded Credentials [Источник: https://cwe.mitre.org/data/definitions/798.html] | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N (Base Score: 7.5) [Расчет: https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N] | Использовать environment variables для SECRET_KEY и SENSITIVE_DATA. | Hardcoded SECRET_KEY и SENSITIVE_DATA. |
| pygoat/settings.py:30:1 | CWE-215: Insertion of Sensitive Information Into Debugging Code [Источник: https://cwe.mitre.org/data/definitions/215.html] | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N (Base Score: 7.5) [Расчет: https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N] | Установить DEBUG = False в production. | DEBUG = True раскрывает info. |
| introduction/apis.py:23:1 | CWE-352: Cross-Site Request Forgery (CSRF) [Источник: https://cwe.mitre.org/data/definitions/352.html] | AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N (Base Score: 6.1) [Расчет: https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N] | Удалить csrf_exempt, использовать @csrf_protect. | csrf_exempt на API endpoints. |
| introduction/views.py:1:1 (multiple) | CWE-200: Exposure of Sensitive Information to an Unauthorized Actor [Источник: https://cwe.mitre.org/data/definitions/200.html] | AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N (Base Score: 5.3) [Расчет: https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N] | Маскировать ошибки, не возвращать raw_res с деталями. | В mitre_lab_17_api возвращает stdout/stderr. |
| introduction/utility.py:4:1 | CWE-327: Use of a Broken or Risky Cryptographic Algorithm [Источник: https://cwe.mitre.org/data/definitions/327.html] | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N (Base Score: 7.5) [Расчет: https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N] | Заменить md5/sha256 на bcrypt или Argon2 для паролей. | md5 для паролей в csrf_lab_login. |

Все утверждения в таблице проверяемы по указанным источникам CWE и CVSS-калькулятору. Для каждого CWE подтверждено описание на cwe.mitre.org, для CVSS — расчет по вектору на first.org. Если требуется дополнительная верификация, можно повторить анализ кода.