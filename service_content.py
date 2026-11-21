"""Service overview copy for the established RU/FR sections."""
from html import escape

CONTENT = {
 'migration': {
  'ru': dict(lead='Миграционный вопрос начинается с точного статуса человека: гражданство, основание въезда, документы, сроки и цель проживания. Мы разбираем эти факты, сравниваем доступные правовые маршруты и согласуем последовательность действий. Для разных членов семьи или сотрудников порядок может отличаться.',
    cards=[('Статус и документы','Проверяем имеющиеся визы, РВП, ВНЖ, решения и данные в документах.'),('Маршрут оформления','Оцениваем применимое основание, требования и последовательность обращений.'),('Сложные ситуации','Разбираем отказ, противоречия в документах и возможные способы защиты.')],
    prepare=['Гражданство и место постоянного проживания каждого заявителя','Цель и предполагаемые даты въезда или продолжения проживания','Копии имеющихся решений и список ранее поданных заявлений','Вопросы о семье, работе, учёбе или бизнесе, влияющие на маршрут'],
    example='Например, семья уже живёт в разных странах и планирует общий переезд. Сначала мы составим отдельную карту статуса каждого человека и только затем общий календарь действий.',
    link=('/ru/knowledge/articles/how-to-choose-residence/','Как выбрать основание для проживания')),
  'fr': dict(lead='La démarche commence par le statut précis de chaque personne : nationalité, entrée, documents, échéances et projet de séjour. Nous analysons les faits avant de choisir la voie juridique et l’ordre des démarches. Une même famille peut nécessiter plusieurs parcours.',
    cards=[('Statut et pièces','Examen des visas, permis, décisions et incohérences éventuelles.'),('Voie juridique','Analyse du fondement, des exigences et de la séquence de dépôt.'),('Dossiers complexes','Étude des refus, des contradictions et des moyens de défense.')],
    prepare=['Nationalité et résidence permanente de chaque personne','Objectif du séjour et dates envisagées','Décisions déjà reçues et demandes antérieures','Éléments familiaux, professionnels ou universitaires utiles'],
    example='Une famille vivant dans plusieurs pays ne dispose pas nécessairement d’un seul parcours. Une fiche de statut par personne permet de construire ensuite un calendrier commun.',
    link=('/fr/knowledge/articles/how-to-choose-residence/','Choisir son statut de séjour')),
 },
 'real-estate': {
  'ru': dict(lead='Аренда и покупка жилья требуют проверки не только цены и объекта. Важно установить полномочия сторон, прочитать договор, понять ограничения и зафиксировать условия передачи денег. Для иностранного гражданина вопрос проживания и миграционного учёта рассматривается отдельно.',
    cards=[('Аренда','Сверяем стороны, адрес, платежи, обеспечительный платёж и акт передачи.'),('Покупка','Проверяем сведения об объекте, права, ограничения и порядок расчётов.'),('Юридическая проверка','Составляем список документов и рисков до подписания обязательств.')],
    prepare=['Адрес и описание объекта','Проект договора и сведения о подписантах','Документы об объекте, которые уже предоставлены','Планируемые платежи, сроки и вопросы о проживании'],
    example='Если договор предлагает подписать представитель, а деньги просят отправить другому лицу, сначала выясните полномочия и основание платежа. Это нужно сделать до перевода средств.',
    link=('/ru/knowledge/articles/renting-a-home/','Что проверить перед арендой')),
  'fr': dict(lead='Louer ou acheter un logement exige de vérifier les parties, l’actif, le contrat et les paiements. Pour un ressortissant étranger, les démarches liées au séjour et à l’enregistrement migratoire se traitent séparément du contrat immobilier.',
    cards=[('Location','Parties, adresse, dépôt, paiements et état des lieux.'),('Achat','Droits sur le bien, restrictions et modalités de règlement.'),('Vérification juridique','Documents et risques à examiner avant de s’engager.')],
    prepare=['Adresse et description du bien','Projet de contrat et identité des signataires','Documents déjà transmis sur le bien','Paiements, calendrier et questions de séjour'],
    example='Si un représentant signe mais qu’un tiers reçoit le paiement, demandez d’abord les pouvoirs du signataire et l’explication du paiement.',
    link=('/fr/knowledge/articles/renting-a-home/','Points à vérifier avant de louer')),
 },
 'business': {
  'ru': dict(lead='Создание бизнеса с иностранным участием начинается с модели деятельности, распределения полномочий и источников финансирования. Выбор формы компании или ИП, миграционный статус участников, налоги и разрешения по отдельным видам деятельности — разные блоки проверки.',
    cards=[('Компания и участники','Схема владения, руководитель, адрес и корпоративные документы.'),('Договоры и риски','Полномочия, отношения с партнёрами, платежи и условия выхода.'),('Международный найм','Для работодателей есть отдельное направление по иностранным работникам.')],
    prepare=['Описание продукта или услуги и клиентов','Гражданство и роль каждого участника','Источники средств, предполагаемые расчёты и регионы работы','Документы существующей компании, если проект уже действует'],
    example='Если иностранный учредитель одновременно планирует руководить компанией и жить в России, корпоративные полномочия и миграционный статус анализируются отдельно.',
    link=('/ru/for-business/','Для бизнеса: сопровождение международного найма')),
  'fr': dict(lead='Un projet d’entreprise avec une participation étrangère commence par la description de l’activité, des associés, de la direction et des flux financiers. La structure juridique, le séjour, la fiscalité et les autorisations sectorielles nécessitent des vérifications distinctes.',
    cards=[('Société et associés','Parts, direction, adresse et documents constitutifs.'),('Contrats et risques','Pouvoirs, partenaires, paiements et conditions de sortie.'),('Recrutement international','Un parcours spécifique concerne l’emploi de travailleurs étrangers.')],
    prepare=['Activité, produits et clients envisagés','Nationalité et rôle de chaque associé','Financement, paiements et régions d’activité','Documents de la société existante, le cas échéant'],
    example='Un associé étranger qui souhaite diriger la société et vivre en Russie doit examiner séparément ses pouvoirs sociaux et son statut migratoire.',
    link=('/fr/for-business/','Pour les entreprises : recrutement international')),
 },
 'investments': {
  'ru': dict(lead='Юридическая проверка инвестиционного проекта помогает понять, кто принимает обязательства, кому принадлежит актив, какие ограничения действуют и как устроен выход. Объём работы зависит от сделки; правовая проверка не является обещанием доходности.',
    cards=[('Стороны сделки','Регистрационные сведения и полномочия подписантов.'),('Активы и обязательства','Основания владения, ограничения, ключевые договоры и споры.'),('Условия сделки','Контроль, расчёты, ответственность, выход и разрешение споров.')],
    prepare=['Описание проекта и желаемого участия','Презентация, финансовая модель и проект договора','Сведения о продавце, партнёре и активе','Ваши условия отказа от сделки'],
    example='Покупка доли в одной компании не означает владение объектом, который находится у другой компании группы. Связь нужно подтвердить документами.',
    link=('/ru/knowledge/articles/investor-checklist/','Базовый список проверки проекта')),
  'fr': dict(lead='La vérification juridique d’un investissement porte sur les parties, la propriété des actifs, les obligations et les possibilités de sortie. Son périmètre dépend de la transaction ; elle ne garantit aucun rendement.',
    cards=[('Parties','Immatriculation et pouvoirs des signataires.'),('Actifs et obligations','Titres, restrictions, contrats et litiges.'),('Conditions','Contrôle, paiements, responsabilité et sortie.')],
    prepare=['Description du projet et de votre participation','Présentation, modèle financier et projet de contrat','Données sur le partenaire et l’actif','Critères qui vous conduiraient à refuser la transaction'],
    example='Acheter une part dans une société ne donne pas automatiquement accès à un immeuble détenu par une autre société du groupe.',
    link=('/fr/knowledge/articles/investor-checklist/','Liste de contrôle d’un projet')),
 },
 'legal': {
  'ru': dict(lead='Юридическая помощь начинается с постановки вопроса и анализа документов. Мы определяем применимые нормы, варианты действий, сроки, доказательства и риски. Объём представительства согласуется отдельно; результат спора или решения органа не может быть гарантирован.',
    cards=[('Документы','Изучение и подготовка договоров, заявлений и правовой позиции.'),('Споры','Анализ решения, доказательств, сроков и порядка защиты.'),('Консультация','Письменный или устный разбор вопроса в согласованном формате.')],
    prepare=['Краткая хронология событий','Документы и решения, связанные с вопросом','Сроки, которые уже известны, и ожидаемые действия другой стороны','Какой результат вы считаете полезным'],
    example='Если вы получили отказ органа, сохраните полный текст решения и подтверждение даты получения. Формулировка отказа определяет дальнейшую проверку.',
    link=('/ru/consultations/','Задать вопрос юристу')),
  'fr': dict(lead='L’assistance juridique commence par une question précise et les documents disponibles. Nous examinons les règles, les options, les délais, les preuves et les risques. Le mandat de représentation est convenu séparément ; l’issue d’un litige ne peut pas être garantie.',
    cards=[('Documents','Analyse et préparation de contrats, demandes et arguments.'),('Litiges','Décisions, preuves, délais et voies de recours.'),('Consultation','Analyse orale ou écrite selon le format convenu.')],
    prepare=['Chronologie concise des faits','Documents et décisions utiles','Échéances connues et actions attendues des autres parties','Résultat recherché'],
    example='Après un refus administratif, conservez la décision complète et la preuve de sa réception. Le motif exact guide la suite de l’analyse.',
    link=('/fr/consultations/','Poser une question juridique')),
 },
 'relocation': {
  'ru': dict(lead='Переезд складывается из юридических и бытовых задач. Мы помогаем выстроить последовательность: статус и документы, жильё, прибытие, семейные вопросы и первые практические шаги. Конкретные услуги и участие профильных специалистов согласуются по задаче.',
    cards=[('До поездки','Карта документов, контрольных дат и вопросов к консульству.'),('Прибытие','План жилья, адресов, связи и действий после въезда.'),('Семья','Отдельные потребности супругов и детей, единый календарь переезда.')],
    prepare=['Состав семьи и гражданство каждого','Желаемый регион и даты переезда','Имеющиеся визы, разрешения и договоры','Вопросы о жилье, учёбе и повседневной адаптации'],
    example='Если семья переезжает поэтапно, план должен показывать, кто приезжает первым, какие документы нужны каждому и кто отвечает за жильё и первые действия.',
    link=('/ru/knowledge/articles/how-to-choose-residence/','Начните с выбора правового маршрута')),
  'fr': dict(lead='Une installation comprend des tâches juridiques et pratiques. Nous organisons l’ordre des questions : statut, documents, logement, arrivée et besoins familiaux. Les services concrets et l’intervention de spécialistes sont convenus pour chaque projet.',
    cards=[('Avant le départ','Documents, échéances et questions consulaires.'),('Arrivée','Logement, adresses et premières démarches.'),('Famille','Besoins individuels et calendrier commun.')],
    prepare=['Composition et nationalité de la famille','Région et dates souhaitées','Visas, permis et contrats existants','Questions de logement, d’études et d’adaptation'],
    example='Pour une famille qui arrive en plusieurs étapes, le plan doit indiquer les documents de chacun et les responsabilités liées au logement.',
    link=('/fr/knowledge/articles/how-to-choose-residence/','Commencer par la voie de séjour')),
 },
}


def rich_section(lang, slug):
    d=CONTENT[slug][lang]
    is_ru=lang=='ru'
    parts=['<section class="sr-sec"><div class="sr-width"><div class="sr-section-head"><h2>'+('С чего начинается работа' if is_ru else 'Comment commencer')+'</h2><p>'+escape(d['lead'])+'</p></div><div class="sr-grid">']
    for title,description in d['cards']:
        parts.append('<div class="sr-card"><h3>'+escape(title)+'</h3><p>'+escape(description)+'</p></div>')
    parts.append('</div></div></section><section class="sr-sec alt"><div class="sr-width sr-b2b-copy"><h2>'+('Что подготовить к первому разговору' if is_ru else 'Préparer le premier échange')+'</h2><ul>')
    parts.extend('<li>'+escape(item)+'</li>' for item in d['prepare'])
    parts.append('</ul><h2>'+('Пример' if is_ru else 'Exemple')+'</h2><p>'+escape(d['example'])+'</p><p><a class="sr-link" href="'+d['link'][0]+'">'+escape(d['link'][1])+' →</a></p></div></section>')
    return ''.join(parts)
