from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .sheets import get_pipeline_sheet


# =====================================
# DATA FUNCTION (KEEP AT TOP)
# =====================================
def get_pipeline_data(request):

    sheet = get_pipeline_sheet()
    raw_data = sheet.get_all_records()


    # ======================
    # FILTER INPUTS
    # ======================
    country_filter = request.GET.get("country", "").strip().lower()
    owner_filter = request.GET.get("owner", "").strip().lower()
    stage_filter = request.GET.get("stage", "").strip().lower()

    pipeline = []
    stage_counts = {}
    owner_counts = {}
    country_counts = {}

    total_value = 0
    weighted_value = 0

    for index, row in enumerate(raw_data, start=2):

        item = {
            "row_number": index,
            "id": row.get("ID"),
            "opportunity": row.get("Opportunity Name", ""),
            "country": row.get("Country", ""),
            "stage": row.get("Pipeline Stage", ""),
            "owner": row.get("Internal Owner", ""),
            "min_value": row.get("Min Value (USD)", ""),
            "max_value": row.get("Max Value (USD)", ""),
            "weighted_value": row.get("Weighted Value (USD)", ""),
            "days": row.get("Days to Deadline", ""),
        }

        # ======================
        # NORMALIZE
        # ======================
        c = str(item["country"]).strip().lower()
        o = str(item["owner"]).strip().lower()
        s = str(item["stage"]).strip().lower()

        # ======================
        # FILTER LOGIC
        # ======================
        if country_filter and c != country_filter:
            continue

        if owner_filter and o != owner_filter:
            continue

        if stage_filter and s != stage_filter:
            continue

        pipeline.append(item)

        stage_counts[item["stage"]] = stage_counts.get(item["stage"], 0) + 1
        owner_counts[item["owner"]] = owner_counts.get(item["owner"], 0) + 1
        country_counts[item["country"]] = country_counts.get(item["country"], 0) + 1

        try:
            total_value += float(item["max_value"])
        except:
            pass

        try:
            weighted_value += float(item["weighted_value"])
        except:
            pass

    urgent = [x for x in pipeline if str(x["days"]).isdigit() and int(x["days"]) <= 14
    ]

    import json


    return {
        "pipeline": pipeline,
        "urgent": urgent,
        "total_opps": len(pipeline),
        "total_value": total_value,
        "weighted_value": weighted_value,

        # ✅ FIXED FOR CHART.JS
        "stage_labels": list(stage_counts.keys()),
        "stage_values": list(stage_counts.values()),

        "owner_labels": list(owner_counts.keys()),
        "owner_values": list(owner_counts.values()),

        "country_labels": list(country_counts.keys()),
        "country_values": list(country_counts.values()),
    }


# =====================================
# DASHBOARD (DEFAULT PAGE)
# =====================================
@login_required
def dashboard(request):
    context = get_pipeline_data(request)
    return render(request, "dashboard.html", context)


# =====================================
# FULL PIPELINE PAGE
# =====================================
@login_required
def pipeline_page(request):
    context = get_pipeline_data(request)
    return render(request, "pipeline.html", context)


# =====================================
# URGENT PAGE
# =====================================
@login_required
def urgent_page(request):
    context = get_pipeline_data(request)
    return render(request, "urgent.html", context)


# =====================================
# ADD PAGE
# =====================================
@login_required
def add_pipeline(request):

    if request.method == "POST":
        sheet = get_pipeline_sheet()

        new_row = [
            request.POST.get("id"),
            request.POST.get("opportunity"),
            request.POST.get("country"),
            request.POST.get("donor"),
            request.POST.get("technical_area"),
            request.POST.get("stage"),
            request.POST.get("min_value"),
            request.POST.get("max_value"),
            request.POST.get("weighted_value"),
            request.POST.get("owner"),
            request.POST.get("next_action"),
            request.POST.get("action_due"),
            request.POST.get("deadline"),
            request.POST.get("days"),
            request.POST.get("partners"),
            request.POST.get("risks"),
        ]

        sheet.append_row(new_row)

        return redirect("/pipeline/")

    return render(request, "add_pipeline.html")


# =====================================
# DELETE
# =====================================
@login_required
def delete_pipeline(request, row):
    sheet = get_pipeline_sheet()
    sheet.delete_rows(row)
    return redirect("/pipeline/")