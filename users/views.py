import json

from django.shortcuts import render
from django.contrib import messages
from summarytemplates.views import make_api_get_request, make_api_put_request
from users.forms import VehicleUserDataForm


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
    vehicle_user_data = json.dumps(data['userData'], indent=4, sort_keys=True)
    return render(request, 'users/user_vehicle.html', {
        'user': user,
        'vehicle_id': vehicle_id,
        'vehicle': vehicle,
        'vehicle_user_data': vehicle_user_data,
        'average_market_value': average_market_value,
        'annual_insurance_cost': annual_insurance_cost,
        'annual_fuel_cost': annual_fuel_cost,
        'annual_maintenance_cost': annual_maintenance_cost,
    })


def user_vehicle_user_data(request, user, vehicle_id):
    vehicle = make_api_get_request(f'/vehicles/{vehicle_id}?username={user}')

    if request.method == 'POST':
        form = VehicleUserDataForm(request.POST)
        if form.is_valid():
            vehicle['userData'] = {
                'insuranceRate': form['insurance_rate'].data,
                'insuranceProvider': form['insurance_provider'].data,
                'insuranceRenewalDate': form['insurance_renewal_date'].data,
                'financingInterestRate': form['financing_interest_rate'].data,
                'financingTermEnd': form['financing_term_end'].data,
                'previousMaintenanceData': form['previous_maintenance_data'].data,
            }
            del vehicle['vinAuditData']
            make_api_put_request(f'/vehicles/{vehicle_id}?username={user}', vehicle)
            messages.success(request, 'Vehicle updated successfully')
        else:
            messages.error(request, 'Invalid data')
    else:
        user_data = vehicle['userData']
        initial_data = {
            'insurance_rate': user_data['insuranceRate'],
            'insurance_provider': user_data['insuranceProvider'],
            'insurance_renewal_date': user_data['insuranceRenewalDate'],
            'financing_interest_rate': user_data['financingInterestRate'],
            'financing_term_end': user_data['financingTermEnd'],
            'previous_maintenance_data': user_data['previousMaintenanceData'],
        }
        form = VehicleUserDataForm(initial=initial_data)

    vehicle = make_api_get_request(f'/vehicles/{vehicle_id}?username={user}')
    return render(request, 'users/user_vehicle_user_data.html', {'user': user, 'vehicle': vehicle, 'form': form})


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
    if arr is None or len(arr) == 0:
        return 0
    return sum(arr) / len(arr)
