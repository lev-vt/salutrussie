# Проект политики персональных данных / Projet de politique de confidentialité

**Внутренний черновик от 21.11.2026. Не переносить на сайт и не объявлять утверждённой политикой до проверки владельцем и юристом.**

Основа для проверки: [Федеральный закон № 152-ФЗ «О персональных данных», ст. 18.1](https://mintrud.gov.ru/docs/laws/130). В действующей сборке нет формы отправки данных на сервер и счётчика аналитики; шрифты размещены локально. Ссылки на WhatsApp, Telegram и email открывают внешние приложения, где посетитель сам решает, отправлять ли сообщение. Фактическую обработку входящих обращений, серверные журналы и подрядчиков нужно подтвердить перед утверждением текста.

## Факты, которые требуется заполнить

| Поле | Статус |
|---|---|
| `[[OPERATOR]]` — лицо, оказывающее услуги и обрабатывающее обращения | Требуется решение владельца: исходные RU и FR страницы указывают разных лиц |
| `[[ADDRESS]]` — адрес оператора для обращений о данных | Не подтверждён |
| `[[DOMAIN]]` — основной домен сайта | Не подтверждён |
| `[[EMAIL]]` — канал обращений о персональных данных | Проверить, что `salutrussie@salutrussie.ru` используется для этого |
| `[[HOST]]` — хостинг и технические журналы | Определить при размещении |
| `[[RETENTION]]` — сроки хранения входящих обращений и критерии удаления | Определить по фактическому процессу |
| `[[PROCESSORS]]` — лица, которым поручена обработка, если есть | Подтвердить |
| `[[SECURITY]]` — фактически применяемые меры защиты | Подтвердить без общих обещаний |
| `[[LEGAL_BASES]]` — основания обработки по целям | Согласовать с юристом после описания реального процесса |
| `[[TRANSFERS]]` — использование зарубежных сервисов и связанные решения | Согласовать с юристом и владельцем |

## Русская версия — рабочий текст

### 1. Оператор и область действия

Настоящая политика описывает обработку персональных данных в связи с сайтом `[[DOMAIN]]` и обращениями в SalutRussie. Оператор: `[[OPERATOR]]`, адрес: `[[ADDRESS]]`, контакт по вопросам персональных данных: `[[EMAIL]]`. Политика применяется к сведениям, которые посетитель добровольно передаёт при обращении, а также к техническим данным, которые могут возникать при открытии сайта в инфраструктуре `[[HOST]]`.

### 2. Какие данные и для чего обрабатываются

При обращении посетитель может сообщить имя, контакт для ответа и описание вопроса. Цель — принять обращение, ответить на него, оценить возможность и объём юридической работы и, если стороны договорятся, подготовить дальнейшее взаимодействие. Не направляйте паспорт, медицинские сведения и другие чувствительные документы в первом сообщении. Состав данных, основания обработки и дальнейшая работа с документами определяются отдельно для конкретного поручения: `[[LEGAL_BASES]]`.

В действующей версии сайта нет анкеты, которая отправляет данные на сервер SalutRussie, и нет подключённого счётчика аналитики. При посещении хостинг может формировать технические журналы, включая сетевой адрес и время запроса. Их фактический состав и срок хранения: `[[HOST]]`, `[[RETENTION]]`. Шрифты и иконка загружаются с этого же сайта.

### 3. Мессенджеры, почта и другие участники

Кнопки консультаций открывают WhatsApp, Telegram или почтовое приложение. Текст сообщения для WhatsApp и почты предлагается к отправке, а для Telegram может быть скопирован в буфер обмена. Сайт сам не отправляет сообщение. После перехода применяются условия выбранного сервиса. Использование таких сервисов и возможная передача данных через них должны быть описаны с учётом фактической практики: `[[TRANSFERS]]`. Лица, которым поручена обработка данных оператором, если они есть: `[[PROCESSORS]]`.

### 4. Хранение, защита и обращения посетителей

Оператор хранит сведения не дольше периода, определённого фактической целью и применимыми обязанностями: `[[RETENTION]]`. Применяемые организационные и технические меры защиты: `[[SECURITY]]`. По адресу `[[EMAIL]]` можно запросить сведения об обработке своих данных, уточнение или прекращение обработки в предусмотренных законом случаях. Для рассмотрения запроса оператору может потребоваться подтвердить личность заявителя. Изменения политики публикуются на `[[DOMAIN]]` с датой обновления.

## Version française — projet de travail

### 1. Responsable et champ d’application

Cette politique décrit le traitement des données personnelles lié au site `[[DOMAIN]]` et aux demandes adressées à SalutRussie. Responsable : `[[OPERATOR]]`, adresse : `[[ADDRESS]]`, contact pour les questions relatives aux données : `[[EMAIL]]`. Elle concerne les informations communiquées volontairement par un visiteur ainsi que les données techniques éventuellement produites par l’infrastructure `[[HOST]]` lors de l’accès au site.

### 2. Données et finalités

Une personne qui nous contacte peut indiquer son nom, un moyen de réponse et la description de sa question. Ces éléments servent à recevoir la demande, y répondre, déterminer si une intervention juridique est possible et, si les parties en conviennent, organiser la suite. N’envoyez pas de passeport, de renseignements médicaux ou d’autres documents sensibles dans le premier message. Les données nécessaires, les fondements du traitement et les pièces d’un dossier ultérieur sont définis séparément : `[[LEGAL_BASES]]`.

La version actuelle du site ne comporte pas de formulaire transmettant des données au serveur de SalutRussie et n’intègre pas d’outil d’analyse d’audience. L’hébergeur peut conserver des journaux techniques, notamment l’adresse réseau et l’heure d’une requête. Leur contenu exact et la durée de conservation restent à confirmer : `[[HOST]]`, `[[RETENTION]]`. Les polices et l’icône sont servies par le site lui-même.

### 3. Messageries, courriel et autres intervenants

Les boutons de consultation ouvrent WhatsApp, Telegram ou une application de courriel. Un texte est proposé pour WhatsApp et le courriel ; pour Telegram, il peut être copié dans le presse-papiers. Le site n’envoie pas le message à votre place. Les conditions du service choisi s’appliquent ensuite. Son utilisation et les éventuels transferts de données doivent être décrits selon la pratique réelle : `[[TRANSFERS]]`. Les prestataires chargés du traitement pour le responsable, le cas échéant : `[[PROCESSORS]]`.

### 4. Conservation, protection et demandes

Les informations ne sont conservées que pendant la période justifiée par la finalité réelle et les obligations applicables : `[[RETENTION]]`. Mesures organisationnelles et techniques effectivement appliquées : `[[SECURITY]]`. À l’adresse `[[EMAIL]]`, une personne peut demander des informations sur le traitement, la rectification ou l’arrêt du traitement dans les cas prévus par la loi. Une vérification de l’identité du demandeur peut être nécessaire. Les modifications de cette politique sont publiées sur `[[DOMAIN]]` avec leur date de mise à jour.
