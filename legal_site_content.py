"""Confirmed service-provider facts from the original Russian contact page.

The service provider is not assumed to be the personal-data operator.
"""

from html import escape


ENTITY_NAME = 'ООО «ИННОВАЦИОННЫЕ ПРАВОВЫЕ РЕШЕНИЯ»'
OGRN = '1247700538370'
INN = '9721237517'
KPP = '772101001'
ADDRESS = 'г. Москва, ул. Маршала Василевского, д. 17'

LABELS = {
    'ru': ('Исполнитель юридических услуг', 'Юридическая информация', 'Адрес'),
    'fr': ('Prestataire des services juridiques', 'Informations juridiques', 'Adresse'),
    'en': ('Legal service provider', 'Legal details', 'Address'),
}


def provider_block(lang):
    """A visible, full legal-identity block for a contact page."""
    role, heading, address_label = LABELS[lang]
    return (
        '<section class="sr-sec alt"><div class="sr-width"><div class="sr-legal-identity">'
        f'<span class="sr-eyebrow">{escape(role)}</span><h2>{escape(heading)}</h2>'
        f'<p><strong>{escape(ENTITY_NAME)}</strong></p>'
        f'<dl><div><dt>ОГРН</dt><dd>{OGRN}</dd></div>'
        f'<div><dt>ИНН</dt><dd>{INN}</dd></div>'
        f'<div><dt>КПП</dt><dd>{KPP}</dd></div></dl>'
        f'<p>{escape(address_label)}: {escape(ADDRESS)}</p>'
        '</div></div></section>'
    )


def provider_footer(lang):
    """Compact legal identity for every language, without privacy-operator claims."""
    role = LABELS[lang][0]
    return (
        f'<p class="sr-small">{escape(role)}: {escape(ENTITY_NAME)}'
        f' · ОГРН {OGRN} · ИНН {INN}</p>'
    )


LEGAL_CSS = '''
.sr-legal-identity{max-width:880px;border:1px solid var(--line);background:var(--parchment-2);padding:clamp(24px,4vw,42px)}
.sr-legal-identity h2{margin:8px 0 18px}
.sr-legal-identity p{margin:14px 0 0;overflow-wrap:anywhere}
.sr-legal-identity dl{display:flex;flex-wrap:wrap;gap:12px 30px;margin:22px 0 0}
.sr-legal-identity dl div{min-width:145px}
.sr-legal-identity dt{font-size:12px;color:var(--ink-text-soft)}
.sr-legal-identity dd{margin:2px 0 0;font-weight:600;overflow-wrap:anywhere}
'''


DATA_NOTICE = {
    'ru': {
        'title': 'Как работают каналы связи',
        'description': 'Информация о переходе из SalutRussie в почту и мессенджеры.',
        'body': (
            '<article class="sr-content"><p>Для обращения вы можете выбрать электронную почту, '
            'WhatsApp или Telegram. Сайт открывает выбранный сервис; сообщение отправляется только '
            'после вашего действия в нём.</p>'
            '<h2>Перед отправкой сообщения</h2><p>Кнопки выбора консультации могут подготовить '
            'текст с темой обращения. Вы можете изменить или удалить его перед отправкой. '
            'Не передавайте паспортные данные и другие чувствительные документы в первом сообщении.</p>'
            '<h2>Сторонние сервисы</h2><p>При переходе в почтовое приложение или мессенджер '
            'дальнейшая работа с сообщением зависит от выбранного вами сервиса и его правил. '
            'Если удобнее, напишите на <a href="mailto:salutrussie@salutrussie.ru">salutrussie@salutrussie.ru</a>.</p>'
            '</article>'
        ),
    },
    'fr': {
        'title': 'Fonctionnement des moyens de contact',
        'description': 'Informations sur l’ouverture de la messagerie et du courrier électronique depuis SalutRussie.',
        'body': (
            '<article class="sr-content"><p>Vous pouvez nous contacter par courrier électronique, '
            'WhatsApp ou Telegram. Le site ouvre le service choisi ; votre message n’est envoyé '
            'qu’après une action de votre part dans ce service.</p>'
            '<h2>Avant d’envoyer un message</h2><p>Le choix d’une consultation peut préparer '
            'un texte indiquant le sujet de votre demande. Vous pouvez le modifier ou l’effacer '
            'avant l’envoi. Évitez de joindre des passeports ou d’autres documents sensibles à '
            'votre premier message.</p>'
            '<h2>Services externes</h2><p>Après l’ouverture de votre application de courrier '
            'ou de messagerie, le traitement du message dépend de ce service et de ses règles. '
            'Vous pouvez aussi écrire à <a href="mailto:salutrussie@salutrussie.ru">salutrussie@salutrussie.ru</a>.</p>'
            '</article>'
        ),
    },
}


def data_notice(lang):
    """Factual contact-channel notice, not a personal-data processing policy."""
    return DATA_NOTICE[lang]
