from fastapi import APIRouter, BackgroundTasks
import pandas as pd
import os

router = APIRouter()

# Project root/data/cleaned_loan_data.csv
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "cleaned_loan_data.csv"
)


def get_combined_dataset():
    """Load historical data and combine with live predictions."""

    df = pd.DataFrame()

    # Load historical CSV
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH)
        except Exception as e:
            print(f"Could not read dataset: {e}")

    # Load live predictions
    try:
        from api.state import LIVE_PREDICTIONS

        if LIVE_PREDICTIONS:
            live_df = pd.DataFrame(LIVE_PREDICTIONS)

            if df.empty:
                df = live_df
            else:
                df = pd.concat(
                    [df, live_df],
                    ignore_index=True
                )

    except Exception as e:
        print(f"Could not load live predictions: {e}")

    return df


@router.get("/dashboard/stats")
def get_stats():
    try:
        df = get_combined_dataset()

        total = len(df)

        if total == 0:
            return {
                "total_applicants": 0,
                "low_risk": 0,
                "high_risk": 0,
                "avg_income": 0,
                "avg_credit_score": 0,
                "avg_loan_amount": 0
            }

        # Risk
        if "Risk_Status" in df.columns:
            low_risk = int(
                df[df["Risk_Status"].isin(
                    ["Low", "Low Risk"]
                )].shape[0]
            )

            high_risk = int(
                df[df["Risk_Status"].isin(
                    ["High", "High Risk"]
                )].shape[0]
            )
        else:
            low_risk = 0
            high_risk = 0

        # Average values
        avg_income = (
            float(df["Income"].mean(skipna=True))
            if "Income" in df.columns
            else 0.0
        )

        avg_credit = (
            float(df["Credit_Score"].mean(skipna=True))
            if "Credit_Score" in df.columns
            else 0.0
        )

        avg_loan = (
            float(df["Loan_Amount"].mean(skipna=True))
            if "Loan_Amount" in df.columns
            else 0.0
        )

        # Prevent NaN in JSON
        if pd.isna(avg_income):
            avg_income = 0.0

        if pd.isna(avg_credit):
            avg_credit = 0.0

        if pd.isna(avg_loan):
            avg_loan = 0.0

        return {
            "total_applicants": total,
            "low_risk": low_risk,
            "high_risk": high_risk,
            "avg_income": round(avg_income, 2),
            "avg_credit_score": round(avg_credit, 2),
            "avg_loan_amount": round(avg_loan, 2)
        }

    except Exception as e:
        return {"error": str(e)}


def generate_viz_bg(df, viz_dir):
    """Regenerate visualizations in background."""

    try:
        import matplotlib

        matplotlib.use("Agg")

        import sys

        src_dir = os.path.join(BASE_DIR, "src")

        if not os.path.exists(src_dir):
            return

        if src_dir not in sys.path:
            sys.path.append(src_dir)

        from visualization import generate_all_visualizations

        os.makedirs(viz_dir, exist_ok=True)

        generate_all_visualizations(df, viz_dir)

    except Exception as e:
        print(f"Failed to regenerate visualizations: {e}")


@router.get("/analysis/summary")
def get_summary(background_tasks: BackgroundTasks):

    try:
        df = get_combined_dataset()

        if df.empty:
            return {
                "employment_distribution": [
                    {"name": "Employed", "value": 0},
                    {"name": "Self-Employed", "value": 0},
                    {"name": "Unemployed", "value": 0}
                ],
                "risk_by_income": []
            }

        # Visualization directory
        viz_dir = os.path.join(
            BASE_DIR,
            "frontend",
            "public",
            "visualizations"
        )

        os.makedirs(viz_dir, exist_ok=True)

        background_tasks.add_task(
            generate_viz_bg,
            df.copy(),
            viz_dir
        )

        # --------------------------------
        # Employment Distribution
        # --------------------------------

        employed = 0
        self_employed = 0
        unemployed = 0

        # Historical one-hot encoded columns
        if "Employment_Status_Employed" in df.columns:
            employed += int(
                df["Employment_Status_Employed"]
                .fillna(0)
                .sum()
            )

        if "Employment_Status_Self-Employed" in df.columns:
            self_employed += int(
                df["Employment_Status_Self-Employed"]
                .fillna(0)
                .sum()
            )

        if "Employment_Status_Unemployed" in df.columns:
            unemployed += int(
                df["Employment_Status_Unemployed"]
                .fillna(0)
                .sum()
            )

        # Live categorical column
        if "Employment_Status" in df.columns:

            counts = df["Employment_Status"].value_counts(
                dropna=True
            )

            employed += int(
                counts.get("Employed", 0)
            )

            self_employed += int(
                counts.get("Self-Employed", 0)
            )

            unemployed += int(
                counts.get("Unemployed", 0)
            )

        employment_data = [
            {
                "name": "Employed",
                "value": employed
            },
            {
                "name": "Self-Employed",
                "value": self_employed
            },
            {
                "name": "Unemployed",
                "value": unemployed
            }
        ]

        # --------------------------------
        # Risk by Income
        # --------------------------------

        risk_by_income = []

        if (
            "Risk_Status" in df.columns
            and "Income" in df.columns
        ):

            income = pd.to_numeric(
                df["Income"],
                errors="coerce"
            )

            valid_income = income.dropna()

            if len(valid_income) > 0:

                try:
                    # qcut with duplicate protection
                    buckets = pd.qcut(
                        income,
                        q=4,
                        labels=[
                            "Low",
                            "Medium",
                            "High",
                            "Very High"
                        ],
                        duplicates="drop"
                    )

                    df_temp = df.copy()
                    df_temp["Income_Bucket"] = buckets

                    for bucket in [
                        "Low",
                        "Medium",
                        "High",
                        "Very High"
                    ]:

                        bucket_df = df_temp[
                            df_temp["Income_Bucket"] == bucket
                        ]

                        low_risk = int(
                            bucket_df[
                                bucket_df["Risk_Status"].isin(
                                    ["Low", "Low Risk"]
                                )
                            ].shape[0]
                        )

                        high_risk = int(
                            bucket_df[
                                bucket_df["Risk_Status"].isin(
                                    ["High", "High Risk"]
                                )
                            ].shape[0]
                        )

                        risk_by_income.append({
                            "bucket": bucket,
                            "Low Risk": low_risk,
                            "High Risk": high_risk
                        })

                except Exception as e:
                    print(
                        f"Income bucket calculation failed: {e}"
                    )

        return {
            "employment_distribution": employment_data,
            "risk_by_income": risk_by_income
        }

    except Exception as e:
        import traceback

        traceback.print_exc()

        return {
            "error": str(e)
        }