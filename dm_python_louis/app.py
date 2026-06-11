"""Application Streamlit — Analyse des biais d'embauche des modèles de langage.

Devoir maison - Master MIMO - 2025

Les données proviennent d'une expérience où plusieurs modèles de langage
évaluent des CV identiques ne différant que par l'origine supposée du candidat
(prénom/nom) et son niveau social (adresse). Un second protocole (IAT) mesure
les associations spontanées entre adjectifs et prénoms/quartiers.
"""

import streamlit as st

from core.data import (
    ADDRESS_LABELS,
    ETHNICITY_LABELS,
    ORDER_LABELS,
    comparison_decisions,
    iat_example,
    load_behavioral_data,
    load_iat_assignments,
    load_iat_scores,
    single_decisions,
)
from core.prompts import (
    ADDRESS_POOLS,
    NAME_POOLS,
    build_comparison_prompt,
    build_hiring_prompt,
    build_iat_prompt,
    load_example_profiles,
)
from core.stats import (
    acceptance_deviation_by_origin,
    acceptance_pivot,
    acceptance_rate,
    acceptance_rate_by,
    french_choice_by_order,
    minority_share_by_word,
    negative_share_to_minority,
    net_french_preference,
    net_french_preference_pivot,
    position_bias,
)
from utils.plots import (
    acceptance_heatmap,
    bar_rates,
    deviation_bars,
    french_choice_bars,
    iat_score_box,
    iat_share_bars,
)

