from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import joblib
import numpy as np
from PIL import Image as PILImage
from django.http import JsonResponse

from .models import Image, Prediction
from .serializers import MultipleImageSerializer

# Load the model
# model_path = settings.BASE_DIR / 'brainstroke.joblib'
# print(f"Loading model from: {model_path}")
# model = joblib.load(model_path)

class PredictView(APIView):
    pass
    # def post(self, request, *args, **kwargs):
    #     if not model:
    #         return JsonResponse({'error': 'Model could not be loaded'}, status=500)
        
    #     serializer = MultipleImageSerializer(data=request.data)
        
    #     if serializer.is_valid():
    #         images_data = serializer.validated_data['images']
    #         image_instances = []
    #         predictions = []
            
    #         for image_data in images_data:
    #             img_instance = Image.objects.create(user=request.user, image=image_data)
    #             image_instances.append(img_instance)
                
    #             img = PILImage.open(img_instance.image)
    #             img = img.resize((224, 224))  # Resize if necessary
    #             img_array = np.array(img) / 255.0  # Normalize if required
    #             img_array = img_array.reshape(1, -1)  # Reshape if necessary
                
    #             predictions.append(img_array)
            
    #         # Convert list of arrays to a single batch array
    #         batch_array = np.vstack(predictions)
            
    #         try:
    #             # Make batch prediction
    #             batch_prediction = model.predict(batch_array)
    #             batch_prediction_list = batch_prediction.tolist()
                
    #             # Save prediction
    #             prediction_instance = Prediction.objects.create(
    #                 user=request.user,
    #                 result=batch_prediction_list
    #             )
    #             prediction_instance.images.set(image_instances)
    #             prediction_instance.save()
                
    #             return Response({'predictions': batch_prediction_list})
    #         except Exception as e:
    #             return JsonResponse({'error': str(e)}, status=500)
        
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
