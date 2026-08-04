import re
from collections import Counter
from datetime import timedelta

from django.utils import timezone

from .models import Emotion, FoodMoodLog, InsightSummary


STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'from',
    'had', 'has', 'have', 'i', 'in', 'is', 'it', 'its', 'me', 'my', 'of',
    'on', 'or', 'so', 'that', 'the', 'this', 'to', 'was', 'were', 'with',
    'you', 'your', 'am', 'im', 'ive', 'just', 'like', 'really', 'very',
}


def tokenize_sensory_words(text):
    words = re.findall(r"[a-zA-Z']+", (text or '').lower())
    return [
        word.strip("'")
        for word in words
        if len(word.strip("'")) > 2 and word.strip("'") not in STOPWORDS
    ]


def weekly_consistency_score_from_logs(logs, today=None):
    """Percent of days logged in the current calendar week (Mon–Sun)."""
    today = today or timezone.localdate()
    week_start = today - timedelta(days=today.weekday())
    unique_days = {
        timezone.localtime(log.created_at).date()
        for log in logs
        if week_start <= timezone.localtime(log.created_at).date() <= today
    }
    return round(len(unique_days) / 7 * 100)


def build_mood_correlation_data(logs):
    """Map each mood to log count and top sensory word frequencies."""
    correlation = {}

    for log in logs:
        bucket = correlation.setdefault(log.emotion, {
            'log_count': 0,
            'words': Counter(),
        })
        bucket['log_count'] += 1
        bucket['words'].update(tokenize_sensory_words(log.food_description))

    serialized = {}
    for emotion, data in correlation.items():
        top_words = data['words'].most_common(10)
        serialized[emotion] = {
            'log_count': data['log_count'],
            'words': dict(top_words),
            'top_words': [word for word, _ in top_words[:5]],
        }
    return serialized


def recompute_insight_summary(user):
    """Rebuild the user's InsightSummary from all FoodMoodLog rows."""
    logs = list(
        FoodMoodLog.objects
        .filter(user=user)
        .only('emotion', 'food_description', 'created_at')
    )

    summary, _ = InsightSummary.objects.get_or_create(user=user)
    summary.total_logs_count = len(logs)
    summary.weekly_consistency_score = weekly_consistency_score_from_logs(logs)
    summary.mood_correlation_data = build_mood_correlation_data(logs)
    summary.save()
    return summary


MOOD_META = {
    'STRESSED': {'label': 'Stress', 'icon': 'bolt'},
    'BORED': {'label': 'Bored', 'icon': 'panorama_fish_eye'},
    'CALM': {'label': 'Calm', 'icon': 'spa'},
    'HAPPY': {'label': 'Happy', 'icon': 'wb_sunny'},
    'SAD': {'label': 'Sad', 'icon': 'cloud'},
    'TIRED': {'label': 'Tired', 'icon': 'bedtime'},
}


def _impact_label(share):
    if share >= 40:
        return 'High Impact'
    if share >= 20:
        return 'Steady Link'
    if share >= 10:
        return 'Low Correlation'
    return 'Minimal Effect'


def _node_size_class(share):
    if share >= 40:
        return 'w-24 h-24'
    if share >= 20:
        return 'w-20 h-20'
    if share >= 10:
        return 'w-16 h-16'
    return 'w-12 h-12'


def _node_style_class(share):
    if share >= 40:
        return 'bg-deep-forest text-sanctuary-white shadow-lg'
    if share >= 20:
        return 'border-2 border-deep-forest text-deep-forest'
    if share >= 10:
        return 'bg-seafoam-mist text-deep-forest'
    return 'bg-soft-sage text-deep-forest'


