from app.ml.pipeline.ranking_pipeline import RankingPipeline


if __name__ == "__main__":
    pipeline = RankingPipeline()
    job_description = "Senior Python backend engineer with FAISS, vector databases, retrieval, ranking, and production ML experience"
    results = pipeline.run(job_description)
    output_path = "submission.csv"
    pipeline.exporter.export(results, output_path)
    print(f"Generated {len(results)} ranked candidates")
    print(f"Wrote {output_path}")