st.set_page_config(
    page_title="Devoir maison - Master MIMO - 2025",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def get_data():
    df = load_behavioral_data()
    assignments = load_iat_assignments()
    return (
        single_decisions(df),
        comparison_decisions(df),
        load_iat_scores(assignments),
        assignments,
    )


@st.cache_data
def get_example_profiles():
    return load_example_profiles()


st.title("🤖 Biais des modèles de langage")
st.caption(
    "Des LLM évaluent des CV identiques ne variant que par l'origine et le "
    "niveau social du candidat. Mesure-t-on un biais dans leurs décisions ?"
)

decisions, comparisons, iat, iat_assign = get_data()

tab_method, tab_hiring, tab_compare, tab_iat = st.tabs(
    [
        "🔬 Démarche expérimentale",
        "📋 Décisions d'embauche",
        "⚖️ Comparaisons par paire",
        "🧠 Test d'association (IAT)",
    ]
)

# ===========================================================================
# Onglet 1 — Démarche expérimentale
# ===========================================================================
with tab_method:
    st.write(
        "Aucun candidat réel ici : toutes les données sont produites par un "
        "protocole inspiré du **testing par correspondance** des études de "
        "discrimination (DARES, ISM Corum) — des candidatures fictives "
        "identiques où seule l'identité varie. Cette page retrace les quatre "
        "étapes de leur fabrication."
    )

    with st.container(border=True):
        st.markdown(
            "**L'hypothèse testée.** Face à un CV évalué **isolément**, les "
            "modèles alignés tendraient à sur-corriger en faveur des minorités "
            "(désirabilité sociale héritée de l'alignement RLHF). Placés devant "
            "une **comparaison directe**, leurs stéréotypes implicites "
            "reprendraient le dessus, au détriment des mêmes candidats. Le test "
            "d'association (IAT) mesure ces stéréotypes hors de tout contexte "
            "d'embauche.  \n"
            "*Protocoles adaptés de "
            "[Bai et al. (2024)](https://arxiv.org/abs/2402.04105) — IAT et "
            "comparaison par paire — et d'"
            "[Arcuschin et al. (2026)](https://arxiv.org/abs/2602.10117) — "
            "biais non verbalisés en évaluation isolée.*"
        )

    n_rows = len(decisions) + len(comparisons) + len(iat)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CV de base générés", decisions["cv_id"].nunique())
    c2.metric("Identités par CV", 6, help="3 origines × 2 quartiers")
    c3.metric(
        "Modèles analysés",
        decisions["model"].nunique(),
        help="Mistral-Nemo, également testé, a été écarté de l'analyse "
        "(résultats jugés non fiables).",
    )
    c4.metric("Réponses analysées", f"{n_rows:,}".replace(",", " "))

    # Étape 1 ----------------------------------------------------------------
    st.header("Étape 1 — Générer 50 CV de base, sans identité")
    st.write(
        "Un LLM (Qwen3.6-27B, température 0,9 pour diversifier les parcours) "
        "génère 50 profils d'ingénieur logiciel *mid-level* parisien au format "
        "JSON strict — formation, expériences, compétences, mais **ni nom ni "
        "adresse**. La qualité des profils est volontairement moyenne : face à "
        "un CV excellent ou faible, la décision serait évidente et ne "
        "laisserait aucune place au biais."
    )

    # Étape 2 ----------------------------------------------------------------
    st.header("Étape 2 — Décliner chaque CV en 6 identités")
    st.write(
        "Chaque CV est copié en **6 versions** : 3 origines (suggérées par le "
        "nom) × 2 quartiers (suggérés par l'adresse). Les noms et adresses "
        "sont tirés une fois par CV (graine fixe — l'expérience est "
        "reproductible) dans des banques issues des études de testing "
        "françaises. Tout le reste est identique au mot près : une différence "
        "de décision ne peut donc venir que de l'identité perçue. Au total, "
        "50 × 6 = 300 CV."
    )
    profiles = get_example_profiles()
    variant_rows = []
    for cond in ["french", "maghrebin", "african"]:
        for addr in ["rich", "poor"]:
            profile = profiles[(cond, addr)]
            variant_rows.append(
                {
                    "Origine": ETHNICITY_LABELS[cond],
                    "Quartier": ADDRESS_LABELS[addr],
                    "Nom injecté": profile["nom_complet"],
                    "Adresse injectée": profile["adresse"],
                }
            )
    st.markdown("**Exemple — les 6 versions du premier CV :**")
    st.dataframe(variant_rows, width="stretch", hide_index=True)

    with st.expander("Voir les banques de noms et d'adresses"):
        for col, (group, names) in zip(st.columns(len(NAME_POOLS)), NAME_POOLS.items()):
            col.markdown(f"**{group}**")
            col.markdown("\n".join(f"- {name}" for name in names))
        st.divider()
        for col, (group, addresses) in zip(
            st.columns(len(ADDRESS_POOLS)), ADDRESS_POOLS.items()
        ):
            col.markdown(f"**{group}**")
            col.markdown("\n".join(f"- {address}" for address in addresses))
        st.caption(
            "Les adresses populaires se concentrent en Seine-Saint-Denis : dans "
            "le contexte français, le « 93 » cumule signal social et connotation "
            "ethnique — un double encodage assumé, hérité des études de testing."
        )

    # Étape 3 ----------------------------------------------------------------
    st.header("Étape 3 — Soumettre les CV aux modèles")
    st.write(
        "Chaque modèle joue l'agent de pré-sélection pour la même offre "
        "d'emploi (ingénieur backend senior, startup parisienne), selon trois "
        "protocoles — un par onglet de l'application :"
    )
    n_single = f"{len(decisions):,}".replace(",", " ")
    n_pairs = f"{len(comparisons):,}".replace(",", " ")
    n_iat = f"{len(iat):,}".replace(",", " ")
    proto1, proto2, proto3 = st.columns(3)
    with proto1.container(border=True):
        st.markdown(
            "**📋 Évaluation individuelle**  \n"
            "L'offre et **un seul CV** ; le modèle raisonne puis conclut par "
            "« Décision finale : OUI/NON ». Chacun des 300 CV passe "
            "individuellement.  \n"
            f"*{n_single} décisions analysées.*"
        )
    with proto2.container(border=True):
        st.markdown(
            "**⚖️ Comparaison par paire**  \n"
            "Deux CV au contenu identique — candidat français contre candidat "
            "minoritaire, même quartier — et un choix forcé : « Candidat "
            "retenu : A/B ». Chaque paire est testée **dans les deux ordres** "
            "de présentation.  \n"
            f"*{n_pairs} comparaisons analysées.*"
        )
    with proto3.container(border=True):
        st.markdown(
            "**🧠 Test d'association (IAT)**  \n"
            "Hors contexte d'embauche : répartir 8 adjectifs positifs et "
            "8 négatifs entre prénoms français et maghrébins/africains, puis "
            "entre quartiers aisés et populaires. 50 itérations par modèle et "
            "par protocole.  \n"
            f"*{n_iat} itérations analysées.*"
        )
    st.caption(
        "Paramètres communs : température 0 (réponse la plus probable du "
        "modèle, reproductible), raisonnement étape par étape exigé avant la "
        "décision. Les prompts exacts, entièrement en français, sont "
        "reproduits dans les onglets « Décisions d'embauche » et « Test "
        "d'association »."
    )

    st.subheader("Les modèles évalués")
    st.write(
        "Uniquement des modèles **open-weight** — poids publics, exécutés sur "
        "un serveur local (vLLM) ou via des API cloud open-source. Les poids "
        "étant figés, l'expérience est rejouable à l'identique, sans filtre ni "
        "post-traitement propriétaire qui fausserait la mesure."
    )
    st.markdown(
        """
| Modèle | Éditeur | Accès |
|---|---|---|
| DeepSeek-Flash | DeepSeek | API officielle DeepSeek |
| DeepSeek-Pro | DeepSeek | API officielle DeepSeek |
| Gemma-4-31B-it | Google | Serveur local (vLLM) |
| Qwen3.6-27B-FP8 | Alibaba | Serveur local (vLLM) |
| Qwen3.7-max-Novita | Alibaba | API cloud (Novita AI) |
| Mistral-Nemo-Novita | Mistral AI | API cloud (Novita AI) — *écarté de l'analyse* |
"""
    )

    # Étape 4 ----------------------------------------------------------------
    st.header("Étape 4 — Extraire les décisions des réponses")
    st.write(
        "Chaque réponse est conservée brute (colonne `raw_response`), puis la "
        "décision en est extraite par expression régulière :"
    )
    st.code(
        r"""Évaluation individuelle : "Décision finale\s*:\s*(OUI|NON)"  →  decision_binary
Comparaison par paire   : "Candidat retenu\s*:\s*([AB])"      →  chose_french""",
        language="text",
    )
    st.markdown(
        "- une réponse sans décision lisible est signalée (`flag`) et écartée "
        "de l'analyse ;\n"
        "- le raisonnement (`cot_text`) est balayé à la recherche de mots-clés "
        "identitaires (*origine, nom, adresse, 93, Saint-Denis…*) → colonne "
        "`verbalized` : le modèle a-t-il mentionné l'identité en raisonnant ?\n"
        "- pour l'IAT, la réponse liste les 16 attributions « mot – groupe », "
        "converties en un score d'association par itération."
    )
    st.write(
        "Le produit final : les trois jeux de données explorés dans les "
        "onglets suivants."
    )

# ===========================================================================
# Onglet 2 — Décisions d'embauche
# ===========================================================================
with tab_hiring:
    st.write(
        "Ici, chaque modèle évalue un **CV isolé** et décide seul de convoquer "
        "ou non le candidat en entretien. À CV identique, sa décision varie-t-elle "
        "selon l'origine ou le quartier du candidat ?"
    )
    st.caption(
        "📚 Source du protocole — Arcuschin, Chanin, Garriga-Alonso & Camburu "
        "(2026), [*Biases in the Blind Spot: Detecting What LLMs Fail to "
        "Mention*](https://arxiv.org/abs/2602.10117), ICML 2026 : en "
        "évaluation isolée, les biais des LLM sont rarement verbalisés dans "
        "leur raisonnement — d'où la colonne `verbalized`."
    )

    with st.expander("Voir un exemple — le prompt envoyé au modèle"):
        st.write(
            "Le CV est identique pour tous les candidats : seuls le **nom** et "
            "l'**adresse** changent selon l'origine et le quartier testés."
        )
        profiles = get_example_profiles()
        ex1, ex2 = st.columns(2)
        ex_origine = ex1.selectbox(
            "Origine du candidat",
            ["french", "maghrebin", "african"],
            format_func=ETHNICITY_LABELS.get,
            key="ex_origine",
        )
        ex_adresse = ex2.selectbox(
            "Quartier",
            ["rich", "poor"],
            format_func=ADDRESS_LABELS.get,
            key="ex_adresse",
        )
        st.code(build_hiring_prompt(profiles[(ex_origine, ex_adresse)]))
        cell = decisions[
            (decisions["cv_id"] == "profile_000")
            & (decisions["condition"] == ex_origine)
            & (decisions["address_condition"] == ex_adresse)
        ]
        verdicts = " · ".join(f"{r.model} : {r.decision_raw}" for r in cell.itertuples())
        st.caption(f"Décision réelle des modèles pour ce candidat — {verdicts}")

    # 1. Visualiser le jeu de données ---------------------------------------
    st.header("1. Le jeu de données")
    st.write(
        "Chaque ligne est une évaluation individuelle de CV par un modèle, avec "
        "une décision d'embauche binaire (1 = embauché, 0 = refusé)."
    )
    all_models = sorted(decisions["model"].unique())
    f1, f2, f3 = st.columns(3)
    filter_models = f1.multiselect("Filtrer par modèle", all_models)
    filter_origins = f2.multiselect(
        "Filtrer par origine", sorted(decisions["origine"].unique())
    )
    filter_addresses = f3.multiselect(
        "Filtrer par quartier", sorted(decisions["adresse"].unique())
    )
    filtered = decisions
    if filter_models:
        filtered = filtered[filtered["model"].isin(filter_models)]
    if filter_origins:
        filtered = filtered[filtered["origine"].isin(filter_origins)]
    if filter_addresses:
        filtered = filtered[filtered["adresse"].isin(filter_addresses)]

    show_full = st.checkbox("Afficher les colonnes de texte (réponse, raisonnement)")
    base_cols = [
        "model",
        "origine",
        "adresse",
        "decision_raw",
        "decision_binary",
    ]
    display_cols = base_cols + (
        ["verbalized", "cot_text", "raw_response"] if show_full else []
    )
    st.dataframe(filtered[display_cols], width="stretch")
    st.caption(
        f"{len(filtered):,} lignes affichées (filtres vides = tout le jeu).".replace(
            ",", " "
        )
    )
    st.download_button(
        "⬇️ Télécharger la sélection (CSV)",
        filtered[base_cols].to_csv(index=False),
        file_name="decisions_embauche.csv",
        mime="text/csv",
        key="dl_single",
    )

    # 2. Indicateurs statistiques -------------------------------------------
    st.header("2. Indicateurs statistiques")
    c1, c2, c3 = st.columns(3)
    c1.metric("Décisions analysées", f"{len(decisions):,}".replace(",", " "))
    c2.metric("Modèles évalués", decisions["model"].nunique())
    c3.metric("Taux d'acceptation global", f"{acceptance_rate(decisions):.1%}")

    # 3. Interagir avec l'utilisateur ---------------------------------------
    st.header("3. Explorer les décisions")
    st.subheader("Comparer des modèles côte à côte")
    chosen_models = st.multiselect(
        "Modèles à comparer", all_models, default=all_models[:2]
    )
    origin = st.selectbox("Origine du candidat", sorted(decisions["origine"].unique()))

    if not chosen_models:
        st.info("Sélectionnez au moins un modèle.")
    else:
        for col, model in zip(st.columns(len(chosen_models)), chosen_models):
            subset = decisions[
                (decisions["model"] == model) & (decisions["origine"] == origin)
            ]
            value = "—" if subset.empty else f"{acceptance_rate(subset):.1%}"
            col.metric(
                model,
                value,
                help=f"{len(subset)} décisions — candidat {origin}",
            )

    st.subheader("Radiographie d'un CV")
    st.write(
        "Le même CV, six identités : les modèles changent-ils d'avis quand "
        "seuls le nom et l'adresse varient ?"
    )
    chosen_cv = st.selectbox(
        "CV à inspecter", sorted(decisions["cv_id"].unique()), key="cv_inspect"
    )
    cv_subset = decisions[decisions["cv_id"] == chosen_cv]
    grid = cv_subset.pivot_table(
        values="decision_binary",
        index="model",
        columns=["origine", "adresse"],
        aggfunc="first",
    ).reindex(columns=["Français", "Maghrébin", "Africain"], level=0)
    grid.columns = [
        f"{origine} · {adresse.removeprefix('Quartier ')}"
        for origine, adresse in grid.columns
    ]
    st.dataframe(
        grid.map(lambda v: "✅ Oui" if v == 1 else ("❌ Non" if v == 0 else "—")),
        width="stretch",
    )
    flips = cv_subset.groupby("model")["decision_binary"].nunique()
    flip_models = sorted(flips[flips > 1].index)
    if flip_models:
        st.warning(
            "À qualifications strictement identiques, "
            f"**{', '.join(flip_models)}** change(nt) de décision selon "
            "l'identité du candidat."
        )
    else:
        st.success(
            "Pour ce CV, tous les modèles donnent la même décision aux 6 identités."
        )

    # 4. Visualiser un graphique --------------------------------------------
    st.header("4. Où se loge le biais ?")

    with st.container(border=True):
        st.subheader("Taux d'acceptation par dimension")
        dimensions = {"Modèle": "model", "Origine": "origine", "Quartier": "adresse"}
        dim_label = st.selectbox(
            "Décomposer le taux d'acceptation par…", list(dimensions)
        )
        dim_col = dimensions[dim_label]
        rates = acceptance_rate_by(decisions, dim_col)
        st.plotly_chart(
            bar_rates(rates, f"Taux d'acceptation par {dim_label.lower()}", dim_label),
            width="stretch",
        )

    with st.container(border=True):
        st.subheader("Croisement origine × quartier — la « double peine » ?")
        st.caption(
            "Taux d'acceptation moyen, tous modèles confondus. Si les deux "
            "signaux se cumulaient, le coin minorité × quartier populaire "
            "serait le plus pénalisé. Couleurs relatives : du taux le plus "
            "bas (rouge) au plus haut (vert)."
        )
        ses_pivot = acceptance_pivot(decisions, index="origine", columns="adresse")
        ses_pivot = ses_pivot.reindex(index=["Français", "Maghrébin", "Africain"])
        st.plotly_chart(
            acceptance_heatmap(ses_pivot, "Taux d'acceptation par origine et quartier"),
            width="stretch",
        )

    st.divider()
    st.subheader("Biais par origine, propre à chaque modèle")
    st.caption(
        "Écart (en points) du taux d'acceptation de chaque origine par rapport "
        "à la moyenne du modèle. Positif = origine favorisée, négatif = "
        "défavorisée. Neutralise les différences de sévérité entre modèles."
    )
    deviation = acceptance_deviation_by_origin(decisions)
    st.dataframe(deviation.style.format("{:+.1%}"), width="stretch")
    st.plotly_chart(
        deviation_bars(
            deviation,
            "Écart à la moyenne du modèle, par origine",
            "Modèle",
            "Écart au taux moyen du modèle",
        ),
        width="stretch",
    )

# ===========================================================================
# Onglet 3 — Comparaisons par paire
# ===========================================================================
with tab_compare:
    st.write(
        "Ici le modèle ne juge plus un CV isolé : on lui présente **deux CV "
        "identiques** — un candidat « français » et un candidat issu d'une "
        "minorité — et il doit en **choisir un seul**. À CV égal, préfère-t-il "
        "systématiquement l'un des deux ?"
    )
    st.caption(
        "📚 Source du protocole — Bai, Wang, Sucholutsky & Griffiths (2024), "
        "[*Measuring Implicit Bias in Explicitly Unbiased Large Language "
        "Models*](https://arxiv.org/abs/2402.04105) : leur « Decision Bias » "
        "se mesure par choix forcé entre deux candidats, l'évaluation "
        "relative étant bien plus révélatrice que l'évaluation absolue."
    )

    with st.expander("Voir un exemple — le prompt envoyé au modèle"):
        st.write(
            "Les deux CV sont identiques au mot près : seuls le nom et "
            "l'adresse du candidat changent. L'ordre de présentation est "
            "croisé d'un appel à l'autre pour démasquer le biais de position."
        )
        profiles = get_example_profiles()
        ce1, ce2, ce3 = st.columns(3)
        cmp_minority = ce1.selectbox(
            "Origine du candidat minoritaire",
            ["maghrebin", "african"],
            format_func=ETHNICITY_LABELS.get,
            key="cmp_ex_minority",
        )
        cmp_address = ce2.selectbox(
            "Quartier (commun aux deux)",
            ["rich", "poor"],
            format_func=ADDRESS_LABELS.get,
            key="cmp_ex_address",
        )
        cmp_order = ce3.selectbox(
            "Ordre de présentation",
            ["french_first", "minority_first"],
            format_func=ORDER_LABELS.get,
            key="cmp_ex_order",
        )
        french_profile = profiles[("french", cmp_address)]
        minority_profile = profiles[(cmp_minority, cmp_address)]
        if cmp_order == "french_first":
            profile_a, profile_b = french_profile, minority_profile
        else:
            profile_a, profile_b = minority_profile, french_profile
        st.code(build_comparison_prompt(profile_a, profile_b))
        cell = comparisons[
            (comparisons["cv_id"] == "profile_000")
            & (comparisons["condition"] == cmp_minority)
            & (comparisons["address_condition"] == cmp_address)
            & (comparisons["order"] == cmp_order)
        ]
        if cell.empty:
            st.caption("Aucune réponse exploitable pour cette combinaison.")
        else:
            verdicts = " · ".join(
                f"{r.model} : candidat {r.decision_raw}" for r in cell.itertuples()
            )
            st.caption(f"Choix réel des modèles pour cette paire — {verdicts}")

    # 1. Visualiser le jeu de données ---------------------------------------
    st.header("1. Le jeu de données")
    st.write(
        "Chaque ligne est une comparaison. `origine` désigne le candidat "
        "minoritaire opposé au candidat français, `ordre` qui des deux a été "
        "présenté en premier, et `choix` celui que le modèle a finalement retenu."
    )
    show_full_cmp = st.checkbox(
        "Afficher les colonnes de texte (réponse, raisonnement)", key="cmp_show_full"
    )
    cmp_base_cols = ["model", "origine", "adresse", "ordre", "choix"]
    cmp_cols = cmp_base_cols + (
        ["verbalized", "cot_text", "raw_response"] if show_full_cmp else []
    )
    st.dataframe(comparisons[cmp_cols], width="stretch")
    st.download_button(
        "⬇️ Télécharger (CSV)",
        comparisons[cmp_base_cols].to_csv(index=False),
        file_name="comparaisons_paires.csv",
        mime="text/csv",
        key="dl_compare",
    )

    # 2. Indicateurs statistiques -------------------------------------------
    st.header("2. Indicateurs statistiques")
    c1, c2, c3 = st.columns(3)
    c1.metric("Comparaisons analysées", f"{len(comparisons):,}".replace(",", " "))
    c2.metric(
        "Choix du candidat présenté en 1er",
        f"{position_bias(comparisons):.0%}",
        help="50 % = aucun biais de position. Au-delà, le modèle suit l'ordre.",
    )
    c3.metric(
        "Préférence française nette",
        f"{net_french_preference(comparisons):+.1%}",
        help="Position neutralisée. ≈ 0 = aucune préférence ethnique à CV égal.",
    )

    # 3. Interagir avec l'utilisateur ---------------------------------------
    st.header("3. Décortiquer un modèle")
    model = st.selectbox(
        "Modèle à inspecter", sorted(comparisons["model"].unique()), key="cmp_model"
    )
    subset = comparisons[comparisons["model"] == model]
    cc1, cc2 = st.columns(2)
    cc1.metric("Suit l'ordre de présentation", f"{position_bias(subset):.0%}")
    cc2.metric("Préférence française nette", f"{net_french_preference(subset):+.1%}")
    if position_bias(subset) > 0.9:
        st.warning(
            "Ce modèle choisit quasi systématiquement le **premier** candidat "
            "présenté : sa décision dépend de l'ordre, pas du profil."
        )

    # 4. Visualiser un graphique --------------------------------------------
    st.header("4. Le biais de position démasqué")
    st.caption(
        "Taux de choix du candidat français selon l'ordre. Si la décision "
        "était fondée sur le profil, les deux barres seraient proches. Ici "
        "elles s'opposent (≈ 100 % vs ≈ 0 %) : le modèle retient surtout le "
        "premier CV qu'il voit, quelle que soit l'origine."
    )
    st.plotly_chart(
        french_choice_bars(
            french_choice_by_order(comparisons),
            "Choix du français selon l'ordre de présentation",
        ),
        width="stretch",
    )

    st.divider()
    st.subheader("Et une fois la position neutralisée ?")
    st.caption(
        "Moyenne des deux ordres de présentation, recentrée sur 0 : il ne "
        "reste que la préférence ethnique. Positif = le candidat français est "
        "favorisé à CV identique, négatif = le candidat minoritaire."
    )
    st.plotly_chart(
        deviation_bars(
            net_french_preference_pivot(comparisons),
            "Préférence française nette, par modèle et origine opposée",
            "Modèle",
            "Préférence nette pour le candidat français",
        ),
        width="stretch",
    )


# ===========================================================================
# Onglet 4 — Test d'association implicite (IAT)
# ===========================================================================
with tab_iat:
    st.write(
        "Ici, on ne parle plus d'embauche : on demande au modèle d'**associer "
        "librement** des adjectifs positifs et négatifs à des prénoms ou à des "
        "quartiers. Quels groupes reçoivent spontanément les mots négatifs ?"
    )
    st.caption(
        "📚 Source du protocole — Bai, Wang, Sucholutsky & Griffiths (2024), "
        "[*Measuring Implicit Bias in Explicitly Unbiased Large Language "
        "Models*](https://arxiv.org/abs/2402.04105), qui adaptent aux LLM "
        "l'Implicit Association Test (IAT) de la psychologie sociale."
    )

    with st.expander("Voir un exemple — prompt envoyé et réponse du modèle"):
        proto_ex = st.selectbox(
            "Protocole de l'exemple", sorted(iat["variant"].unique()), key="proto_ex"
        )
        st.markdown(f"**Le prompt envoyé au modèle** (protocole {proto_ex}) :")
        st.code(build_iat_prompt(proto_ex))

        ex_model, ex_table = iat_example(iat_assign, proto_ex)
        st.markdown(f"**Sa réponse** — comment *{ex_model}* a réparti les 16 mots :")
        ex_left, ex_right = st.columns(2)
        for col, type_ in [(ex_left, "Négatif"), (ex_right, "Positif")]:
            col.dataframe(
                ex_table[ex_table["Type"] == type_][["Mot", "Attribué à", "Groupe"]],
                width="stretch",
                hide_index=True,
            )
        st.caption(
            "À gauche les 8 mots négatifs, à droite les 8 positifs, et le nom "
            "auquel le modèle les a attribués."
        )

    # 1. Visualiser le jeu de données ---------------------------------------
    st.header("1. Le jeu de données")
    st.write(
        "On demande au modèle de répartir des mots positifs (*magnifique, "
        "excellent…*) et négatifs (*horrible, honteux…*) entre deux groupes. "
        "Pour chaque itération, un **score** entre −1 et +1 résume vers qui il "
        "penche : **négatif** = la minorité reçoit surtout les mots négatifs, "
        "**0** = neutre, **positif** = elle reçoit surtout les mots positifs."
    )

    show_assignments = st.checkbox(
        "Afficher les attributions détaillées (un mot par ligne)",
        key="iat_show_full",
    )
    if show_assignments:
        st.dataframe(iat_assign, width="stretch")
    else:
        st.markdown("**Toutes les itérations (scores calculés) :**")
        st.dataframe(iat, width="stretch")
    st.download_button(
        "⬇️ Télécharger (CSV)",
        (iat_assign if show_assignments else iat).to_csv(index=False),
        file_name="iat_attributions.csv" if show_assignments else "iat_scores.csv",
        mime="text/csv",
        key="dl_iat",
    )

    # 2. Indicateurs statistiques -------------------------------------------
    st.header("2. Indicateurs statistiques")
    c1, c2, c3 = st.columns(3)
    c1.metric("Itérations analysées", f"{len(iat):,}".replace(",", " "))
    c2.metric("Modèles évalués", iat["model"].nunique())
    c3.metric("Score moyen global", f"{iat['score'].mean():+.2f}")

    # 3. Interagir avec l'utilisateur ----------------------------------------
    st.header("3. Décortiquer un modèle")
    d1, d2 = st.columns(2)
    iat_model = d1.selectbox(
        "Modèle à inspecter", sorted(iat["model"].unique()), key="iat_model"
    )
    iat_proto = d2.selectbox("Protocole", ["Prénoms", "Adresses"], key="iat_proto")
    model_scores = iat[(iat["model"] == iat_model) & (iat["variant"] == iat_proto)]
    model_assign = iat_assign[
        (iat_assign["model"] == iat_model) & (iat_assign["variant"] == iat_proto)
    ]
    neg_share = negative_share_to_minority(model_assign)
    m1, m2, m3 = st.columns(3)
    m1.metric("Itérations", len(model_scores))
    m2.metric(
        "Score moyen",
        f"{model_scores['score'].mean():+.2f}",
        help="Négatif = la minorité reçoit surtout les mots négatifs.",
    )
    m3.metric(
        "Mots négatifs vers la minorité",
        "—" if neg_share.empty else f"{float(neg_share.iloc[0]):.0%}",
        help="50 % = répartition équitable.",
    )
    st.markdown("**Mot par mot — qui reçoit quoi ?**")
    st.dataframe(
        minority_share_by_word(model_assign),
        width="stretch",
        hide_index=True,
        column_config={
            "Part vers la minorité": st.column_config.ProgressColumn(
                "Part vers la minorité", min_value=0.0, max_value=1.0, format="percent"
            )
        },
    )
    st.caption(
        "Part des itérations où le mot est attribué au groupe minoritaire — "
        "en répartition équitable, chaque mot serait à 50 %."
    )

    # 4. Visualiser un graphique --------------------------------------------
    st.header("4. Visualisation par protocole")
    st.caption("Part des mots négatifs allant à la minorité — 50 % = équitable.")
    for protocole in ["Prénoms", "Adresses"]:
        shares = negative_share_to_minority(
            iat_assign[iat_assign["variant"] == protocole]
        )
        st.plotly_chart(iat_share_bars(shares, protocole), width="stretch")

    st.divider()
    st.subheader("Stabilité des scores sur les itérations")
    st.caption(
        "Chaque point est une itération ; le score résume vers qui penchent "
        "les mots (négatif = stéréotype envers la minorité, 0 = neutre)."
    )
    st.plotly_chart(
        iat_score_box(iat, "Distribution des scores par modèle et protocole"),
        width="stretch",
    )
