import pandas as pd
from django.http import JsonResponse
from ..models import Employee
from ..serializers import EmployeeSerializer
from ..utils import calculate_age

# AVERAGE AGE BY INDUSTRY
def average_age_by_industry(request):
    employees = Employee.objects.values('id', 'industry', 'date_of_birth')
    df = pd.DataFrame(list(employees))
    if df.empty:
        return JsonResponse([], safe=False)

    df['age'] = df['date_of_birth'].apply(calculate_age.calculate_age)
    avg_age_by_industry = df.groupby('industry')['age'].mean().reset_index()
    avg_age_by_industry.rename(columns={'age': 'average_age'}, inplace=True)
    result = avg_age_by_industry.to_dict(orient='records')
    return JsonResponse(result, safe=False)


# SALARY BY INDUSTRY
def average_salary_by_industry(request):
    employees = Employee.objects.values('id', 'industry', 'salary')
    df = pd.DataFrame(list(employees))
    if df.empty:
        return JsonResponse([], safe=False)

    avg_salary_by_industry = df.groupby('industry')['salary'].mean().reset_index()
    avg_salary_by_industry.rename(columns={'salary': 'average_salary'}, inplace=True)
    result = avg_salary_by_industry.to_dict(orient='records')
    return JsonResponse(result, safe=False)


# SALARY BY EXPERIENCE
def average_salary_by_experience(request):
    employees = Employee.objects.values('id', 'years_of_experience', 'salary')
    df = pd.DataFrame(list(employees))
    if df.empty:
        return JsonResponse([], safe=False)

    df = df.dropna(subset=['years_of_experience'])
    avg_salary_by_experience = df.groupby('years_of_experience')['salary'].mean().reset_index()
    avg_salary_by_experience.rename(columns={'salary': 'average_salary'}, inplace=True)
    result = avg_salary_by_experience.to_dict(orient='records')
    return JsonResponse(result, safe=False)


# GENDER DISTRYBUTION PER INDUSTRY
def gender_distribution_per_industry(request):
    employees = Employee.objects.values('id', 'gender', 'industry')
    df = pd.DataFrame(list(employees))
    if df.empty:
        return JsonResponse([], safe=False)

    total_by_industry = df.groupby("industry")["id"].count().reset_index().rename(columns={"id": "total_employees"})
    gender_distribution = df.groupby(["industry", "gender"])["id"].count().reset_index().rename(columns={"id": "gender_count"})
    merged_df = gender_distribution.merge(total_by_industry, on="industry")
    merged_df["percentage"] = (merged_df["gender_count"] / merged_df["total_employees"]) * 100
    result = merged_df.to_dict(orient="records")
    return JsonResponse(result, safe=False)


# PERCENTAGE OF EMPLOYEES WITH SALARY ABOVE THRESHOLD
def percentage_above_threshold(request):
    try:
        salary_threshold = float(request.GET.get('salary_threshold', 0))
    except ValueError:
        return JsonResponse({"error": "Invalid salary_threshold parameter."}, status=400)
    employees = Employee.objects.values('id', 'salary', 'industry')
    df = pd.DataFrame(list(employees))
    if df.empty:
        return JsonResponse([], safe=False)

    total_by_industry = df.groupby("industry")["id"].count().reset_index().rename(columns={"id": "total_employees"})
    above_threshold = df[df["salary"] > salary_threshold].groupby("industry")["id"].count().reset_index().rename(columns={"id": "above_threshold"})
    merged_df = above_threshold.merge(total_by_industry, on="industry", how="right").fillna(0)
    merged_df["percentage_above_threshold"] = (merged_df["above_threshold"] / merged_df["total_employees"]) * 100
    result = merged_df.to_dict(orient="records")
    return JsonResponse(result, safe=False)