def build_insight_page_context(insight):
    """Shape InsightSummary JSON into template-friendly dashboard data."""
    correlation = (insight.mood_correlation_data if insight else {}) or {}
    total_logs = insight.total_logs_count if insight else 0
    weekly_consistency = insight.weekly_consistency_score if insight else 0

    mood_nodes = []
    for value, label in Emotion.choices:
        data = correlation.get(value, {})
        log_count = data.get('log_count', 0)
        share = round((log_count / total_logs) * 100) if total_logs else 0
        top_words = data.get('top_words') or list((data.get('words') or {}).keys())[:5]
        meta = MOOD_META[value]
        mood_nodes.append({
            'emotion': value,
            'label': meta['label'],
            'icon': meta['icon'],
            'log_count': log_count,
            'share': share,
            'impact_label': _impact_label(share),
            'size_class': _node_size_class(share),
            'style_class': _node_style_class(share),
            'top_words': top_words,
            'primary_word': top_words[0] if top_words else None,
        })

    ranked = sorted(mood_nodes, key=lambda node: (-node['share'], node['label']))
    top_mood = ranked[0] if ranked and ranked[0]['log_count'] else None
    secondary_mood = ranked[1] if len(ranked) > 1 and ranked[1]['log_count'] else None

    primary_driver = None
    if top_mood and top_mood['primary_word']:
        primary_driver = f"{top_mood['primary_word'].title()} notes when {top_mood['label'].lower()}"
    elif top_mood:
        primary_driver = f"Most frequent mood: {top_mood['label']}"

    observations = []
    if top_mood:
        words = ', '.join(top_mood['top_words'][:3]) if top_mood['top_words'] else 'comforting flavors'
        observations.append({
            'icon': 'insights',
            'title': f"{top_mood['label']} leads your pattern",
            'body': (
                f"{top_mood['label']} shows up in {top_mood['share']}% of your logs"
                f" ({top_mood['log_count']} "
                f"{'entry' if top_mood['log_count'] == 1 else 'entries'}). "
                f"Sensory words that often appear: {words}."
            ),
        })
    if secondary_mood:
        words = ', '.join(secondary_mood['top_words'][:3]) if secondary_mood['top_words'] else 'quieter notes'
        observations.append({
            'icon': 'spa',
            'title': f"{secondary_mood['label']} is a steady undercurrent",
            'body': (
                f"{secondary_mood['label']} accounts for {secondary_mood['share']}% of entries. "
                f"Common language around those meals: {words}."
            ),
        })
    if total_logs:
        observations.append({
            'icon': 'calendar_month',
            'title': f"{weekly_consistency}% weekly consistency",
            'body': (
                f"You've logged {total_logs} mindful "
                f"{'entry' if total_logs == 1 else 'entries'} overall. "
                f"This week your consistency score is {weekly_consistency}% "
                f"(unique days logged ÷ 7)."
            ),
        })
    if not observations:
        observations.append({
            'icon': 'edit_note',
            'title': 'Your patterns are waiting',
            'body': (
                'Log a few restorative entries and this space will fill with '
                'gentle observations about mood and nourishment.'
            ),
        })

    pathways = [
        {
            'icon': 'self_improvement',
            'duration': '5 MINS',
            'title': 'Pause before the pattern',
            'body': (
                f"When {top_mood['label'].lower()} shows up, take two soft breaths "
                f"before your next bite."
                if top_mood else
                'Before your next meal, pause for two soft breaths and notice how you feel.'
            ),
            'cta': 'Open Emotion',
            'url_name': 'emotion',
        },
        {
            'icon': 'water_drop',
            'duration': '1 MIN',
            'title': 'Sensory check-in',
            'body': (
                f"Name one flavor or texture—maybe “{top_mood['primary_word']}”—"
                f"and write it into your next log."
                if top_mood and top_mood['primary_word'] else
                'Name one flavor, texture, or temperature and capture it in your next log.'
            ),
            'cta': 'Log Entry',
            'url_name': 'journal_new',
        },
        {
            'icon': 'edit_note',
            'duration': '3 MINS',
            'title': 'Keep the streak gentle',
            'body': (
                f"You're at {weekly_consistency}% this week. One short entry today "
                f"keeps the rhythm without pressure."
                if total_logs else
                'Your first entry is enough. Capture one mood and one sensory detail today.'
            ),
            'cta': 'Add Reflection',
            'url_name': 'journal_history',
        },
    ]

    return {
        'insight': insight,
        'has_logs': total_logs > 0,
        'total_logs': total_logs,
        'weekly_consistency': weekly_consistency,
        'mood_nodes': mood_nodes,
        'top_mood': top_mood,
        'primary_driver': primary_driver,
        'observations': observations,
        'pathways': pathways,
        'last_computed': insight.last_computed if insight else None,
    }