import json

from django.shortcuts import render

from summarytemplates.views import make_api_get_request


def index_get(request):
    data = make_api_get_request('/admin/users')
    return render(request, 'users/index.html', {'users': data})


def user_vehicle_get(request, user, vehicle_id):
    data = make_api_get_request(f'/admin/users/{user}/vehicles/{vehicle_id}')
    average_market_value = avg(list(map(
        lambda a: (null_conditional(a, 'group.max', 0) + null_conditional(a, 'group.min', 0)) / 2,
        null_conditional(data, 'vinAuditData.marketValue.prices.distribution', [])
    )))
    annual_insurance_cost = avg(null_conditional(data, 'vinAuditData.ownershipCost.insuranceCost', 0))
    annual_fuel_cost = avg(null_conditional(data, 'vinAuditData.ownershipCost.fuelCost', 0))
    annual_maintenance_cost = avg(null_conditional(data, 'vinAuditData.ownershipCost.maintenanceCost', 0))
    vehicle = json.dumps(data, indent=4, sort_keys=True)
    return render(request, 'users/user_vehicle.html', {
        'vehicle': vehicle,
        'average_market_value': average_market_value,
        'annual_insurance_cost': annual_insurance_cost,
        'annual_fuel_cost': annual_fuel_cost,
        'annual_maintenance_cost': annual_maintenance_cost,
    })


def null_conditional(obj, attr_string, default=None):
    try:
        attrs = attr_string.split('.')
        for attr in attrs:
            if isinstance(obj, dict):
                obj = obj.get(attr, default)
            else:
                obj = getattr(obj, attr, default)
        return obj
    except (AttributeError, KeyError):
        return default


def avg(arr):
    if len(arr) == 0 or arr is None:
        return 0
    return sum(arr) / len(arr)
