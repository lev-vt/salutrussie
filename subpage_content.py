"""Specific service-detail guidance without invented eligibility or outcomes."""
from html import escape

DETAILS = {
 'rent': {
  'ru': ('Поможем разобрать документы и условия аренды до оплаты. Отдельно проверим, какие действия потребуются для законного проживания иностранного жильца.', ['Личность и полномочия подписанта, точный адрес и состав жильцов','Размер каждого платежа, условия возврата обеспечения и подтверждение оплаты','Акт передачи, состояние квартиры и обязанности сторон по документам'], 'Если договор подписывает представитель, попросите документ о полномочиях и проверьте, кому именно переводятся деньги.'),
  'fr': ('Nous examinons le bail et les documents avant tout versement. Les démarches nécessaires au séjour du locataire étranger sont vérifiées séparément.', ['Identité et pouvoirs du signataire, adresse et occupants','Paiements, dépôt, remboursement et preuves de versement','État des lieux et responsabilités documentaires'], 'Si un mandataire signe, vérifiez ses pouvoirs et l’identité du bénéficiaire des paiements.'),
 },
 'buy': {
  'ru': ('При покупке важно установить не только цену, но и право продавца, ограничения объекта, порядок расчётов и последствия условий договора.', ['Сведения об объекте и основании права продавца','Обременения, согласия и ограничения, значимые для сделки','Проект договора, этапы передачи денег и регистрации прав'], 'Если в рекламе указана одна площадь, а в документах другая, зафиксируйте расхождение до задатка.'),
  'fr': ('Avant un achat, il faut vérifier le droit du vendeur, les restrictions relatives au bien, les paiements et les clauses contractuelles.', ['Bien et titre du vendeur','Charges, consentements et restrictions utiles','Contrat, paiements et enregistrement des droits'], 'Si la surface annoncée diffère des documents, clarifiez l’écart avant tout acompte.'),
 },
 'legal-check': {
  'ru': ('Состав проверки зависит от объекта и сделки. Мы сопоставляем документы, сведения реестров и проект договора, затем обозначаем вопросы, которые нужно разрешить до подписания.', ['Определить объект, стороны и цель приобретения или аренды','Запросить доступные документы и актуальные сведения официальных реестров','Составить перечень расхождений, ограничений и условий для сделки'], 'Отсутствие очевидной записи об обременении не заменяет проверку всех договоров и фактических обстоятельств.'),
  'fr': ('Le contrôle dépend du bien et de la transaction. Nous comparons les pièces, les registres et le contrat avant de signaler les points à résoudre.', ['Identifier le bien, les parties et le projet','Obtenir les documents et données officielles disponibles','Lister les incohérences, restrictions et clauses à négocier'], 'L’absence de charge apparente dans un registre ne remplace pas l’examen des autres documents.'),
 },
 'company-registration': {
  'ru': ('Регистрация компании — часть более широкого проекта. До подачи нужно определить участников, руководство, вид деятельности, адрес и связанные миграционные и налоговые вопросы.', ['Описать деятельность, клиентов, участников и структуру управления','Проверить документы иностранных участников и полномочия подписантов','Согласовать уставные решения, адрес и последовательность регистрации'], 'Если будущий директор — иностранный гражданин, корпоративную роль и право работать в России рассматривают отдельно.'),
  'fr': ('L’immatriculation n’est qu’une étape. Il faut d’abord clarifier associés, direction, activité, adresse, séjour et fiscalité.', ['Décrire activité, clients, associés et gestion','Vérifier pièces des associés étrangers et pouvoirs','Définir statuts, adresse et ordre des formalités'], 'Si le futur directeur est étranger, sa fonction et son droit de travailler en Russie sont examinés séparément.'),
 },
 'legal-support': {
  'ru': ('Юридическое сопровождение бизнеса строится вокруг конкретных решений: договоров, полномочий, отношений участников и изменений деятельности.', ['Собрать действующие документы компании и ключевые договоры','Выделить решения, которые нужно принять, и сроки','Согласовать приоритетные правовые документы и порядок внедрения'], 'Если партнёры меняют доли, важно проверить корпоративные процедуры и договорённости, а не только текст соглашения.'),
  'fr': ('Le conseil juridique d’entreprise porte sur les contrats, pouvoirs, relations entre associés et changements d’activité.', ['Réunir les documents sociaux et contrats importants','Identifier décisions et échéances','Définir les pièces prioritaires et leur mise en œuvre'], 'Un changement de parts nécessite l’examen des procédures sociales et des accords entre associés.'),
 },
 'legal-due-diligence': {
  'ru': ('Юридическая проверка проекта показывает, какие сведения подтверждены, какие документы отсутствуют и какие условия сделки требуют изменения.', ['Проверить контрагента и полномочия подписанта','Сопоставить заявленные активы с документами о правах и ограничениях','Проанализировать обязательства, споры, расчёты и возможность выхода'], 'Если актив принадлежит другой компании группы, нужно объяснить, какие права реально получает инвестор.'),
  'fr': ('L’audit identifie les faits prouvés, les pièces manquantes et les clauses qui doivent être revues.', ['Vérifier partenaire et signataire','Comparer actifs annoncés, titres et restrictions','Examiner obligations, litiges, paiements et sortie'], 'Si l’actif est détenu par une autre société du groupe, définissez les droits réellement acquis.'),
 },
 'project-support': {
  'ru': ('На этапе проекта важно согласовать юридические контрольные точки до перевода средств и начала исполнения.', ['Зафиксировать стороны, активы, права и обязанности','Разделить подготовку, подписание, оплату и передачу по этапам','Определить контроль, отчётность, изменения и выход из проекта'], 'При поэтапном финансировании условия каждого транша должны быть связаны с проверяемым событием.'),
  'fr': ('Un projet d’investissement doit prévoir des étapes juridiques vérifiables avant les paiements et l’exécution.', ['Définir parties, actifs, droits et obligations','Séparer préparation, signature, paiement et transfert','Prévoir contrôle, rapports, modifications et sortie'], 'Pour un financement par tranches, liez chaque versement à une étape vérifiable.'),
 },
 'document-preparation': {
  'ru': ('Хороший документ решает конкретную задачу и согласован с фактами. Мы сначала выясняем цель, стороны и риски, затем готовим или проверяем текст.', ['Предоставить черновик, переписку и краткую хронологию','Определить обязательные факты, полномочия и сроки','Согласовать формулировки, приложения и порядок подписания'], 'Если договор используется в нескольких языках, нужно заранее определить, как стороны будут разрешать расхождения версий.'),
  'fr': ('Un bon document répond à un objectif précis et correspond aux faits. Nous définissons d’abord les parties et les risques.', ['Fournir projet, échanges et chronologie','Identifier faits, pouvoirs et échéances','Valider clauses, annexes et signature'], 'Pour un contrat bilingue, prévoyez comment résoudre une divergence entre les versions.'),
 },
 'disputes': {
  'ru': ('Спор начинается с документа, который вы оспариваете, даты его получения и имеющихся доказательств. Так можно оценить варианты защиты и сроки.', ['Сохранить решение или претензию целиком и доказательство получения','Составить хронологию событий и перечень доказательств','Проверить применимый порядок обращения и процессуальные риски'], 'При отказе органа не подавайте повторно тот же комплект, пока не разобрали конкретное основание отказа.'),
  'fr': ('Pour un litige, il faut connaître le document contesté, sa date de réception et les preuves disponibles.', ['Conserver décision ou réclamation et preuve de réception','Établir chronologie et inventaire des preuves','Vérifier recours, délais et risques procéduraux'], 'Après un refus administratif, analysez le motif avant de déposer le même dossier à nouveau.'),
 },
 'rvp': {
  'ru': ('РВП оформляется по применимому основанию и процедуре. Мы проверяем, какие факты и документы подтверждают маршрут, а какие требуют дополнительной работы.', ['Гражданство, основание въезда и текущий статус','Основание для РВП и возможные исключения из квоты','Документы, переводы, прежние решения и регион обращения'], 'Если основание зависит от семейных обстоятельств, проверьте документы каждого участника до планирования даты подачи.'),
  'fr': ('Le RVP dépend d’un fondement et d’une procédure applicables. Nous vérifions les faits et les documents avant le dépôt.', ['Nationalité, entrée et statut actuel','Fondement du RVP et exceptions éventuelles au quota','Pièces, traductions, décisions antérieures et région'], 'Si le fondement repose sur la famille, vérifiez les pièces de chaque personne avant de planifier le dépôt.'),
 },
 'vnzh': {
  'ru': ('Для ВНЖ нужно определить доступное основание, текущий статус и последовательность действий. Наличие одного документа ещё не означает готовность всего пакета.', ['История пребывания и действующие разрешения','Возможное основание для ВНЖ и подтверждающие сведения','Документы семьи, адрес, переводы и прежние решения'], 'Если один из документов скоро истекает, сначала уточните влияние этого срока на маршрут.'),
  'fr': ('Le VNZh exige l’analyse du fondement, du statut actuel et des étapes. Une pièce isolée ne suffit pas à valider le dossier.', ['Historique du séjour et permis en vigueur','Fondement envisagé et preuves','Famille, adresse, traductions et décisions antérieures'], 'Si une pièce expire bientôt, vérifiez l’effet de cette échéance avant de choisir le calendrier.'),
 },
 'citizenship': {
  'ru': ('Вопрос гражданства требует проверки основания, состава семьи, действующего статуса и истории документов. Порядок зависит от индивидуальных обстоятельств.', ['Текущий статус и гражданство заявителя','Семейные, исторические или иные обстоятельства, на которые вы ссылаетесь','Ранее выданные документы и решения по заявлениям'], 'Если документы о рождении, имени или браке содержат разные написания, устраните расхождения до окончательного пакета.'),
  'fr': ('La nationalité russe suppose un fondement précis, l’examen de la famille, du statut et de l’historique documentaire.', ['Statut actuel et nationalité','Circonstances familiales ou autres invoquées','Pièces et décisions antérieures'], 'Des orthographes différentes du nom dans les actes doivent être expliquées avant le dépôt.'),
 },
 'visas': {
  'ru': ('Визовый маршрут определяется целью поездки, гражданством и обстоятельствами подачи. Мы сверяем назначение визы с планируемыми действиями в России.', ['Цель, даты поездки и место подачи','Гражданство, паспорт и история въездов','Приглашение или иной документ, если он требуется для выбранной категории'], 'Если человек собирается работать, нельзя автоматически считать подходящей визу, выбранную для частной поездки.'),
  'fr': ('La voie du visa dépend du motif du voyage, de la nationalité et du lieu de dépôt. La catégorie choisie doit correspondre au projet réel.', ['Motif, dates et poste de dépôt','Nationalité, passeport et séjours précédents','Invitation ou autre pièce requise pour la catégorie retenue'], 'Un projet de travail ne doit pas être assimilé automatiquement à une visite privée.'),
 },
 'students': {
  'ru': ('Студенту важно сопоставить учебную программу, документ о зачислении, основание въезда и сроки миграционных документов.', ['Учебная организация, программа и документы о зачислении','Гражданство, виза или иной текущий статус','Изменения обучения, адреса и даты окончания документов'], 'При переводе в другое учебное заведение проверьте последствия для статуса до оформления перевода.'),
  'fr': ('Pour un étudiant, il faut rapprocher la formation, l’admission, la voie d’entrée et les échéances du séjour.', ['Établissement, programme et admission','Nationalité, visa ou autre statut','Changement d’études ou d’adresse et échéances'], 'Avant de changer d’établissement, vérifiez l’effet sur le statut migratoire.'),
 },
 'family': {
  'ru': ('Семейный переезд удобнее планировать как общий проект с отдельной правовой карточкой каждого человека.', ['Гражданство, родство и нынешний статус каждого','Порядок въезда и сроки документов','Документы о браке, рождении, смене имени и составе семьи'], 'Если один член семьи уже в России, его маршрут может отличаться от маршрута тех, кто ещё за рубежом.'),
  'fr': ('Une installation familiale demande un calendrier commun et une fiche juridique pour chaque personne.', ['Nationalité, lien familial et statut actuel de chacun','Ordre d’arrivée et échéances','Actes de mariage, naissance, changement de nom et composition familiale'], 'Le parcours d’une personne déjà en Russie peut différer de celui des proches encore à l’étranger.'),
 },
 'migration-disputes': {
  'ru': ('При отказе или другом миграционном споре нужно изучить точный текст решения, факты дела и сроки защиты до повторной подачи.', ['Полное решение, дата вручения и подтверждение получения','Копия поданного пакета, переписка и доказательства','Конкретное основание отказа и возможные способы его проверки'], 'Если отказ связан с расхождением сведений, сначала установите источник расхождения и документы, которые его объясняют.'),
  'fr': ('Après un refus migratoire, examinez la décision complète, les faits et les délais avant un nouveau dépôt.', ['Décision, date et preuve de notification','Copie du dossier, échanges et preuves','Motif précis du refus et moyens de le vérifier'], 'Pour des données contradictoires, identifiez leur origine et les pièces explicatives avant d’agir.'),
 },
}


def detail_rich(lang, slug):
    _, checks, example = DETAILS[slug][lang]
    ru=lang=='ru'
    title='Что проверяем' if ru else 'Points à vérifier'
    example_title='Пример для подготовки' if ru else 'Exemple pratique'
    ending=('Результат и сроки зависят от фактов и решений уполномоченных лиц. Объём и стоимость нашей работы согласуем заранее.' if ru else 'Le résultat et les délais dépendent des faits et des décisions des autorités. Le mandat et les honoraires sont convenus à l’avance.')
    return '<section class="sr-sec"><div class="sr-width sr-b2b-copy"><h2>'+title+'</h2><ul>'+''.join('<li>'+escape(item)+'</li>' for item in checks)+'</ul><h2>'+example_title+'</h2><p>'+escape(example)+'</p><p class="sr-note">'+ending+'</p></div></section>'
