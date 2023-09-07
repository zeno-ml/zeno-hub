"""Calculate BLEU score."""
import math
from collections import Counter

from psycopg import sql

from zeno_backend.classes.base import GroupMetric
from zeno_backend.classes.metric import Metric
from zeno_backend.database.database import Database


def bleu(
    project_uuid: str, metric: Metric, model: str, filter: sql.Composed | None
) -> GroupMetric:
    """Calculate BLEU score.

    Args:
        project_uuid (str): project identifier
        metric (Metric): metric object
        model (str): model identifier
        filter (sql.Composed | None): filter to apply to the data

    Returns:
        GroupMetric: final metric and slice size
    """
    with Database() as db:
        output_col = db.execute_return(
            sql.SQL(
                "SELECT column_id FROM {} WHERE name = 'output' AND"
                " (model IS NULL OR model = {})"
            ).format(
                sql.Identifier(f"{project_uuid}_column_map"),
                sql.Literal(model),
            )
        )

        if len(output_col) == 0:
            return GroupMetric(metric=None, size=0)
        output_col = output_col[0][0]

        data = db.execute_return(
            sql.SQL("SELECT {}, label FROM {}").format(
                sql.Identifier(output_col), sql.Identifier(project_uuid)
            )
            if filter is None
            else sql.SQL("SELECT {}, label FROM {} WHERE ").format(
                sql.Identifier(output_col), sql.Identifier(project_uuid)
            )
            + filter
        )

        if data is None or len(data) == 0:
            return GroupMetric(metric=None, size=0)

        scorer = BleuScorer()
        score = scorer.score_corpus([d[0] for d in data], [d[1] for d in data])
        return GroupMetric(metric=float(score), size=len(data))


class BleuScorer:
    """A scorer that calculates BLEU score."""

    def __init__(self, weights=(0.25, 0.25, 0.25, 0.25), case_insensitive=False):
        """Initialize the scorer.

        Args:
            weights (tuple, optional): Statistic weights.
                Defaults to (0.25, 0.25, 0.25, 0.25).
            case_insensitive (bool, optional): Case sensitivity.
                Defaults to False.
        """
        self.weights = weights
        self.case_insensitive = case_insensitive

    def score_corpus(self, ref, out):
        """Score a corpus using BLEU score.

        Args:
          ref: A reference corpus
          out: An output corpus

        Returns:
          A tuple containing a single value for the BLEU score and a
            string summarizing auxiliary information
        """
        cached_stats = self.cache_stats(ref, out)
        return self.score_cached_corpus(range(len(ref)), cached_stats)

    def _precision(self, ref, out, n):
        """Caculate n-gram precision.

        Args:
          ref: A reference sentence
          out: An output sentence
          n: The ngram length to consider

        Returns:
          Numerator and denominator of the precision
        """
        out_ngram = sent_ngrams_list(out, n)
        ref_ngram = sent_ngrams_list(ref, n)
        out_cnt = Counter(out_ngram)
        ref_cnt = Counter(ref_ngram)

        num = 0
        denom = 0
        for ngram, o_cnt in out_cnt.items():
            num += min(o_cnt, ref_cnt[ngram])
            denom += o_cnt
        denom = max(1, denom)

        return num, denom

    def cache_stats(self, ref, out, src=None):
        """Cache sufficient statistics for caculating BLEU score.

        Args:
          ref: A reference corpus
          out: An output corpus
          src: A source courpus. Ignored if passed

        Returns:
          A list of cached statistics
        """
        if self.case_insensitive:
            ref = ref.lower()
            out = out.lower()

        cached_stats = []

        for r, o in zip(ref, out):
            prec = []
            for n in range(1, len(self.weights) + 1):
                prec.append(self._precision(r, o, n))
            cached_stats.append((len(r), len(o), prec))

        return cached_stats

    def score_cached_corpus(self, sent_ids, cached_stats):
        """Score a corpus using BLEU score with cache.

        Args:
          sent_ids: The sentence ids for reference and output corpora
          cached_stats: A list of cached statistics

        Returns:
          A tuple containing a single value for the BLEU score and a
            string summarizing auxiliary information
        """
        if len(cached_stats) == 0:
            return 0.0

        cached_ref_len, cached_out_len, cached_prec = zip(*cached_stats)

        num_prec = Counter()
        denom_prec = Counter()

        ref_len = 0
        out_len = 0
        for sent_id in sent_ids:
            ref_len += cached_ref_len[sent_id]
            out_len += cached_out_len[sent_id]
            for n in range(1, len(self.weights) + 1):
                num, denom = cached_prec[sent_id][n - 1]
                num_prec[n] += num
                denom_prec[n] += denom

        if num_prec[1] == 0:
            return 0

        prec = 0
        for i, w in enumerate(self.weights, start=1):
            p = num_prec[i] / denom_prec[i] if denom_prec[i] != 0 else 0
            p = math.log(p) if p > 0 else 0
            prec += p * w

        bp = min(1, math.exp(1 - ref_len / out_len)) if out_len != 0 else 0

        return bp * math.exp(prec)


def sent_ngrams_list(words, n):
    """Create a list with all the n-grams in a sentence.

    Arguments:
      words: A list of strings representing a sentence
      n: The ngram length to consider

    Returns:
      A list of n-grams in the sentence
    """
    word_ngram = []
    for i in range(len(words) - n + 1):
        ngram = tuple(words[i : i + n])
        word_ngram.append(ngram)
    return word_ngram
