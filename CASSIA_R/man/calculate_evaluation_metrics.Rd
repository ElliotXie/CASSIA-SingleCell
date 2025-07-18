\name{calculate_evaluation_metrics}
\alias{calculate_evaluation_metrics}
\title{Calculate Evaluation Metrics}
\usage{
calculate_evaluation_metrics(eval_df, score_col = "score")
}
\arguments{
\item{eval_df}{Data frame containing evaluation results}

\item{score_col}{Character string specifying the column name for evaluation scores (default: "score")}
}
\value{
A named list containing calculated metrics:
\itemize{
\item mean_score: Average score
\item median_score: Median score
\item min_score: Minimum score
\item max_score: Maximum score
\item std_score: Standard deviation of scores
\item count: Number of evaluations
\item For 0-5 scale: perfect_ratio, very_good_ratio, good_ratio, partial_ratio, poor_ratio, nonsensical_ratio
}
}
\description{
Calculate comprehensive metrics from evaluation results including mean scores, distributions, and performance ratios.
}
\examples{
\dontrun{
# Calculate metrics from evaluation results
metrics <- calculate_evaluation_metrics(
  eval_df = evaluation_results,
  score_col = "evaluation_score"
)

# Print key metrics
cat("Mean Score:", metrics$mean_score, "\n")
cat("Perfect Predictions:", sprintf("%.1f%%", metrics$perfect_ratio * 100), "\n")
}
} 