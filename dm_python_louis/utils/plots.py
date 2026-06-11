"""Constructeurs de graphiques Plotly pour l'application Streamlit.

Tous les graphiques sont interactifs (survol des valeurs, zoom, légende
cliquable).
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def bar_rates(
    rates: pd.Series,
    title: str,
    xlabel: str,
    ylabel: str = "Taux d'acceptation",
    ref_line: float | None = None,
) -> go.Figure:
    """Diagramme en barres interactif d'une série de taux (valeurs entre 0 et 1)."""
    fig = go.Figure(
        go.Bar(
            x=rates.index.astype(str),
            y=rates.values,
            marker_color="#4C72B0",
            text=[f"{v:.0%}" for v in rates.values],
            textposition="outside",
            cliponaxis=False,
            hovertemplate=f"%{{x}}<br>{ylabel} : %{{y:.1%}}<extra></extra>",
        )
    )
    if ref_line is not None:
        fig.add_hline(y=ref_line, line_dash="dash", line_color="grey")
    fig.update_yaxes(range=[0, 1], tickformat=".0%", title_text=ylabel)
    fig.update_xaxes(title_text=xlabel)
    fig.update_layout(title=title, margin=dict(t=50, b=40))
    return fig


def deviation_bars(
    pivot: pd.DataFrame, title: str, xlabel: str, ylabel: str
) -> go.Figure:
    """Barres divergentes interactives centrées sur 0 (écarts positifs/négatifs)."""
    long = pivot.reset_index().melt(
        id_vars=pivot.index.name, var_name=pivot.columns.name, value_name="ecart"
    )
    fig = px.bar(
        long,
        x=pivot.index.name,
        y="ecart",
        color=pivot.columns.name,
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.add_hline(y=0, line_color="black", line_width=1)
    span = pivot.abs().to_numpy().max() * 1.25
    fig.update_yaxes(range=[-span, span], tickformat=".0%", title_text=ylabel)
    fig.update_xaxes(title_text=xlabel)
    fig.update_traces(hovertemplate="%{x}<br>%{y:.1%}<extra>%{fullData.name}</extra>")
    fig.update_layout(title=title, legend_title=pivot.columns.name, margin=dict(t=50, b=40))
    return fig


def french_choice_bars(pivot: pd.DataFrame, title: str) -> go.Figure:
    """Choix du français par modèle selon l'ordre — révèle le biais de position."""
    long = pivot.reset_index().melt(
        id_vars="model", var_name="Ordre", value_name="rate"
    )
    fig = px.bar(
        long,
        x="model",
        y="rate",
        color="Ordre",
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.add_hline(
        y=0.5,
        line_dash="dash",
        line_color="grey",
        annotation_text="choix au hasard (50 %)",
        annotation_position="top left",
    )
    fig.update_yaxes(range=[0, 1], tickformat=".0%", title_text="Choix du candidat français")
    fig.update_xaxes(title_text="Modèle")
    fig.update_traces(hovertemplate="%{x}<br>%{y:.0%}<extra>%{fullData.name}</extra>")
    fig.update_layout(title=title, legend_title="Ordre de présentation", margin=dict(t=50, b=40))
    return fig


def acceptance_heatmap(pivot: pd.DataFrame, title: str) -> go.Figure:
    """Carte de chaleur interactive d'un tableau croisé de taux d'acceptation."""
    fig = px.imshow(
        pivot,
        text_auto=".0%",
        color_continuous_scale="RdYlGn",
        aspect="auto",
    )
    fig.update_traces(
        hovertemplate="%{y} × %{x}<br>Taux d'acceptation : %{z:.1%}<extra></extra>"
    )
    fig.update_coloraxes(colorbar_tickformat=".0%")
    fig.update_layout(title=title, margin=dict(t=50, b=40))
    return fig


def iat_score_box(scores: pd.DataFrame, title: str) -> go.Figure:
    """Distribution des scores IAT par modèle et protocole (un point = une itération)."""
    fig = px.box(
        scores,
        x="model",
        y="score",
        color="variant",
        points="all",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="grey",
        annotation_text="neutre (0)",
        annotation_position="top left",
    )
    fig.update_yaxes(range=[-1.08, 1.08], title_text="Score d'association")
    fig.update_xaxes(title_text="Modèle")
    fig.update_layout(
        title=title, legend_title="Protocole", boxmode="group", margin=dict(t=50, b=40)
    )
    return fig


def iat_share_bars(shares: pd.Series, title: str) -> go.Figure:
    """Part (%) des mots négatifs allant à la minorité, avec repère à 50 %."""
    shares = shares.sort_values(ascending=True)
    colors = ["#C0392B" if v > 0.5 else "#27AE60" for v in shares]
    fig = go.Figure(
        go.Bar(
            x=shares.values,
            y=shares.index.astype(str),
            orientation="h",
            marker_color=colors,
            text=[f"{v:.0%}" for v in shares.values],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{y}<br>Part minorité : %{x:.1%}<extra></extra>",
        )
    )
    fig.add_vline(
        x=0.5,
        line_dash="dash",
        line_color="grey",
        annotation_text="équitable (50 %)",
        annotation_position="top",
        annotation_yshift=12,
    )
    fig.update_xaxes(
        range=[0, 1],
        tickformat=".0%",
        title_text="Part des mots négatifs reçue par la minorité",
    )
    fig.update_layout(
        title=title, height=70 * len(shares) + 150, margin=dict(t=70, b=40, r=60)
    )
    return fig
