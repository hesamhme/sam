from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from verification_service.tasks import verify_user
import redis

# Create a Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)


@csrf_exempt
def buy_stock(request):
    if request.method == 'POST':
        data = request.POST.dict()
        user = data.get('user')
        stock_name = data.get('stock_name')
        quantity = data.get('quantity')

        # Check if the quantity is provided
        if quantity is None:
            return JsonResponse({'error': 'Quantity is required'})

        quantity = int(quantity)  # Convert quantity to an integer

        # Retrieve user data from Redis
        user_data = r.hgetall(user)
        user_credit = float(user_data.get('credit'))

        # Check if user credit is enough to buy the stock
        if user_credit >= quantity:
            response = {'status': 'Accept'}
        else:
            response = {'status': 'Deny'}

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def buy_stock(request):
    if request.method == 'POST':
        data = request.POST.dict()
        user = data.get('user')
        stock_name = data.get('stock_name')
        quantity = int(data.get('quantity'))

        # Enqueue the user's buy request for verification
        verification_task = verify_user.delay(user)

        # Return an immediate response to the user
        response = {
            'status': 'Received',
            'task_id': verification_task.id
        }
        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request method'})
