from flask_restx import Namespace, Resource
from time import perf_counter
from app.ml.pipeline.ranking_pipeline import RankingPipeline

debug_ns = Namespace('debug', description='Debug endpoints for ranking')


@debug_ns.route('/ranking')
class DebugRanking(Resource):
    def post(self):
        payload = debug_ns.payload or {}
        jd = payload.get('job_description', '')
        start = perf_counter()
        pipeline = RankingPipeline()
        results = pipeline.run(jd)
        elapsed = (perf_counter() - start) * 1000.0
        debug_items = []
        for i, item in enumerate(results[:20], start=1):
            debug_items.append({
                'rank': i,
                'candidate_id': item['candidate_id'],
                'score': item['score'],
                'evidence': item.get('explanation', {}),
                'behavior_trace': item.get('behavior_trace', {}),
            })
        return {'debug': debug_items, 'execution_time_ms': elapsed}
